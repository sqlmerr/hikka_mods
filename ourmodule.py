import asyncio

from telethon.tl.types import Message
from telethon import functions

from .. import loader, utils

@loader.tds
class OurModule(loader.Module):
    """Описание нашего модуля"""
    strings = {
        "name": "OurMod",
        "pon": "pon_pon"
    }
    strings_ru = {
        "name": "НашМодуль",
        "пон": "пон_пон"
    }

    @loader.command(ru_doc="описание вашей команды на русском") # p.s. можно делать не только ru_doc, всё расписано на dev.hikka.pw
    async def ourcommand(self, message):
        """Стандартное описание команды"""
        pon = self.strings("pon")
        await utils.answer(message, f"поздравляю, вы создали свою первую команду!, {pon}")
    