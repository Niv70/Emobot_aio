# В этом модуле выполняется обработка сообщений в состоянии Опроса (Pool)
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
from random import choice
import logging

from loader import dp
from states.states import Pool, Start
from .task_mess import run_task
from utils.db_api.db_commands import db_save_emotions, db_save_reason


# Общий блок сообщений для веток: опрос и опрос+задача. Сделал здесь для удобства правки
quest = [", что ты сейчас чувствуешь?", ", какая эмоция сейчас внутри тебя?",
         ", прислушайся какая эмоция сейчас внутри тебя?", ", тук-тук-тук, что ты сейчас чувствуешь?"]
r_p = "{0}{1}"
a_e_1 = "{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>"
a_e_2 = "Как думаешь, {0}, чем эта эмоция вызвана?"
a_r = "Спасибо, {0}, информация сохранена."


# Запуск опроса эмоции
async def run_poll(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker3.tgs", 'rb')  # Приветствует наступив на хвост мышке
    await message.answer_sticker(sticker=sti)
    await message.answer(r_p.format(name_user, choice(quest)))
    await Pool.Emo.set()


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
    s2 = s2[:20]  # ограничиваем фантазию пользователя 20ю символами
    await db_save_emotions(message.from_user.id, s2)
    logging.info("a_e 0: Пользователь {0}(id={1}) ввел эмоцию: {2}".format(name_user, message.from_user.id, s2))
    await message.answer(a_e_2.format(name_user))
    await Pool.Reason.set()  # или можно await Start.next()


# Обработчик ввода причины эмоции
@dp.message_handler(state=Pool.Reason)
async def answer_reason(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text[:50]  # ограничиваем фантазию пользователя 50ю символами
    await db_save_reason(message.from_user.id, s)
    await message.answer(a_r.format(name_user))
    logging.info("a_r 0: Пользователь {0}(id={1}) ввел причину эмоции: "
                 "{2}".format(name_user, message.from_user.id, s))
    await Start.Wait.set()


# Запуск опроса эмоции c последующим запуском задачи
async def run_poll_task(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker3.tgs", 'rb')  # Приветствует наступив на хвост мышке
    await message.answer_sticker(sticker=sti)
    await message.answer(r_p.format(name_user, choice(quest)))
    await Pool.EmoTask.set()


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
    s2 = s2[:20]  # ограничиваем фантазию пользователя 20ю символами
    await db_save_emotions(message.from_user.id, s2)
    logging.info("a_e_t 0: Пользователь {0}(id={1}) ввел эмоцию: {2}".format(name_user, message.from_user.id, s2))
    await message.answer(a_e_2.format(name_user))
    await Pool.ReasonTask.set()  # или можно await Start.next()


# Обработчик ввода причины эмоции
@dp.message_handler(state=Pool.ReasonTask)
async def answer_reason_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text[:50]  # ограничиваем фантазию пользователя 50ю символами
    await db_save_reason(message.from_user.id, s)
    await message.answer(a_r.format(name_user))
    logging.info("a_r_t 0: Пользователь {0}(id={1}) ввел причину эмоции: "
                 "{2}".format(name_user, message.from_user.id, s))
    await run_task(message, state)
