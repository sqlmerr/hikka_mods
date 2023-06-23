# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: MineEVO-bossfarm
# Description: Полезный модуль для фарма боссов в боте @mine_evo_bot
# Author: sqlmerr
# Commands:
# .mautoboss
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (1, 0, 1)
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
class MineEVO_bossfarm(loader.Module):
    """Полезный модуль для фарма боссов в боте @mine_evo_bot"""
    # нужные переменные
    strings = {
        "name": "MineEVO-bossfarm",
        "status": "Включен ли модуль или нет",
        "boss": "Какого босса бить автоматически? По счёту (например: слайм - 1, каменный голем - 5)",
        "delay": "Время между чеканьем боссов"
    }
    async def client_ready(self):
        # создается чат
        self._mineevoboss_channel, _ = await utils.asset_channel(
            self._client,
            "MineEVO-bosses - чат",
            "Не пишите сюда. Этот чат предназначет для модуля MineEVO-bosses от @sqlmerr_m",
            silent=True,
            archive=True,
            _folder="hikka",
        )
        # в этот чат добавляется бот @mine_evo_bot
        await self.client(functions.channels.InviteToChannelRequest(self._mineevoboss_channel, ['@mine_evo_bot']))
        # и этому боту выдаются права админа, для корректной работы бота
        await self.client(functions.channels.EditAdminRequest(
                channel=self._mineevoboss_channel,
                user_id="@mine_evo_bot",
                admin_rights=ChatAdminRights(ban_users=True, post_messages=True, edit_messages=True),
                rank="MineEVO-bosses",
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
                "boss",
                None,
                lambda: self.strings("boss"),
                validator=loader.validators.Integer()
            ),
            loader.ConfigValue(
                "delay",
                5,
                lambda: self.strings("delay"),
                validator=loader.validators.Integer()
            ),
        )

    # .mautosell
    @loader.command()
    async def mautoboss(self, message: Message):
        """Включить/выключить автофарм боссов"""
        self.config["status"] = not self.config["status"]
        status = (
            "<emoji document_id=5409048419211682843>💲</emoji> Автофарм боссов включен"
            if self.config["status"]
            else "<emoji document_id=5409048419211682843>💲</emoji> Автофарм боссов выключен"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус автофарма боссов:\n <b>{}</b>".format(status))
        self.config["status"]
        if self.config["status"]:
            while self.config["status"]:
                boss = self.config["boss"]
                if self.config["status"]:
                    async with self._client.conversation(self._mineevoboss_channel) as conv:
                        a = await conv.send_message('Боссы')
                        # получаем ответ
                        b = await conv.get_response()
                        list_msgs_id = [a.id, b.id]
                    await b.click(boss-1)
                    await asyncio.sleep(self.config["delay"])
                else:
                    return
                    break
        else:
            return

