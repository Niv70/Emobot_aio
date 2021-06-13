# Модуль общих функций (Common functions)
# import aiogram
from asyncio import sleep
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import datetime

from handlers.users.pool_mess import run_poll, run_poll_task
from handlers.users.task_mess import run_task
from loader import SEC_IN_H, SEC_IN_M, HOUR_IN_DAY, LAST_DAY
import logging


# Ввод неотрицательного числа
async def get_digit(message: Message, state: FSMContext, d_min: int, d_max: int):
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


# Бесконечный цикл действия ботика
async def loop_action(message: Message, state: FSMContext):
    t = await get_time_next_action(state, 1)  # первый запуск
    while True:
        data = await state.get_data()
        name_user = data.get("name_user")
        tmz = data.get("tmz")
        prev_data = data.get("prev_data")
        current_day = data.get("current_day")
        flag_pool = data.get("flag_pool")
        flag_task = data.get("flag_task")
        # тайм-аут до начала следующего действия
        logging.info('loop_action 0: засыпаю на {0} сек, prev_data={1} current_day='
                     '{2}'.format(t, prev_data, current_day))
        await sleep(t)
        # Рассчет и изменение номера текущего дня
        c_data = datetime.datetime.now() + datetime.timedelta(hours=tmz)
        if SEC_IN_H == 3600:  # Проверяем работаем ли мы по боевому или в режиме отладки
            c_day = c_data.day
        else:
            c_day = c_data.hour
        if c_day != prev_data:
            current_day = current_day + 1
            await state.update_data(current_day=current_day)
            prev_data = c_day
            await state.update_data(prev_data=prev_data)
            await message.answer('<code>------- начался {0}-й день опроса -------</code>'.format(current_day))
        logging.info('loop_action 1: c_day={0} prev_data={1} current_day={2}'.format(c_day, prev_data, current_day))
        if current_day > LAST_DAY:  # проверяем условие на завершение работы
            await run_bye(message, state)
        # Проверка закончил ли пользователь за тайм-аут с предыдущим опросом/задачей/настройкой (<-можно детализировать)
        c_state = await state.get_state()
        logging.info('loop_action 2: c_state={0}'.format(c_state))
        if c_state != "Start:Wait":
            await message.answer('{0}, я не могу больше ждать твоего ответа, т.к. пришло время следующего '
                                 'вопроса!'.format(name_user))
        # Запуск следующего действия и рассчет времени сна с установкой флагов
        logging.info('loop_action 3: flag_pool={0} flag_task={1}'.format(flag_pool, flag_task))
        if flag_pool and flag_task:
            await run_poll_task(message, state)  # запуск опроса с последующим запуском задачи
        elif flag_pool:
            await run_poll(message, state)  # запуск  одного опроса
        elif flag_task:  # можно было бы поставить else, но пусть для надежности будет так
            await run_task(message, state)  # запуск одной задачи
        t = await get_time_next_action(state, 0)


# Определяем время до следующего действия в секундах (т.е. если пропустили что-то, то пропустили)
async def get_time_next_action(state: FSMContext, flag: int) -> int:
    data = await state.get_data()  # Достаем имя пользователя
    tmz = data.get("tmz")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    period = data.get("period")
    tsk_t = data.get("tsk_t")
    c_data = datetime.datetime.now() + datetime.timedelta(hours=tmz)
    flag_pool = 1  # взводим флажок выполнения опроса
    flag_task = 0  # сбрасываем флажок выполнения задачи
    # Проверяем работаем ли мы по боевому или в режиме отладки
    if SEC_IN_H == 3600:
        c_hour = c_data.hour
        c_minute = c_data.minute
    else:
        c_hour = c_data.minute
        c_minute = c_data.second
    # обработка 1го вызова функции
    if flag:
        if SEC_IN_H == 3600:  # инициализируем prev_data
            prev_data = c_data.day
        else:
            prev_data = c_data.hour
        await state.update_data(prev_data=prev_data)
        if c_hour < start_t:  # настройки завершены сегодня до наступления начала опроса
            t = (start_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
            await state.update_data(current_day=1)  # считаем,что пошел 1й день опроса
        else:  # настройки завершены после наступления начала опроса - выполнение опроса начнется завтра
            t = ((HOUR_IN_DAY - c_hour) * SEC_IN_H - c_minute * SEC_IN_M) + start_t * SEC_IN_H
        if tsk_t == start_t:
            flag_task = 1
            await state.update_data(flag_task=flag_task)  # взводим флажок выполнения задачи
        logging.info('g_t_n_a 0: c_hour={0} c_minute={1} start_t={2} prev_data={3} flag_task={4} t='
                     '{5}'.format(c_hour, c_minute, start_t, prev_data, flag_task, t))
        return t+10  # запас надежности в 10 секунд
    # обработка вызова функции из цикла действий
    if c_hour >= end_t:  # рассчет времени задержки после завершения опроса в текущем дне
        t = ((HOUR_IN_DAY - c_hour) * SEC_IN_H - c_minute * SEC_IN_M) + start_t * SEC_IN_H
        if tsk_t == start_t:
            flag_task = 1
    elif c_hour < start_t:  # никогда не должно выполниться (раньше- выполнится если задержали ответ на последний опрос)
        t = (start_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
        if tsk_t == start_t:
            flag_task = 1
        logging.info('g_t_n_a 1: !!_ЧУШЬ_!! c_hour={0} c_minute={1} start_t={2} flag_task={3} t='
                     '{4}'.format(c_hour, c_minute, start_t, flag_task, t))
    else:    # рассчет времени задержки в рамках опроса текущего дня
        p = period
        while c_hour >= start_t + p:  # находим час следующего опроса
            p = p + period
        # м.б. следующей должна выполняться задача? (+ м.б. без опроса?) - помним, что tsk_t <= end_t
        if (start_t + p >= tsk_t) and (tsk_t > c_hour):
            t = (tsk_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
            flag_task = 1  # взводим флажок выполнения задачи
            if start_t + p > tsk_t:
                flag_pool = 0  # опускаем флажок выполнения опроса
        elif start_t + p > end_t:  # вышли за время опроса из-за сокращенного последнего врменного отрезка
            t = (end_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
        else:  # расчет задержки в рамках опроса без необходимости запуска задачи
            t = (start_t + p - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
    await state.update_data(flag_pool=flag_pool)
    await state.update_data(flag_task=flag_task)
    logging.info('g_t_n_a 2: c_hour={0} c_minute={1} start_t={2} end_t={3} flag_pool={4} flag_task={5} t='
                 '{6}'.format(c_hour, c_minute, start_t, end_t, flag_pool, flag_task, t))
    return t+10  # запас надежности в 10 секунд


# Штатное завершение работы бота
async def run_bye(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    sti = open("./a_stickers/AnimatedSticker2.tgs", 'rb')  # Приветствует воздушным поцелуем
    await message.answer_sticker(sticker=sti)
    await message.answer("Мы полезно с тобой пообщались, {0}! До новых встреч"
                         "!".format(name_user), reply_markup=ReplyKeyboardRemove())
    await state.reset_state()  # для сохранения данных в data можно писать await state.reset_state(with_data=False)
    # TODO д.б. добавлена команда по выводу статистики из БД
    logging.info("run_bye 0: Бот пользователя {0}(id={1}) штатно завершил работу. "
                 "current_day={2}".format(name_user, message.from_user.id, current_day))
