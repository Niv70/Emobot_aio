# В этом модуле выполняется обработка сообщений в состоянии Задача (Task)
# from aiogram import types
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from states.states import Task


# Запуск задачки "на прокачку" 2-го дня
async def run_tsk2(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer("Приветствую тебя {0} на этапе выполнения задачи 2-го дня".format(name_user))
    await message.answer("{0}, пожалуйста, напиши <b><i>Привет_1</i></b>".format(name_user))
    await Task.Answer_02_01.set()  # Здесь д.б. 02_01. Написал 02_05 просто для демонстрации


# Обработчик ввода ПОСЛЕДНЕГО ответа к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task.Answer_02_01)
async def answer_02_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s.lower() != "привет_1":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Привет_1</i></b>".format(name_user))
        return
    # TODO Добавить запись ответа на задачу БД bd_save_task_answer(...s)
    await message.answer("Еще раз, приветствую тебя, {0}, на этапе выполнения задачи 2-го дня".format(name_user))
    await message.answer("{0}, пожалуйста, напиши <b><i>Привет_2</i></b>".format(name_user))
    await Task.Answer_02_05.set()  # Здесь д.б. 02_02. Написал 02_05 просто для демонстрации
