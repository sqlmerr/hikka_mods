# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: MineEVO-logs
# Description: Полезный модуль для логгирования в боте @mine_evo_bot | Для работы поставьте в конфиге ваш ник
# Author: sqlmerr
# Commands:
# .mlogging
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (1, 0, 0)
# meta developer: @sqlmerr_m
# only hikka

# импортируем нужные библиотеки
import asyncio

from telethon.tl.types import Message, ChatAdminRights
from telethon import events, functions, types

import logging

import re

from .. import loader, utils


logger = logging.getLogger(__name__)

# сам класс модуля
@loader.tds
class MineEVO_logs(loader.Module):
    """Полезный модуль для логгирования в боте @mine_evo_bot | Для работы поставьте в конфиге ваш ник"""
    # нужные переменные
    strings = {
        "name": "MineEVO-logging",
        "status": "Включен ли модуль или нет",
        "nickname": "Ваш ник в боте (важно)"
    }
    async def client_ready(self):
        # создается чат
        self._mineevologs_channel, _ = await utils.asset_channel(
            self._client,
            "MineEVO-logs - чат",
            "Не пишите сюда. Этот чат предназначет для модуля MineEVO-logs от @sqlmerr_m",
            silent=True,
            archive=True,
            _folder="hikka",
        )
        # в этот чат добавляется бот @mine_evo_bot
        await self.client(functions.channels.InviteToChannelRequest(self._mineevologs_channel, ['@mine_evo_bot']))
        # и этому боту выдаются права админа, для корректной работы бота
        await self.client(functions.channels.EditAdminRequest(
                channel=self._mineevologs_channel,
                user_id="@mine_evo_bot",
                admin_rights=ChatAdminRights(ban_users=True, post_messages=True, edit_messages=True),
                rank="MineEVO-logs",
            )
        )
            

    # функция, связанная с ООП и нужная для создания конфига
    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "nickname",
                "",
                lambda: self.strings("nickname"),
                validator=loader.validators.String()
            ),
        )

    # .mlogging
    @loader.command()
    async def mlogging(self, message: Message):
        """Включить/выключить логгирование"""
        if self.config["nickname"] != "":
            self.config["status"] = not self.config["status"]
            status = (
                "Логгирование включено <emoji document_id=5409048419211682843>💲</emoji>"
                if self.config["status"]
                else "Логгирование вкылючено <emoji document_id=5409048419211682843>💲</emoji>"
            )

            await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> <b>{}</b>".format(status))
        else:
            await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> <b>Логгирование не включено, так как вы не указали в конфиге ваш ник в боте <emoji document_id=5409048419211682843>💲</emoji></b>")
    
    @loader.watcher(only_pm=True, only_messages=True, from_id=5522271758)
    async def watcher(self, message: Message):
        if self.config["nickname"] != "":
            if self.config["status"]:
                #if self.config["nickname"] in message.raw_text:
                if "📦 Ты нашел(ла) Кейс!" in message.raw_text or "✉️ Ты нашел(ла) конверт." in message.raw_text or "🧧 Ты нашел(ла) редкий конверт." in message.raw_text or "🗳 Ты нашел(ла) Редкий Кейс!" in message.raw_text or "💎 Ты нашел(ла) Кристальный Кейс!" in message.raw_text or "🕋 Ты нашел(ла) Мифический Кейс!" in message.raw_text or"передал(а) игроку" in message.raw_text or "передал(а) тебе" in message.raw_text:
                    await self.client.send_message(self._mineevologs_channel, message.text)
