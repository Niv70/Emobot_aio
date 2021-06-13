# В этом модуле выполняется обработка сообщений в состоянии Задача (Task)
# from aiogram import types
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from states.states import Start, Task
from utils.db_api.db_commands import db_save_task


# ============================== Запуск задач текущего дня ==============================
async def run_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    # начинаем опрос
    if current_day != 1:  # and current_day != x
        sti = open("./a_stickers/AnimatedSticker4.tgs", 'rb')  # Пускает праздничный салют
        await message.answer_sticker(sticker=sti)
        await message.answer('{0}! Наступил час потехи - начинаем задачку "на прокачку"!'.format(name_user))
        logging.info("run_task 0: current_day={0}".format(current_day))
    if current_day == 2:  # на 2-й (не на 0-й и 1-й) день работы боты запускаем задачи
        await run_tsk2(message, state)
    # elif current_day == 3:
    #     await run_tsk3(message, state)
    # elif current_day == 4:
    #     await run_tsk4(message, state)
    else:  # переходим в состояние ожидания следующего действия
        sti = open("./a_stickers/AnimatedSticker8.tgs", 'rb')  # Идет с закрытыми глазами по беговой дорожке
        await message.answer_sticker(sticker=sti)
        await message.answer('{0}, для {1} нет задачку "на прокачку" - можешь просто легонько помедитировать... :)'
                             '...'.format(name_user, current_day))
        await Start.Wait.set()


# ============================== Запуск задачки "на прокачку" 2-го дня ==============================
async def run_tsk2(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer("Приветствую тебя {0} на 1м этапе выполнения задачи 2-го дня".format(name_user))
    await message.answer("{0}, пожалуйста, напиши <b><i>Привет_1</i></b>".format(name_user))
    await Task.Answer_02_01.set()  # Здесь д.б. 02_01. Написал 02_05 просто для демонстрации


# Обработчик ввода 1го ответа к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task.Answer_02_01)
async def answer_02_01(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s.lower() != "привет_1":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Привет_1</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, data.get("current_day"), s)
    logging.info("answer_02_01 0: Пользователь {0}(id={1}) ввел ответ: {2}".format(name_user, message.from_user.id, s))
    await message.answer("Еще раз, приветствую тебя, {0}, на 5м этапе выполнения задачи 2-го дня".format(name_user))
    await message.answer("{0}, пожалуйста, напиши <b><i>Привет_2</i></b>".format(name_user))
    await Task.Answer_02_05.set()  # Здесь д.б. 02_02. Написал 02_05 просто для демонстрации


# Обработчик ввода 5го ответа к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task.Answer_02_05)
async def answer_02_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s.lower() != "привет_2":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Привет_2</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, data.get("current_day"),  s)
    await message.answer("Спасибо, {0}, информация сохранена.".format(name_user))
    logging.info("answer_02_05 0: Пользователь {0}(id={1}) ввел ответ: {2}".format(name_user, message.from_user.id, s))
    await Start.Wait.set()


# ============================== Запуск задачки "на прокачку" N-го дня ==============================
