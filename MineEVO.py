# ---------------------------------------------------------------------------------
# Name: MineEVO
# Description: Полезный модуль для бота @mine_evo_bot
# Author: sqlmerr
# Commands:
# .mevoprofile | .mevocases
# ---------------------------------------------------------------------------------

__version__ = (0, 1, 0)
# meta developer: @sqlmerr_m


import asyncio

from telethon.tl.types import Message
from telethon import events, functions, types

import logging

from .. import loader, utils


logger = logging.getLogger(__name__)

@loader.tds
class MineEVO(loader.Module):
    """Полезный модуль для бота @mine_evo_bot"""
    strings = {
        "name": "MineEVO",
        "mine_interval": "Интервал копания в секундах (integer)",
        "mine_status": "Ну тип копаете вы или нет"
    }
    strings_ru = {
        "mine_interval": "Интервал копания в секундах (integer)",
        "mine_status": "Ну тип копаете вы или нет"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "mine_interval",
                2,
                lambda: self.strings("mine_interval")
                validator=loader.validators.Integer()),
            loader.ConfigValue(
                "mine_status",
                False,
                lambda: self.strings("mine_status")
                validator=loader.validators.Boolean()),
        )

    @loader.command()
    async def mevoprofile(self, message: Message):
        """отправляет в текущий чат ваш профиль в боте @mine_evo_bot (❗️не рекомендую использовать во время копания❗️)"""
        async with self._client.conversation("@mine_evo_bot") as conv:
            await conv.send_message('профиль')  # upload step
            response = await conv.get_response() # first message
            await utils.answer(message, response)

    @loader.command()
    async def mevocases(self, message: Message):
        """отправляет в текущий чат ваши кейсы в боте @mine_evo_bot (❗️не рекомендую использовать во время копания❗️)"""
        
        async with self._client.conversation("@mine_evo_bot") as conv:
            await conv.send_message('кейсы')  # upload step
            response = await conv.get_response() # first message
            await utils.answer(message, response)
    
    @loader.command()
    async def mevomine(self, message: Message):
        """Автоматически копает за вас"""
        if not self.config["mine_status"]:
            return
        logger.debug("start mining")
        while self.config["mine_status"]:
            await self.client.send_message("@mine_evo_bot", "Копать")
        await utils.answer(message, 'Копаю ⛏')
