from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Запустить бота",
            "/help - Получить справку",
            "/stop - Остановить бота",
            "/stat - Статистика по зафиксированным эмоциям")
    await message.answer("\n".join(text))
