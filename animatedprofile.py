# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: AnimatedProfile
# Description: Модуль для анимации вашего профиля (имя, био)
# Author: sqlmerr
# Commands:
# .animatedname (.aname) | .animatedbio (.abio) | .animationconstructor (.aconstructor)
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

from ..inline.types import InlineCall
from .. import loader, utils


logger = logging.getLogger(__name__)

# сам класс модуля
@loader.tds
class AnimatedProfile(loader.Module):
    """Модуль для анимации вашего профиля (имя, био)"""
    strings = {
        "name": "AnimatedProfile",
        "name_status": "Включена ли анимация имени или нет",
        "name_delay": "Время между кадрами анимации имени",
        "animated_name_frames": "Кадры анимации имени",
        "bio_status": "Включена ли анимация био или нет",
        "bio_delay": "Время между кадрами анимации био",
        "animated_bio_frames": "Кадры анимации био",
    }

    def __init__(self):
        self.aname = False
        self.abio = False
        self.config = loader.ModuleConfig(
            loader.ConfigValue(
                "animated_name_frames",
                [],
                lambda: self.strings("animated_name_frames"),
                validator=loader.validators.Series(loader.validators.Union(loader.validators.String())),
            ),
            loader.ConfigValue(
                "name_delay",
                1.0,
                lambda: self.strings("name_delay"),
                validator=loader.validators.Float(),
            ),
            loader.ConfigValue(
                "animated_bio_frames",
                [],
                lambda: self.strings("animated_bio_frames"),
                validator=loader.validators.Series(loader.validators.Union(loader.validators.String())),
            ),
            loader.ConfigValue(
                "bio_delay",
                2.0,
                lambda: self.strings("bio_delay"),
                validator=loader.validators.Float(),
            ),
        )

    @loader.command(alias="aname")
    async def animatedname(self, message: Message):
        """(aname) Включить анимацию имени"""
        if not self.aname:
            await message.delete()
            while self.aname:
                if self.aname:
                    for n in self.config["animated_name_frames"]:
                        await asyncio.sleep(self.config["name_delay"])
                        await self.client(functions.account.UpdateProfileRequest(first_name=n))
                else:
                    return
                    break
        else:
            return await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени уже включена, используйте <code>.stopaname</code>, чтобы выключить.")


    @loader.command(alias="abio")
    async def animatedbio(self, message: Message):
        """(abio) Включить анимацию био"""
        if not self.abio:
            await message.delete()
            while self.abio:
                if self.abio:
                    for n in self.config["animated_bio_frames"]:
                        await asyncio.sleep(self.config["bio_delay"])
                        await self.client(functions.account.UpdateProfileRequest(about=n))
                else:
                    return
                    break
        else:
            return await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био уже включена, используйте <code>.stopabio</code>, чтобы выключить.")

    @loader.command(alias="astopname")
    async def animatedstopname(self, message: Message):
        """(astopname) Выключить анимацию"""
        if self.aname:
            return await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени уже выключена.")
        else:
            await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация имени выключена.")
            self.aname = False

    @loader.command(alias="astopbio")
    async def animatedstopbio(self, message: Message):
        """(astopbio) Выключить анимацию"""
        if self.abio:
            return await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био уже выключена.")
        else:
            await utils.answer(message, "<emoji document_id=5447644880824181073>⚠️</emoji> Анимация био выключена.")
            self.abio = False