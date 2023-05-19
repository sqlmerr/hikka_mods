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

from .. import loader, utils


@loader.tds
class MineEVO(loader.Module):
    strings = {"name": "MineEVO"}

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