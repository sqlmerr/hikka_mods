# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------
# Name: MineEVO
# Description: Полезный модуль для бота @mine_evo_bot
# Author: sqlmerr
# Commands:
# .mevoprofile | .mevocases | .mevoperevod | .mevomine
# ---------------------------------------------------------------------------------

__version__ = (0, 2, 6)
# meta developer: @sqlmerr_m


import asyncio

from telethon.tl.types import Message
from telethon import events, functions, types

import logging

from asyncio import sleep

from .. import loader, utils


logger = logging.getLogger(__name__)

@loader.tds
class MineEVO(loader.Module):
    """Полезный модуль для бота @mine_evo_bot"""
    strings = {
        "name": "MineEVO",
        "mine_interval": "Интервал копания",
        "mine_status": "Ну тип копаете вы или нет",
        "perevod_interval": "Интервал перевода лимитов",
        "perevod_status": "Ну тип переводите вы лимиты или нет"
    }


    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "mine_interval",
                2.0,
                lambda: self.strings("mine_interval"), 
                validator=loader.validators.Float()
            ),

            loader.ConfigValue(
                "mine_status",
                False,
                lambda: self.strings("mine_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "perevod_interval",
                2.0,
                lambda: self.strings("perevod_interval"), 
                validator=loader.validators.Float()
            ),
            loader.ConfigValue(
                "perevod_status",
                False,
                lambda: self.strings("perevod_interval"), 
                validator=loader.validators.Boolean()
            )
        )

    @loader.command()
    async def mevoprofile(self, message: Message):
        """отправляет в текущий чат ваш профиль в боте @mine_evo_bot (❗️не рекомендую использовать во время копания❗️)"""
        await utils.answer(message, 'pon')
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
            await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> mine_status -> Измените False на True")
            return
        interval = self.config["mine_interval"]

        logger.debug("start mining...")            
        await utils.answer(message, 'Копаю ⛏')
        while self.config["mine_status"]:
            if self.config["mine_status"]:
                await self.client.send_message("@mine_evo_bot", "коп")
                await sleep(interval)
            else:
                await utils.answer(message, 'Вы остановили майнинг')


    @loader.command()
    async def mevoperevod(self, message: Message):
        """.mevoperevod <кол-во лимитов> <ник чела в боте> - Автоматически переводит лимиты за вас"""
        if not self.config["perevod_status"]:
            await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> perevod_status -> Измените False на True. Это сделано для защиты от случайных переводов")
            return
        interval = self.config["perevod_interval"]
        args = utils.get_args_raw(message).split()

        if not args:
            utils.answer(message, 'ошибка')
            return

        logger.debug("starting to transfer limits...")
        await utils.answer(message, 'Начинаю переводить лимиты')

        if self.config["perevod_status"]:
            for i in range(int(args[0])):
                if self.config["perevod_status"]:
                    await self.client.send_message("@mine_evo_bot", f"Перевести {args[1]} лимит")
                    await sleep(interval)
                else:
                    await utils.answer(message, 'Вы остановили перевод лимитов')
                    return
            await utils.answer(message, 'Все лимиты переведены!')
