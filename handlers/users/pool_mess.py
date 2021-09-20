# В этом модуле выполняется обработка сообщений в состоянии Опроса (Pool)
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
from random import choice
import logging

from loader import dp
from states.states import Pool, Start
from utils.common_func import run_task
from utils.db_api.db_commands import db_save_emotions, db_save_reason
from keyboards.default.menu import menu, empty_menu

# Общий блок сообщений для веток: опрос и опрос+задача. Сделал здесь для удобства правки
comment = ["Понимаю, такое бывает.", "Знакомая эмоция. Фиксирую.", "Понимаю тебя. Записываю.",
           "Есть контакт. Записано.", "Все зафиксировал!", "Записано! Потом можно будет посмотреть!", "Записал. Запомню обязательно!"]
a_e_1 = "{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>"
a_e_2 = "Как думаешь, {0}, чем эта эмоция вызвана?"
a_r = "{0}"


# Обработчик ввода эмоции
@dp.message_handler(state=Pool.Emo)
async def answer_emo(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:]
    if s1.lower() != "я чувствую ":
        await message.answer(a_e_1.format(name_user))
        return
    s2 = s2[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_emotions(message.from_user.id, s2, state)
    logging.info("a_e 0: Пользователь {0}(id={1}) ввел эмоцию: {2}".format(name_user, message.from_user.id, s2))
    await message.answer(a_e_2.format(name_user))
    await Pool.Reason.set()  # или можно await Start.next()


# Обработчик ввода причины эмоции
@dp.message_handler(state=Pool.Reason)
async def answer_reason(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    s = message.text[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_reason(message.from_user.id, s, state)
    mmenu = lambda cd: empty_menu if (cd > 14) else menu
    await message.answer(a_r.format(choice(comment)), reply_markup=mmenu(current_day))
    logging.info("a_r 0: Пользователь {0}(id={1}) ввел причину эмоции: "
                 "{2}".format(name_user, message.from_user.id, s))
    await Start.Wait.set()


# Обработчик ввода эмоции
@dp.message_handler(state=Pool.EmoTask)
async def answer_emo_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:]
    if s1.lower() != "я чувствую ":
        await message.answer(a_e_1.format(name_user))
        return
    s2 = s2[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_emotions(message.from_user.id, s2, state)
    logging.info("a_e_t 0: Пользователь {0}(id={1}) ввел эмоцию: {2}".format(name_user, message.from_user.id, s2))
    await message.answer(a_e_2.format(name_user))
    await Pool.ReasonTask.set()  # или можно await Start.next()


# Обработчик ввода причины эмоции
@dp.message_handler(state=Pool.ReasonTask)
async def answer_reason_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text[:50]  # ограничиваем фантазию пользователя 50ю символами
    await db_save_reason(message.from_user.id, s, state)
    await message.answer(a_r.format(choice(comment)))  # подстрочное меню поменяется в "задачке на прокачку"
    logging.info("a_r_t 0: Пользователь {0}(id={1}) ввел причину эмоции: "
                 "{2}".format(name_user, message.from_user.id, s))
    await run_task(message, state)
