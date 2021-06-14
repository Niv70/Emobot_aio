from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
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
async def set_c_day_0(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, task_time=99)


@dp.message_handler(Command("reset"), state='*')
async def set_c_day_0(message: types.Message):
    await message.answer("Нужно остановить ЗаБотик :)")
