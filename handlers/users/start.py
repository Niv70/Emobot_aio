import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from states.states import Start
from utils.db_api.db_commands import db_add_user, get_name_by_item


# Обработка первого вызова команды /start
@dp.message_handler(Command("start"), state=None)
async def bot_start(message: types.Message):
    # TODO Добавить проверку существования пользователя в БД и, если он есть, инициализацию переменных или сейчас
    str0 = await get_name_by_item(message.from_user.id)
    #  это делается из FSM.json файла?
    # Для удобства использования задаем локальные для модуля переменные
    help_m = "При ответах на вопрос боту регистр букв неважен.\n" \
             "!!ВАЖНО: Для продолжения работы после использования команды, следует ответить на заданный ранее вопрос."
    await message.answer(help_m)
    sti = open("./a_stickers/AnimatedSticker9.tgs", 'rb')  # Подмигивает, снимая очки
    await message.answer_sticker(sticker=sti)
    if str0 is None:
        await message.answer("Привет! Я - ЗаБотик - заботливый и веселый Телеграм-бот. А тебя как зовут?")
        await Start.set_user_name.set()  # или можно await Start.first()
    else:
        await message.answer(
            "Привет! Я - ЗаБотик - заботливый и веселый Телеграм-бот.\n Рад еще раз видеть тебя ".format(str0))
        await Start.from_db_user_name.set()


# Обработка повторного вызова команды /start
@dp.message_handler(Command("start"), state='*')
async def bot_restart(message: types.Message):
    await message.answer("ЗаБотик уже работает :)")
