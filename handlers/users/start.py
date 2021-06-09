from aiogram import types
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from states.states import Start


# Обработка первого вызова команды /start
@dp.message_handler(Command("start"), state=None)
async def bot_start(message: types.Message):
    # TODO Добавить проверку существования пользователя в БД и, если он есть, инициализацию переменных или сейчас
    #  это делается из FSM.json файла?
    # Для удобства использования задаем лкальные для модуля переменные
    help_m = "При ответах на вопрос боту регистр букв неважен.\n" \
             "!!ВАЖНО: Для продолжения работы после использования команды, селдует ответить на заданный ранее вопрос."
    await message.answer(help_m)
    sti = open("./a_stickers/AnimatedSticker9.tgs", 'rb')  # Подмигивает, снимая очки
    await message.answer_sticker(sticker=sti)
    await message.answer("Привет! Я - ЗаБотик - заботливый и веселый Телеграм-бот. А тебя как зовут?")
    await Start.set_user_name.set()  # или можно await Start.first()


# Обработка повторного вызова команды /start
@dp.message_handler(Command("start"), state='*')
async def bot_restart(message: types.Message):
    await message.answer("ЗаБотик уже работает :)")
