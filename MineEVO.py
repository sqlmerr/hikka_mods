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
# .mevoprofile | .mevocases | .mevoperevod | .mevomine | .mevoautobonus | .mevoautothx 
# ---------------------------------------------------------------------------------------------

# версия модуля
__version__ = (0, 5, 4)
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
class MineEVO(loader.Module):
    """Полезный модуль для бота @mine_evo_bot"""
    # нужные переменные
    strings = {
        "name": "MineEVO",
        "mine_interval": "Интервал копания",
        "mine_status": "Ну тип копаете вы или нет",
        "perevod_interval": "Интервал перевода лимитов",
        "perevod_status": "Ну тип переводите вы лимиты или нет",
        "autobonus_status": "Получаете ли вы автоматически ежедневный бонус или нет",
        "autopromo_status": "Пишите ли вы автоматически промо или нет",
        "autothx_status": "Пишите ли вы автоматически Thx или нет",
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
                "perevod_status",
                False,
                lambda: self.strings("perevod_status"),
                validator=loader.validators.Boolean()
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
        )
    # .mevoprofile
    @loader.command()
    async def mevoprofile(self, message: Message):
        """отправляет в текущий чат ваш профиль в боте @mine_evo_bot"""
        await utils.answer(message, 'Выполняю...')
        # юб начинает диалог в чате с ассетами который создаётся автоматически
        async with self._client.conversation(self._mineevo_channel) as conv:
            await conv.send_message('профиль')
            # получаем ответ
            response = await conv.get_response()
        links_regex = re.compile(r'.(https?://\S+).')
        response.text = links_regex.sub('', response.text)
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.text)
        for l in links:
            # заменяем ссылку в тексте ответа на @sqlmerr_m :)
            response.text = response.text.replace(link, '@sqlmerr_m')
        # выдаём пользователю
        await utils.answer(message, response.text)
    # .mevocases
    @loader.command()
    async def mevocases(self, message: Message):
        """отправляет в текущий чат ваши кейсы в боте @mine_evo_bot"""
        await utils.answer(message, 'Выполняю...')
        # юб начинает диалог в чате с ассетами который создаётся автоматически
        async with self._client.conversation(self._mineevo_channel) as conv:
            await conv.send_message('кейсы')  # upload step
            response = await conv.get_response() # first message
            # получаем ответ
        links_regex = re.compile(r'.(https?://\S+).')
        response.text = links_regex.sub('', response.text)
        links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', response.text)
        for l in links:
            # заменяем ссылку в тексте ответа на @sqlmerr_m :)
            response.text = response.text.replace(link, '@sqlmerr_m')
        # выдаём пользователю
        await utils.answer(message, response.text)
    # .mevomine
    @loader.command()
    async def mevomine(self, message: Message):
        """Автоматически копает за вас"""
        if not self.config["mine_status"]:
            # если в конфиге параметр mine_status имеет значение False, то функция не выполняется дальше
            await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> mine_status -> Измените False на True")
            return
        # получаем интервал копания из конфига
        interval = self.config["mine_interval"]

        logger.debug("start mining...")
        await utils.answer(message, 'Копаю ⛏')
        # юб копает за вас
        while self.config["mine_status"]:
            if self.config["mine_status"]:
                await self.client.send_message("@mine_evo_bot", "коп")
                await asyncio.sleep(interval)
            else:
                await self.client.send_message(self._mineevo_channel, "Вы остановили майнинг!")
                return

    # .mevoperevod <кол-во лимитов> <ник чела в боте>
    @loader.command()
    async def mevoperevod(self, message: Message):
        """.mevoperevod <кол-во лимитов> <ник чела в боте> - Автоматически переводит лимиты за вас"""
        if not self.config["perevod_status"]:
            # если в конфиге параметр mine_status имеет значение False, то функция не выполняется дальше
            await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> perevod_status -> Измените False на True. Это сделано для защиты от случайных переводов")
            return
        interval = self.config["perevod_interval"]
        # получаем аргументы
        args = utils.get_args_raw(message).split()
        
        # если аргументов нет
        if not args:
            utils.answer(message, 'ошибка')
            return

        logger.debug("starting to transfer limits...")
        await utils.answer(message, 'Начинаю переводить лимиты')
        # юб переводит лимиты
        if self.config["perevod_status"]:
            for i in range(int(args[0])):
                if self.config["perevod_status"]:
                    await self.client.send_message("@mine_evo_bot", f"Перевести {args[1]} лимит")
                    await asyncio.sleep(interval)
                else:
                    await self.client.send_message(self._mineevo_channel, "Вы остановили перевод лимитов!")
                    return
            # и по завершению, отправляется сообщение, в котором говорится, что все лимиты переведены
            await self.client.send_message(chat=self._mineevo_channel, message='Все лимиты переведены!')

    # .mevoautobonus
    @loader.command()
    async def mevoautobonus(self, message: Message):
        """автоматически забирает ежедневный бонус"""
        if not self.config["autobonus_status"]:
            await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> autobonus_status -> Измените False на True.")
            return
        await utils.answer(message, 'Начинаю авто-сбор ежедневных бонусов!')
        while self.config["autobonus_status"]:
        	if self.config["autobonus_status"]:
        		await self.client.send_message(self._mineevo_channel, "еб")
        		await asyncio.sleep(86400)

    # .mevoautothx
    @loader.command()
    async def mevoautothx(self, message: Message):
        """автоматически пишет thx"""
        if not self.config["autothx_status"]:
            return await utils.answer(message, "Поставьте <code>True</code> в конфиге модуля! Для этого напишите команду .config -> Внешние -> MineEVO -> autothx_status -> Измените False на True.")
        while True:
            if self.config["autothx_status"]:
                await utils.answer(message, "Начинаю авто-thx")
                async with self._client.conversation(self._mineevo_channel) as conv:
                    a = await conv.send_message('thx')
                    # получаем ответ
                    b = await conv.get_response()
                    list_msgs_id = [a.id, b.id]

                if 'благодарить некого.' in b.text:
                    await self.client.delete_messages(entity=self._mineevo_channel, message_ids=list_msgs_id)
                elif 'этого игрока за глобальный бустер!' in b.text:
                    await self.client.delete_messages(entity=self._mineevo_channel, message_ids=list_msgs_id)
                await asyncio.sleep(3600)
            else:
                return await self.client.send_message(self._mineevo_channel, 'Вы остановили авто-thx')


    # auto-promo (idea: https://t.me/Demchik347)
    @loader.watcher(only_messages=True, from_id=-1001951702424)
    async def watcher(self, message: Message):
        if not self.config["autopromo_status"]:
            return
        if "Этот промокод был сгенерирован ботом" in message.text and "Пиши в боте:" in message.text:
            promo_start = message.text.index("Промо ") + len("Промо ") # находим начало промокода
            promo_end = message.text.index("\n", promo_start) # находим конец промокода
            promo_code = message.text[promo_start:promo_end] # извлекаем код из сообщения
            await self.client.send_message(self._mineevo_channel, f'Промо {promo_code}')

            logger.debug("было введено промо")
        else:
            await self.client.send_message(self._mineevo_channel, message.text)
