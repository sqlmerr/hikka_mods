# ░██████╗░██████╗░██╗░░░░░███╗░░░███╗███████╗██████╗░██████╗░
# ██╔════╝██╔═══██╗██║░░░░░████╗░████║██╔════╝██╔══██╗██╔══██╗
# ╚█████╗░██║██╗██║██║░░░░░██╔████╔██║█████╗░░██████╔╝██████╔╝
# ░╚═══██╗╚██████╔╝██║░░░░░██║╚██╔╝██║██╔══╝░░██╔══██╗██╔══██╗
# ██████╔╝░╚═██╔═╝░███████╗██║░╚═╝░██║███████╗██║░░██║██║░░██║
# ╚═════╝░░░░╚═╝░░░╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚═╝
# ---------------------------------------------------------------------------------------------
# Name: MineEVO
# Description: Полезный модуль для бота @mine_evo_bot
# Author: sqlmerr
# Commands:
# .mprofile | .mcases | .mperevod | .mmine | .mautobonus | .mautopromo | .mautothx | .mautosell
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (1, 0, 2)
# meta developer: @sqlmerr_m
# meta banner: https://github.com/sqlmerr/hikka_mods/blob/main/mineevo.png
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
class MineEVO(loader.Module):
    """Полезный модуль для бота @mine_evo_bot"""
    # нужные переменные
    strings = {
        "name": "MineEVO",
        "lvl": "Ваш уровень",
        "mine_interval": "⏳ Интервал копания",
        "mine_status": "⚙️ Ну тип копаете вы или нет",
        "perevod_interval": "⏳ Интервал перевода лимитов",
        "autobonus_status": "⚙️ Получаете ли вы автоматически ежедневный бонус или нет",
        "autopromo_status": "⚙️ Пишите ли вы автоматически промо или нет",
        "autothx_status": "⚙️ Пишите ли вы автоматически Thx или нет",
        "autosell_status": "⚙️ Продаете ли вы руду или нет",
        "autoboost_status": "⚙️ Используете ли вы буст денег 1.5 во время авто-продажи или нет",
    }
    # когда клиент готов к работе:
    async def client_ready(self):
        # создается чат
        self._mineevo_channel, _ = await utils.asset_channel(
            self._client,
            "MineEVO - чат",
            "Не пишите сюда. Этот чат предназначет для модуля MineEVO от @sqlmerr_m",
            silent=True,
            archive=True,
            _folder="hikka",
        )
        # в этот чат добавляется бот @mine_evo_bot
        await self.client(functions.channels.InviteToChannelRequest(self._mineevo_channel, ['@mine_evo_bot']))
        # и этому боту выдаются права админа, для корректной работы бота
        await self.client(functions.channels.EditAdminRequest(
                channel=self._mineevo_channel,
                user_id="@mine_evo_bot",
                admin_rights=ChatAdminRights(ban_users=True, post_messages=True, edit_messages=True),
                rank="MineEVO",
            )
        )




    # функция, связанная с ООП и нужная для создания конфига
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
                "autobonus_status",
                False,
                lambda: self.strings("autobonus_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autopromo_status",
                True,
                lambda: self.strings("autopromo_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autothx_status",
                False,
                lambda: self.strings("autothx_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autosell_status",
                False,
                lambda: self.strings("autosell_status"),
                validator=loader.validators.Boolean()
            ),
            loader.ConfigValue(
                "autoboost_status",
                False,
                lambda: self.strings("autoboost_status"),
                validator=loader.validators.Boolean()
            ),
        )
    # .mprofile
    @loader.command()
    async def mprofile(self, message: Message):
        """отправляет в текущий чат ваш профиль в боте @mine_evo_bot"""
        await utils.answer(message, '<emoji document_id=5451882707875276247>🕯</emoji> Выполняю...')
        # юб начинает диалог в чате с ассетами который создаётся автоматически
        async with self._client.conversation(self._mineevo_channel) as conv:
            await conv.send_message('профиль')
            # получаем ответ
            response = await conv.get_response()
        # пересылаем ответ
        await response.forward_to(message.to_id)
        await message.delete()
    # .mcases
    @loader.command()
    async def mcases(self, message: Message):
        """отправляет в текущий чат ваши кейсы в боте @mine_evo_bot"""
        await utils.answer(message, '<emoji document_id=5451882707875276247>🕯</emoji> Выполняю...')
        # юб начинает диалог в чате с ассетами который создаётся автоматически
        async with self._client.conversation(self._mineevo_channel) as conv:
            await conv.send_message('кейсы')  # upload step
            response = await conv.get_response() # first message
            # получаем ответ
        # пересылаем ответ
        await response.forward_to(message.to_id)
        await message.delete()
    # .mmine
    @loader.command()
    async def mmine(self, message: Message):
        """Автоматически копает за вас"""
        self.config["mine_status"] = not self.config["mine_status"]
        status = (
            "Копаю <emoji document_id=5282855481121976759>⛏</emoji>"
            if self.config["mine_status"]
            else "Больше не копаю <emoji document_id=5282855481121976759>⛏</emoji>"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-майна:\n <b>{}</b>".format(status))

        if self.config["mine_status"]:
            interval = self.config["mine_interval"]

            logger.debug("start mining...")
            # юб копает за вас
            while self.config["mine_status"]:
                if self.config["mine_status"]:
                    await self.client.send_message("@mine_evo_bot", "коп")
                    await asyncio.sleep(interval)
                else:
                    return
                    break
        else:
            return

    # .mperevod <кол-во лимитов> <ник чела в боте>
    @loader.command()
    async def mperevod(self, message: Message):
        """ <кол-во лимитов> <ник чела в боте> - Автоматически переводит лимиты за вас"""
        autoperevod = False
        autoperevod = not autoperevod
        status = (
            "<emoji document_id=5309799327093236710>🫥</emoji> Начинаю переводить лимиты"
            if autoperevod
            else "<emoji document_id=5307675706283533118>🫥</emoji> Авто-перевод выключен"
        ) 

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-перевода:\n <b>{}</b>".format(status))

        if autoperevod:
            interval = self.config["perevod_interval"]
            # получаем аргументы
            args = utils.get_args_raw(message).split()
            
            # если аргументов нет
            if not args:
                await utils.answer(message, 'введите аргументы: .mperevod <кол-во лимитов> <ник чела в боте>')
                return
            limits = int(args[0])

            async with self._client.conversation(self._mineevo_channel) as conv:
                a = await conv.send_message(f"Перевести {args[1]} лимит")

                b = await conv.get_response()
                list_msgs_id = [a.id, b.id]

            if "перевел(а) игроку" in b.text:
                await self.client.delete_messages(entity=self._mineevo_channel, message_ids=list_msgs_id)
            else:
                await utils.answer(message, f"<emoji document_id=5447644880824181073>⚠️</emoji> Произошла ошибка:\n\n{b.text}")
                return await self.client.delete_messages(entity=self._mineevo_channel, message_ids=list_msgs_id)

            logger.debug("starting to transfer limits...")
            # юб переводит лимиты
            while limits > 0:
                if autoperevod:
                    limits -= 1
                    
                    await self.client.send_message("@mine_evo_bot", f"Перевести {args[1]} лимит")
                    await asyncio.sleep(interval)
                else:
                    await self.client.send_message(self._mineevo_channel, "Вы остановили перевод лимитов!")
                    return
                    break
            await self.client.send_message(self._mineevo_channel, f'<emoji document_id=5447644880824181073>⚠️</emoji> Все лимиты переведены!\n\n<emoji document_id=5210956306952758910>👀</emoji> Кому: <code>{args[1]}</code>  |  <emoji document_id=5456140674028019486>⚡️</emoji> Сколько: <b>{args[0]}</b>')
        else:
            return

    # .mautobonus
    @loader.command()
    async def mautobonus(self, message: Message):
        """автоматически забирает ежедневный бонус"""
        self.config["autobonus_status"] = not self.config["autobonus_status"]
        status = (
            "<emoji document_id=5416081784641168838>🟢</emoji> Авто-еб включено"
            if self.config["autobonus_status"]
            else "<emoji document_id=5411225014148014586>🔴</emoji> Авто-еб выключено"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-еб:\n <b>{}</b>".format(status))

        if self.config["autobonus_status"]:
            while self.config["autobonus_status"]:
                if self.config["autobonus_status"]:
                    await self.client.send_message(self._mineevo_channel, "еб")
                    await asyncio.sleep(86400)
                else:
                    return
                    break
        else:
            return
    # .mautothx
    @loader.command()
    async def mautothx(self, message: Message):
        """автоматически пишет thx"""
        self.config["autothx_status"] = not self.config["autothx_status"]
        status = (
            "Авто-thx включено"
            if self.config["autothx_status"]
            else "Авто-thx выключено"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-thx:\n <b>{}</b>".format(status))

    # .mautopromo
    @loader.command()
    async def mautopromo(self, message: Message):
        """Включить/выключить авто-промо"""
        self.config["autopromo_status"] = not self.config["autopromo_status"]
        status = (
            "<emoji document_id=5424972470023104089>🔥</emoji> Авто-промо включено"
            if self.config["autopromo_status"]
            else "<emoji document_id=5424972470023104089>🔥</emoji> Авто-промо выключено"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-промо:\n <b>{}</b>".format(status))


    # auto-promo (idea: https://t.me/Demchik347), autothx
    @loader.watcher(only_messages=True)
    async def watcher(self, message: Message):
        if self.config["autopromo_status"] and message.chat_id == -1001892345917:
            promo_start = message.text.index("Промо ") + len("Промо ") # находим началопромокода
            promo_end = message.text.index("\n", promo_start) # находим конец промокода
            promo_code = message.text[promo_start:promo_end] # извлекаем код из сообщения
            await self.client.send_message(self._mineevo_channel, f'Промо {promo_code}')

            logger.debug("было введено промо")
        elif message.chat_id == 5522271758 and "(Используй команду Thx чтобы поблагодарить и получить бонус)" in message.raw_text:
            if self.config["autothx_status"]:
                self.client.send_message(self._mineevo_channel, "thx")




    # .mautosell
    @loader.command()
    async def mautosell(self, message: Message):
        """Включить/выключить авто-продажу"""
        self.config["autosell_status"] = not self.config["autosell_status"]
        status = (
            "<emoji document_id=5409048419211682843>💲</emoji> Авто-продажа включена"
            if self.config["autosell_status"]
            else "<emoji document_id=5409048419211682843>💲</emoji> Авто-продажа выключена"
        )

        await utils.answer(message, "<emoji document_id=5314346928660554905>⚠️</emoji> Статус авто-продажи:\n <b>{}</b>".format(status))
        self.config["autosell_status"]
        if self.config["autosell_status"]:
            while self.config["autosell_status"]:
                if self.config["autosell_status"]:
                    async with self._client.conversation(self._mineevo_channel) as conv:
                        if self.config["autoboost_status"]:
                            o = await conv.send_message("буст д 1.5")
                            oo = await conv.get_response()
                        a = await conv.send_message('инв')
                        # получаем ответ
                        b = await conv.get_response()
                        list_msgs_id = [a.id, b.id]
                    await b.click(0)
                    await asyncio.sleep(605)
                    await self.client.delete_messages(entity=self._mineevo_channel, message_ids=list_msgs_id)
                else:
                    return
                    break
        else:
            return

