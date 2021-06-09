# В этом модуле выполняется обработка сообщений в состоянии Задача (Task)
from asyncio import sleep
# from aiogram import types
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from states.states import Pool, Task
from utils.common_func import get_time_next_action
from .pool_mess import run_poll


# Запуск опроса по задаче
async def run_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    # c_state = await state.get_state()
    # начинаем опрос
    sti = open("./a_stickers/AnimatedSticker4.tgs", 'rb')  # Пускает праздничный салют
    await message.answer_sticker(sticker=sti)
    await message.answer('{0}! Наступил час потехи - а именно задачки "на прокачку"!'.format(name_user))
    if current_day == 2:  # на 2-й (не на 0-й и 1-й) день работы боты запускаем задачи
        await run_tsk2(message, state)
    # elif current_day == 3:
    #     await run_tsk3(message, state)
    # elif current_day == 4:
    #     await run_tsk4(message, state)
    else:  # Если для этого дня (например, для 1-го) не была определена задача
        t = get_time_next_action(state)
        logging.info("run_task 0: засыпаю на {0} сек.".format(t))
        await Pool.Wait.set()
        await sleep(t)
        await run_poll(message, state)  # вызов функции опроса


# Запуск задачки "на прокачку" 2-го дня
async def run_tsk2(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer("Приветствую тебя {0} на этапе выполнения задачи 2-го дня".format(name_user))
    await message.answer("{0}, пожалуйста, напиши <b><i>Привет!!</i></b>".format(name_user))
    await Task.Answer_02_05.set()  # Здесь д.б. 02_01. Написал 02_05 просто для демонстрации


# Обработчик ввода эмоции
@dp.message_handler(state=Task.Answer_02_05)
async def answer_02_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s.lower() != "привет!!":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Привет!!</i></b>".format(name_user))
        return
    # !!! Добавить запись настроек в БД
    # !!!!! bd_save_task_answer(s, state)
    logging.info("answer_02_05 0: Пользователь {0}(id={1}) ввел ответ: {2}".format(name_user, message.from_user.id, s))
    t = get_time_next_action(state)
    logging.info('answer_02_05 1: засыпаю на {0}'.format(t))
    await Pool.Wait.set()
    await sleep(t)
    await run_poll(message, state)  # вызов функции опроса
