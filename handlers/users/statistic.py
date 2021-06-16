from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
import datetime
from loader import dp

from typing import List
from sqlalchemy import and_
from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.db_commands import db, db_update_user_settings
from utils.db_api.db_commands import stat_five_emotions
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command("stat"), state='*')
async def bot_restart(message: types.Message):
    str0 = await stat_five_emotions(message.from_user.id)
    await message.answer(str0)


@dp.message_handler(Command("reset"), state=None)
async def set_c_day_0(message: types.Message):
    await db_update_user_settings(message.from_user.id, task_time=99)


@dp.message_handler(Command("reset"), state='*')
async def set_c_day_0(message: types.Message):
    await message.answer("Нужно остановить ЗаБотик :)")


# Устанавливает current_day равным текущей минуте
@dp.message_handler(Command("setday"), state=None)
async def set_c_day_x(message: types.Message):
    c_data = datetime.datetime.now()
    x = c_data.minute
    if x > 40:
        x = x - 40
    elif x > 20:
        x = x - 20
    if x > 18:
        x = 18
    # TODO нужна отдельная команда на запись только current_day
    # await db_update_user_settings(message.from_user.id, current_day=x)


@dp.message_handler(Command("setday"), state='*')
async def set_c_day_x(message: types.Message):
    await message.answer("Нужно остановить ЗаБотик :)")
