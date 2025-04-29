import datetime
import io
import contextlib
import logging
import sys
import typing

from meval import meval
from dataclasses import dataclass, field

from hikkatl.errors.rpcerrorlist import MessageIdInvalidError
from hikkatl.types import Message

from .. import loader, utils
from ..inline.types import InlineCall
from ..log import HikkaException
from ..types import HikkaReplyMarkup


# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_upgradedeval.png?raw=true
# meta icon: https://github.com/sqlmerr/hikka_mods/blob/main/assets/icons/upgradedeval.png?raw=true
# meta developer: @sqlmerr_m

ITEMS_PER_PAGE = 6

@dataclass(frozen=True)
class EvaluationInfo:
    code: str
    result: typing.Optional[str] = field(default=None)
    error: typing.Optional[HikkaException] = field(default=None)
    is_error: bool = field(default=False)
    date: datetime.datetime = field(default_factory=datetime.datetime.now)


@loader.tds
class UpgradedEval(loader.Module):
    """Just eval with customizable text and stdout"""

    strings = {
        "name": "UpgradedEval",
        "_cfg_text_result": "Text for result",
        "_cfg_text_error": "Text for error",
        "_cfg_mode": "Code run mode. stdout is when print works. return, this is standard .e; auto is just a mode that automatically selects stdout or return",
    }

    strings_ru = {
        "_cfg_text_result": "Текст результата",
        "_cfg_text_error": "Текст ошибки",
        "_cfg_mode": "Режим запуска кода. stdout, это когда работает print. return, это стандартный .e; auto - это просто режим, который автоматически выбирает stdout или return",
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text_result",
                "<emoji document_id=5197646705813634076>🐍</emoji> <b><i>Code:</i></b>\n<code><pre class='language-python'>{code}</pre></code>\n\n<emoji document_id=5895231943955451762>✅</emoji> <b><i>Result:</i></b>\n<code><pre class='language-python'>{result}</pre></code>",
                lambda: self.strings("_cfg_text_result"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "text_error",
                "<emoji document_id=5197646705813634076>🐍</emoji> <b><i>Code:</i></b>\n<code><pre>{code}</pre></code>\n\n<emoji document_id=5465665476971471368>❌</emoji> <b><i>Error:</i></b>\n<code><pre class='language-python'>{error}</pre></code>",
                lambda: self.strings("_cfg_text_error"),
                validator=loader.validators.String(),
            ),
            loader.ConfigValue(
                "mode",
                "auto",
                lambda: self.strings("_cfg_mode"),
                validator=loader.validators.Choice(["stdout", "return", "auto"]),
            ),
        )
        self._evals: typing.List[EvaluationInfo] = []


    async def __inline_open_eval(self, call: InlineCall, eval_info: EvaluationInfo, current_page: int):
        if not eval_info.is_error:
            text = self.config["text_result"].format(
                code=utils.escape_html(eval_info.code) if eval_info.code else "None",
                result=eval_info.result if eval_info.result else "None",
            )
        else:
            error = (
                self.lookup("Evaluator").censor(
                    (
                            "\n".join(eval_info.error.full_stack.splitlines()[:-1])
                            + "\n\n"
                            + "🚫 "
                            + eval_info.error.full_stack.splitlines()[-1]
                    )
                ),
            )
            text = self.config["text_error"].format(
                code=utils.escape_html(eval_info.code), error=error[0]
            )


        await call.edit(
            text=text,
            reply_markup={
                "text": "←",
                "callback": self.__inline_open,
                "args": (current_page,)
            }
        )

    async def __inline_open(self, call: InlineCall, page: int = 0):
        await call.edit(
            text="📋 <b>Evaluation history</b>",
            reply_markup=self.__inline_generate_keyboard(self._evals, page),
        )

    def __inline_generate_keyboard(self, evals: typing.List[EvaluationInfo], page: int = 0):
        if len(evals) == 0:
            return []

        # Sort evals in descending order based on date to ensure newest first
        sorted_evals = sorted(evals, key=lambda x: x.date, reverse=True)

        offset = page * ITEMS_PER_PAGE
        if offset < 0 or offset >= len(sorted_evals):
            page = 0
            offset = 0

        # Slice evaluations for the current page
        page_evals = sorted_evals[offset:offset + ITEMS_PER_PAGE]
        buttons = []

        # Generate buttons for evaluations on current page (no reverse)
        for e in page_evals:
            buttons.append(
                [{
                    "text": f"{e.date.strftime('%Y-%m-%d %H:%M:%S')} {'✅' if not e.is_error else '❌'}",
                    "callback": self.__inline_open_eval,
                    "args": (e, page)
                }]
            )

        # Navigation buttons
        nav_buttons = []
        if offset > 0:
            nav_buttons.append({
                "text": "<",
                "callback": self.__inline_open,
                "args": (page - 1,)
            })
        else:
            nav_buttons.append({
                "text": "X",
                "data": "empty"
            })

        nav_buttons.append({
            "text": f"{page + 1}/{(len(evals) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE}",
            "data": "empty"
        })

        if offset + ITEMS_PER_PAGE < len(sorted_evals):
            nav_buttons.append({
                "text": ">",
                "callback": self.__inline_open,
                "args": (page + 1,)
            })
        else:
            nav_buttons.append({
                "text": "X",
                "data": "empty"
            })

        if nav_buttons:
            buttons.append(nav_buttons)

        return buttons

    @loader.command(ru_doc="Получить историю (с рестарта юзербота)")
    async def ehistory(self, message: Message):
        """Get history (since userbot restart)"""

        await self.inline.form(
            text="📋 <b>Evaluation history</b>",
            message=message,
            reply_markup=self.__inline_generate_keyboard(self._evals),
        )

    @loader.command(ru_doc="Улучшенный eval")
    async def ie(self, message: Message):
        """Upgraded eval"""
        args = utils.get_args_raw(message)

        try:
            attrs = await self.lookup("Evaluator").getattrs(message)
            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                result = await meval(
                    utils.escape_html(args),
                    globals(),
                    **attrs,
                )
            output = stdout.getvalue()

        except Exception:
            item = HikkaException.from_exc_info(*sys.exc_info())
            error = (
                self.lookup("Evaluator").censor(
                    (
                        "\n".join(item.full_stack.splitlines()[:-1])
                        + "\n\n"
                        + "🚫 "
                        + item.full_stack.splitlines()[-1]
                    )
                ),
            )

            await utils.answer(
                message,
                self.config["text_error"].format(
                    code=utils.escape_html(utils.get_args_raw(message)), error=error[0]
                ),
            )

            self._evals.append(EvaluationInfo(
                args,
                error=item,
                is_error=True,
            ))
            return

        mode = self.config["mode"]
        if mode == "stdout":
            result = output
        elif mode == "auto" and output.strip():
            result = output


        if callable(getattr(result, "stringify", None)):
            with contextlib.suppress(Exception):
                result = str(result.stringify())

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.config["text_result"].format(
                    code=utils.escape_html(args) if args else "None",
                    result=result if result else "None",
                ),
            )

        self._evals.append(EvaluationInfo(
            args,
            result=result,
        ))
