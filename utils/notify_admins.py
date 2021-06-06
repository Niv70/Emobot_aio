import logging
# from aiogram import types
from aiogram import Dispatcher

from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "АДМИНу: Бот Запущен")
        except Exception as err:
            logging.exception(err)


async def on_notify(dp: Dispatcher, text: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "АДМИНу: " + text)
        except Exception as err:
            logging.exception(err)
