import asyncio
import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from states.states import Start
from utils.common_func import loop_action
from utils.db_api.db_commands import get_name_by_id
from handlers.users.start_mess import user_settings_from_db
from keyboards.default import menu


# Обработка первого вызова команды /start
@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message, state: FSMContext):
    str0 = await get_name_by_id(message.from_user.id)
    # Для удобства использования задаем локальные для модуля переменные
    help_m = "При ответах на вопрос боту регистр букв неважен.\n" \
             "!!ВАЖНО: Для продолжения работы после использования команды, следует ответить на заданный ранее вопрос."
    await message.answer(help_m, reply_markup=ReplyKeyboardRemove())
    sti = open("./a_stickers/AnimatedSticker9.tgs", 'rb')  # Подмигивает, снимая очки
    await message.answer_sticker(sticker=sti)
    if str0 is None:
        await message.answer("Привет! Как тебя зовут?")
        await Start.set_user_name.set()  # или можно await Start.first()
    else:
        await user_settings_from_db(message, state)
        data = await state.get_data()
        tsk_t = data.get("tsk_t")
        if tsk_t > 90:
            await message.answer("Привет! Как тебя зовут?")
            await Start.set_user_name.set()  # или можно await Start.first()
            return
        await message.answer("Привет! Рад еще раз видеть тебя, {0}! Твои настройки восстановлены из БД - опрос начнется"
                             " с наступлением следующего дня.".format(str0), reply_markup=menu)
        await Start.Wait.set()  # это состояние не имеет обработчиков - все сообщения "не команды" попадают в Эхо
        task_loop_action = asyncio.create_task(loop_action(message, state))
        name_task = task_loop_action.get_name()
        await state.update_data(name_task=name_task)
        data = await state.get_data()
        logging.info('bot_start 0: data={}'.format(data))
        await task_loop_action  # ждем завершения бесконечного цикла действий


# Обработка повторного вызова команды /start
@dp.message_handler(CommandStart(), state='*')
async def bot_restart(message: types.Message):
    await message.answer("ЗаБотик уже работает :)")
