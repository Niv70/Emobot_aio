# Модуль общих функций (Common functions)
# import aiogram
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
import datetime


# Ввод неотрицательного числа
async def get_digit(message: Message, state: FSMContext, d_min, d_max):  # d_min: int, d_max: int) -> aiogram.types.int:
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    try:
        d = int(message.text)  # проверяем, что цифра введена корректно
    except Exception as e:
        await message.answer('Ошибка: {0}'.format(e))
        await message.answer('{0}, введи цифрами, пожалуйста!'.format(name_user))
        d = -1
    else:
        if d < d_min or d > d_max:
            await message.answer('{0}, введи значение от {1} до {2}, пожалуйста!'.format(name_user, d_min, d_max))
            d = -2
    return d


# Определяем время до СЛЕДУЮЩЕГО действия в секундах (т.е. если пропустили что-то, то пропустили)
async def get_time_next_action(state: FSMContext) -> int:
    data = await state.get_data()  # Достаем имя пользователя
    tmz = data.get("tmz")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    period = data.get("period")
    tsk_t = data.get("tsk_t")
    c_data = datetime.datetime.now()
    c_time = c_data.time()
    c_time__hour = c_time.hour + tmz
    flag_pool = 1  # взводим флажок выполнения опроса
    flag_task = 0  # сбрасываем флажок выполнения задачи
    if c_time__hour >= end_t:  # рассчет времени задержки после завершения опроса в текущем дне
        t = ((24 - c_time__hour) * 3600 - c_time.minute * 60) + start_t * 3600
        if tsk_t == start_t:
            flag_task = 1
    elif c_time__hour < start_t:  # здесь окажемся если задержали ответ на последний опрос/задание
        t = (start_t - c_time__hour) * 3600 - c_time.minute * 60
        if tsk_t == start_t:
            flag_task = 1
    else:    # рассчет времени задержки в рамках опроса текущего дня
        p = period
        while c_time__hour >= start_t + p:  # находим час следующего опроса
            p = p + period
        # м.б. следующей должна выполняться задача? (+ м.б. опрос)
        if (start_t + p >= tsk_t) and (tsk_t > c_time__hour):
            t = (tsk_t - c_time__hour) * 3600 - c_time.minute * 60
            flag_task = 1  # взводим флажок выполнения задачи
            if start_t + p > tsk_t:
                flag_pool = 0  # опускаем флажок выполнения опроса
        elif start_t + p > end_t:  # вышли за время опроса из-за сокращенного последнего врменного отрезка
            t = (end_t - c_time__hour) * 3600 - c_time.minute * 60
        else:  # расчет задержки в рамках опроса без необходимости запуска задачи
            t = (start_t + p - c_time__hour) * 3600 - c_time.minute * 60
    await state.update_data(flag_pool=flag_pool)
    await state.update_data(flag_task=flag_task)
    return t+10  # запас надежности в 10 секунд
