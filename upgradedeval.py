import io
import contextlib
import itertools
import os
import sys
import typing
from types import ModuleType
from meval import meval

import hikkatl
from hikkatl.errors.rpcerrorlist import MessageIdInvalidError
from hikkatl.sessions import StringSession
from hikkatl.tl.types import Message

from .. import loader, utils, main
from ..log import HikkaException


# meta banner: https://github.com/sqlmerr/sqlmerr/blob/main/assets/hikka_mods/sqlmerrmodules_eval.png?raw=true
# meta developer: @sqlmerr_m

@loader.tds
class UpgradedEval(loader.Module):
    """Just eval with custom text and stdout"""
    strings = {
        "name": "UpgradedEval",
        "_cfg_text_result": "Text for result",
        "_cfg_text_error": "Text for error"
    }
    
    strings_ru = {
        "_cfg_text_result": "Текст результата",
        "_cfg_text_error": "Текст ошибки"
    }

    async def client_ready(self):
        await self.request_join(
            "@sqlmerr_m", "Я делаю модули за бесплатно, ни копейки не получая. Подписка на канал ваша лучшая поддержка!"
        )
    

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "text_result",
                "🐍 <b><i>Code:</i></b>\n<code>{code}</code>\n\n✅ <b><i>Result:</i></b>\n<code>{result}</code>",
                lambda: self.strings("_cfg_text_result"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "text_error",
                "🐍 <b><i>Code:</i></b>\n<code>{code}</code>\n\n❌ <b><i>Error:</i></b>\n<code>{error}</code>",
                lambda: self.strings("_cfg_text_error"),
                validator=loader.validators.String()
            ),
        )

    @loader.command(ru_doc="Улучшенный eval")
    async def ie(self, message):
        """Upgraded eval"""
        args = utils.get_args_raw(message)
        
        try:
            stdout = io.StringIO() 
            with contextlib.redirect_stdout(stdout):
                await meval(utils.escape_html(args), globals(), **await self.getattrs(message))
            result = stdout.getvalue() 

        except Exception as e:
            item = HikkaException.from_exc_info(*sys.exc_info())
            error = self.censor(
                (
                    "\n".join(item.full_stack.splitlines()[:-1])
                    + "\n\n"
                    + "🚫 "
                    + item.full_stack.splitlines()[-1]
                )
            ),

            # await utils.answer(message, str(error))

            await utils.answer(
                message,
                self.config["text_error"].format(
                    code=utils.escape_html(utils.get_args_raw(message)),
                    error=error[0]
                ),
            )

            return
        
        if callable(getattr(result, "stringify", None)):
            with contextlib.suppress(Exception):
                result = str(result.stringify())

        with contextlib.suppress(MessageIdInvalidError):
            await utils.answer(
                message,
                self.config["text_result"].format(
                    code=utils.escape_html(args) if args else "None",
                    result=result if result else "None"
                ),
            )
    
    # https://github.com/hikariatama/Hikka/blob/master/hikka/modules/eval.py
    async def getattrs(self, message: Message) -> dict:
        reply = await message.get_reply_message()
        return {
            "message": message,
            "client": self._client,
            "reply": reply,
            "r": reply,
            **self.get_sub(hikkatl.tl.types),
            **self.get_sub(hikkatl.tl.functions),
            "event": message,
            "chat": message.to_id,
            "hikkatl": hikkatl,
            "telethon": hikkatl,
            "utils": utils,
            "main": main,
            "loader": loader,
            "f": hikkatl.tl.functions,
            "c": self._client,
            "m": message,
            "lookup": self.lookup,
            "self": self,
            "db": self.db,
        }

    # https://github.com/hikariatama/Hikka/blob/master/hikka/modules/eval.py
    def get_sub(self, obj: typing.Any, _depth: int = 1) -> dict:
        """Get all callable capitalised objects in an object recursively, ignoring _*"""
        return {
            **dict(
                filter(
                    lambda x: x[0][0] != "_"
                    and x[0][0].upper() == x[0][0]
                    and callable(x[1]),
                    obj.__dict__.items(),
                )
            ),
            **dict(
                itertools.chain.from_iterable(
                    [
                        self.get_sub(y[1], _depth + 1).items()
                        for y in filter(
                            lambda x: x[0][0] != "_"
                            and isinstance(x[1], ModuleType)
                            and x[1] != obj
                            and x[1].__package__.rsplit(".", _depth)[0] == "hikkatl.tl",
                            obj.__dict__.items(),
                        )
                    ]
                )
            ),
        }

    def censor(self, ret: str) -> str:
        ret = ret.replace(str(self._client.hikka_me.phone), "&lt;phone&gt;")

        if redis := os.environ.get("REDIS_URL") or main.get_config_key("redis_uri"):
            ret = ret.replace(redis, f'redis://{"*" * 26}')

        if db := os.environ.get("DATABASE_URL") or main.get_config_key("db_uri"):
            ret = ret.replace(db, f'postgresql://{"*" * 26}')

        if btoken := self._db.get("hikka.inline", "bot_token", False):
            ret = ret.replace(
                btoken,
                f'{btoken.split(":")[0]}:{"*" * 26}',
            )

        if htoken := self.lookup("loader").get("token", False):
            ret = ret.replace(htoken, f'eugeo_{"*" * 26}')

        ret = ret.replace(
            StringSession.save(self._client.session),
            "StringSession(**************************)",
        )

        return ret
