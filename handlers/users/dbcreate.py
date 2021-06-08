from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from loader import dp

from typing import List
from sqlalchemy import and_
from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db, create_db


@dp.message_handler(Command("dbcreate"), state='*')
async def bot_restart(message: types.Message):
    await message.answer("DBCREATE")
    await create_db()
