from typing import Dict, Tuple, Union

import aiohttp

from .. import utils, loader

from hikkatl.tl.patched import Message
from difflib import get_close_matches

# meta developer: @sqlmerr_m
# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/assets/banners/currencyconverter.png?raw=true


async def find_currency(from_: str, to: str) -> Union[Tuple[str, str, float], None]:
    async with aiohttp.ClientSession() as session:
        res = await session.get(
            "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
        )
        json: Dict[str, str] = await res.json()
        close_match = get_close_matches(from_, json.keys(), 1, cutoff=0.1)
        if not close_match or close_match[0] == "":
            return
        from_currency = json[close_match[0]]
        if not from_currency:
            return

        from_currency = close_match[0].upper()

        res2 = await session.get(
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{close_match[0]}.json"
        )
        json2: Dict[str, Union[str, Dict[str, str]]] = await res2.json()
        close_match2 = get_close_matches(
            to, json2[close_match[0]].keys(), 1, cutoff=0.1
        )
        if close_match2 and close_match2[0] != "":
            to_currency = json2[close_match[0]]
            if not to_currency:
                return
            to_currency = close_match2[0].upper()
            price = json2[from_currency.lower()][to_currency.lower()]
            if not isinstance(price, float):
                return
        else:
            return

    return from_currency, to_currency, price


@loader.tds
class CurrencyConverter(loader.Module):
    """Module for converting a large number of currencies to other currencies"""

    strings = {
        "name": "Currency Converter",
        "msg": "<emoji document_id=5364116657499285751>💲</emoji> <b>Convert</b>\n<i>{from_}</i> <b>/</b> <i>{to}</i> <code>{price}</code>",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> <b>No args!</b>",
        "args_too_short": "<emoji document_id=5210952531676504517>❌</emoji> <b>Args are too short!</b>",
        "not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>Currency not found!</b>",
    }

    strings_ru = {
        "msg": "<emoji document_id=5364116657499285751>💲</emoji> <b>Конвертация</b>\n<i>{from_}</i> <b>/</b> <i>{to}</i> <code>{price}</code>",
        "no_args": "<emoji document_id=5210952531676504517>❌</emoji> <b>Вы не передали аргументы!</b>",
        "args_too_short": "<emoji document_id=5210952531676504517>❌</emoji> <b>Слишком короткие аргументы!</b>",
        "not_found": "<emoji document_id=5210952531676504517>❌</emoji> <b>Валюта не найдена!</b>",
        "_cls_doc": "Модуль для конвертации большого количества валют в другие валюты",
    }

    @loader.command(ru_doc="[from] [to] Конвертировать одну валюту в другую")
    async def cconvert(self, message: Message):
        """[from] [to] Convert currency to other currency"""

        args = utils.get_args(message)
        if len(args) == 0:
            await utils.answer(message, self.strings("no_args"))
            return

        if len(args) < 2:
            await utils.answer(message, self.strings("args_too_short"))
            return

        from_, to = args[0].lower(), args[1].lower()
        result = await find_currency(from_, to)
        if result is None:
            await utils.answer(message, self.strings("not_found"))
            return

        await utils.answer(
            message,
            self.strings["msg"].format(
                from_=result[0], to=result[1], price=round(result[2], 2)
            ),
        )
