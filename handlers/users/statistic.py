from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp

from typing import List
from sqlalchemy import and_
from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.db_commands import db
from utils.db_api.db_commands import stat_five_emotions

@dp.message_handler(Command("stat"), state='*')
async def bot_restart(message: types.Message):
    str0 = await stat_five_emotions(message.from_user.id)
    await message.answer(str0)
