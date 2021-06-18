from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
import datetime
from loader import dp

from typing import List
from utils.db_api.db_commands import db, db_update_current_day, db_update_user_settings
from utils.db_api.db_commands import stat_five_emotions
from aiogram.dispatcher import FSMContext


@dp.message_handler(Command("stat"), state='*')
async def bot_restart(message: types.Message):
    str0 = await stat_five_emotions(message.from_user.id)
    await message.answer(str0)


@dp.message_handler(Command("reset"), state=None)
async def set_c_day_0(message: types.Message):
    await db_update_user_settings(message.from_user.id, task_time=99)
    await message.answer("Бот перезапущен")


@dp.message_handler(Command("reset"), state='*')
async def set_c_day_0(message: types.Message):
    await message.answer("Нужно остановить ЗаБотик :)")


@dp.message_handler(Command("day01"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=1)
    await message.answer("Текущий день установлен в 1")


@dp.message_handler(Command("day02"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=2)
    await message.answer("Текущий день установлен в 2")


@dp.message_handler(Command("day03"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=3)
    await message.answer("Текущий день установлен в 3")


@dp.message_handler(Command("day04"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=4)
    await message.answer("Текущий день установлен в 4")


@dp.message_handler(Command("day05"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=5)
    await message.answer("Текущий день установлен в 5")


@dp.message_handler(Command("day06"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=6)
    await message.answer("Текущий день установлен в 6")


@dp.message_handler(Command("day07"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=7)
    await message.answer("Текущий день установлен в 7")


@dp.message_handler(Command("day08"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=8)
    await message.answer("Текущий день установлен в 8")


@dp.message_handler(Command("day09"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=9)
    await message.answer("Текущий день установлен в 9")


@dp.message_handler(Command("day10"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=10)
    await message.answer("Текущий день установлен в 10")


@dp.message_handler(Command("day11"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=11)
    await message.answer("Текущий день установлен в 11")


@dp.message_handler(Command("day12"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=12)
    await message.answer("Текущий день установлен в 12")


@dp.message_handler(Command("day13"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=13)
    await message.answer("Текущий день установлен в 13")


@dp.message_handler(Command("day14"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=14)
    await message.answer("Текущий день установлен в 14")


@dp.message_handler(Command("day15"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=15)
    await message.answer("Текущий день установлен в 15")


@dp.message_handler(Command("day16"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=16)
    await message.answer("Текущий день установлен в 16")


@dp.message_handler(Command("day17"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=17)
    await message.answer("Текущий день установлен в 17")


@dp.message_handler(Command("day18"), state=None)
async def set_c_day_x(message: types.Message):
    await db_update_current_day(message.from_user.id, current_day=18)
    await message.answer("Текущий день установлен в 18")
