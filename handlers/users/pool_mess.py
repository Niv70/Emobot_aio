# В этом модуле выполняется обработка сообщений в состоянии Опроса (Pool)
from asyncio import sleep
# from aiogram import types
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
from random import choice
import logging
import datetime

from loader import dp
from states.states import Pool, Task
from utils.common_func import get_time_next_action
from .task_mess import run_tsk2


# Запуск опроса эмоции
async def run_poll(message: Message, state: FSMContext):
    quest = [", что ты сейчас чувствуешь?", ", какая эмоция сейчас внутри тебя?",
             ", прислушайся какая эмоция сейчас внутри тебя?", ", тук-тук-тук, что ты сейчас чувствуешь?"]
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    prev_data = data.get("prev_data")
    current_day = data.get("current_day")
    c_state = await state.get_state()
    # рассчет и изменение номера текущего дня
    c_data = datetime.datetime.now()
    logging.info('run_poll 0: c_data.day={0} prev_data={1} current_day={2} c_state='
                 '{3}'.format(c_data.day, prev_data, current_day, c_state))
    if c_data.day != prev_data:
        current_day = current_day + 1
        await state.update_data(current_day=current_day)
        await state.update_data(current_day=c_data.day)
    logging.info('run_poll 1: c_data.day={0} prev_data={1} current_day={2}'.format(c_data.day, prev_data, current_day))
    if current_day > 15:
        await run_bye(message, state)
    if c_state is not Pool.Wait:
        await message.answer('{0}! Текущее действие прервано из-за наступления времени очередного '
                             'опроса.'.format(name_user, choice(quest)))
    # начинаем опрос
    sti = open("./a_stickers/AnimatedSticker3.tgs", 'rb')  # Приветствует наступив на хвост мышке
    await message.answer_sticker(sticker=sti)
    await message.answer('{0}{1}'.format(name_user, choice(quest)))
    await Pool.Emo.set()


# Штатное завершение работы бота
async def run_bye(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    sti = open("./a_stickers/AnimatedSticker2.tgs", 'rb')  # Приветствует воздушным поцелуем
    await message.answer_sticker(sticker=sti)
    await message.answer("Мы полезно с тобой пообщались, {0}! До новых встреч!".format(name_user))
    await state.reset_state()  # для сохранения даннанных в data можно писать await state.reset_state(with_data=False)
    # !!!!! м.б. следует добавить await dp....storage.close()
    # !!!!! д.б. добавлена команда по выводу статистики из БД
    # !!!!! д.б. добавлена команда по закрытию БД
    logging.info("run_bye 0: Бот пользователя {0}(id={1}) штатно завершил работу. "
                 "current_day={2}".format(name_user, message.from_user.id, current_day))


# Обработчик ввода эмоции
@dp.message_handler(state=Pool.Emo)
async def answer_emo(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:]
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    s2 = s2[:20]  # ограничиваем фантазию пользователя 20ю символами
    # !!!!! bd_save_emotion(message, s2)
    logging.info("answer_emo 0: Пользователь {0}(id={1}) ввел эмоцию: {2}".format(name_user, message.from_user.id, s2))
    await message.answer("Как думаешь, {0}, чем эта эмоция вызвана?".format(name_user))
    await Pool.Reason.set()  # или можно await Start.next()


# Обработчик ввода эмоции
@dp.message_handler(state=Pool.Reason)
async def answer_reason(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    flag_task = data.get("flag_task")

    s = message.text[:50]  # ограничиваем фантазию пользователя 50ю символами
    # !!!!! cf.bd_save_reason(message)
    logging.info("answer_reason 0: Пользователь {0}(id={1}) ввел причину эмоции: "
                 "{2}".format(name_user, message.from_user.id, s))
    # проверяем требуется ли дополнительно запускать задачу
    if flag_task == 1:
        logging.info("answer_reason 1: вызываю выполнение задачи")
        await run_task(message, state)
        return
    # если время выполнения задачи еще не наступило
    t = get_time_next_action(state)
    data = await state.get_data()  # state меняется в функции get_time_next_action(state)
    flag_pool = data.get("flag_pool")
    flag_task = data.get("flag_task")
    logging.info("answer_reason 2: засыпаю на {0} сек. flag_pool={1} flag_task={1}".format(t, flag_pool, flag_task))
    if flag_pool:
        await Pool.Wait.set()
    else:
        await Task.Wait.set()
    await sleep(t)
    if flag_pool:  # проверяем, что после таймера нужно выполнять опрос, а не ТОЛЬКО задачу
        logging.info("answer_reason 3: вызываю выполнение запроса снова".format(t))
        await run_poll(message, state)
        return
    logging.info("answer_reason 4: вызываю выполнение ТОЛЬКО задачи после после паузы")  # выполняем ТОЛЬКО задачу
    await run_task(message, state)
    return


# ================= ПЕРЕНЕС СЮДА БЛОК ИЗ task_mess.py ЧТОБЫ ИЗБЕЖАТЬ ОШИБОК ЦИКЛИЧНОСТИ ИНТЕРПРИТАТОРА =================

# Запуск задач текущего дня
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


# Обработчик ввода ПОСЛЕДНЕГО ответа к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task.Answer_02_05)
async def answer_02_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s.lower() != "привет_2":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Привет!!</i></b>".format(name_user))
        return
    # TODO !!!!! bd_save_task_answer(s, state)
    logging.info("answer_02_05 0: Пользователь {0}(id={1}) ввел ответ: {2}".format(name_user, message.from_user.id, s))
    t = get_time_next_action(state)
    logging.info('answer_02_05 1: засыпаю на {0}'.format(t))
    await Pool.Wait.set()
    await sleep(t)
    await run_poll(message, state)  # вызов функции опроса
