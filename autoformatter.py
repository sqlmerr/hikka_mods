# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: AutoFormatter
# Description: Automatically formats the text of your messages | Автоматически форматирует текст ваших сообщений | Check The Config | Загляните в конфиг
# Author: sqlmerr
# Commands:
# .textformat
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
class AutoFormatter(loader.Module):
    """Automatically formats the text of your messages | Автоматически форматирует текст ваших сообщений | Check The Config | Загляните в конфиг"""
    # нужные переменные
    strings = {
        "name": "AutoFormatter",
        "status": "Module enabled or disabled",
        "format": "Text Format",
        "type": "Formatting Type",
        "custom_format": "Custom Text Format | Write as in: text in the left \ text in the right",
        "space": "Is there a space between a custom text format?",
        "exceptions": "This is exceptions, this text is not formated"
    }
    strings_ru = {
        "status": "Включен или выключен модуль",
        "format": "Формат текста",
        "type": "Тип форматирования",
        "custom_format": "Свой формат текста | Пишите в таком формате: текст слева \ текст справа",
        "space": "Есть ли пробел между кастомным форматированием?",
        "exceptions": "Это исключения, этот текст не будет форматироваться"
    }

    def __init__(self):
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "status",
                False,
                lambda: self.strings("status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "format",
                'Bold',
                lambda: self.strings("format"),
                validator=loader.validators.Choice(["Bold", "Mono", "Italic", "Custom"])
            ),
            loader.ConfigValue(
                "type",
                'send_new',
                lambda: self.strings("type"),
                validator=loader.validators.Choice(["send_new", "edit"])
            ),
            loader.ConfigValue(
                "custom_format",
                None,
                lambda: self.strings("custom_format"),
                validator=loader.validators.String()
            ),
            loader.ConfigValue(
                "space",
                True,
                lambda: self.strings("space"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "exceptions",
                [None],
                lambda: self.strings("exceptions"),
                validator=loader.validators.Union(
                    loader.validators.String(), loader.validators.NoneType()
                )
            ),
        )

    @loader.watcher(only_messages=True, no_commands=True, no_stickers=True, no_docs=True, no_audios=True, no_videos=True, no_photos=True, no_forwards=True)
    async def watcher(self, message):
        if self.config["status"]:
            ss = False
            id_ = await self.client.get_peer_id('me')
            if self.config["format"] == "Bold":
                o, oo = "<b>", "</b>"
            elif self.config["format"] == "Mono":
                o, oo = "<code>", "</code>"
            elif self.config["format"] == "Italic":
                o, oo = "<i>", "</i>"
            elif self.config["format"] == "Custom":
                ss = True
            else:
                return
            
            reply = await message.get_reply_message()

            exc = self.config["exceptions"]
            if message.from_id == id_:
                if ss:
                    f = self.config["custom_format"].split(" \ ")[0]
                    ff = self.config["custom_format"].split(" \ ")[1]
                    if f is None:
                        return
                    text = message.text
                    if exc != [None]:
                        if f in text or exc in text:
                            return
                    else:
                        if f in text:
                            return

                    if self.config["type"] == 'send_new':
                        await message.delete()
                        if self.config["space"]:
                            if reply:
                                await self.client.send_message(message.to_id, f"{f} {text} {ff}", reply_to=reply)
                            else:
                                await self.client.send_message(message.to_id, f"{f} {text} {ff}")
                        else:
                            if reply:
                                await self.client.send_message(message.to_id, f"{f}{text}{ff}", reply_to=reply)
                            else:
                                await self.client.send_message(message.to_id, f"{f}{text}{ff}")
                    elif self.config["type"] == 'edit':
                        if self.config["space"]:
                            await utils.answer(message, f"{f} {text} {ff}")
                        else:
                            await utils.answer(message, f"{f}{text}{ff}")
                else:
                    text = message.text
                    if exc != [None]:
                        if o in text or oo in text or exc in text:
                            return
                        if text in exc:
                            return
                    else:
                        if o in text or oo in text:
                            return
                    if self.config["type"] == 'send_new':
                        await message.delete()
                        if reply:
                            await self.client.send_message(message.to_id, f"{o}{text}{oo}", reply_to=reply)
                        else:
                            await self.client.send_message(message.to_id, f"{o}{text}{oo}")
                    elif self.config["type"] == 'edit':
                        await utils.answer(message, f"{o}{text}{oo}")


    @loader.command(ru_doc="Включить/выключить модуль")
    async def textformat(self, message: Message):
        """Turn on/off The Module"""
        self.config["status"] = not self.config["status"]
        status = (
            "<emoji document_id=5447644880824181073>⚠️</emoji> Модуль включен | Module is now enabled"
            if self.config["status"]
            else "<emoji document_id=5447644880824181073>⚠️</emoji>Модуль выключен | Module is now disabled"
        )

        await utils.answer(message, "<b>{}</b>".format(status))
