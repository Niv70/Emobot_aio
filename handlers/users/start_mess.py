# Выделил обработку стартовых сообщени в отдельный файл, чтобы корректно отрабатывала команда /stop
# from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from states.states import Start
from keyboards.inline.choice_buttons import choice01
from utils.notify_admins import on_notify

on_notify("в start_mess")

# Обработчик ввода имени пользователя на стадии начала работы бота
@dp.message_handler(state=Start.Name)
async def answer_q0(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_user=answer)
    await message.answer("{0}, я хочу помочь тебе исследовать и фиксировать "
                         "собственные эмоции. Если ты соглашаешься участвовать в этой работе,"
                         " то я начну регулярно измерять твою «эмоциональную температуру» в "
                         "течение дня.".format(answer), reply_markup=choice01)
    logging.info(f"{state=}")


# Обработчик нажатия кнопок для предыдущего сообщения
# @dp.callback_query_handler(text_contains="c")  # text_contains="choice:Start:Начнем"
@dp.callback_query_handler(text_contains="choice")
async def press_key1(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=60)
    callback_data = call.data
    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    # В Python 3.8 можно так, если у вас ошибка, то сделайте предыдущим способом!
    logging.info(f"{callback_data=}")
    # Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы убрать ее из сообщения
    await call.message.edit_reply_markup(reply_markup=None)
    await Start.Q2.set()  # или можно await Start.next()


@dp.message_handler(state=Start.Q2)
async def answer_q1(message: Message, state: FSMContext):
    answer = message.text
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer(f"{answer=} и {name_user=}")
    answer = "buka"
    await state.update_data(name_user=answer)
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer(f"После изменения {name_user=}")

    await Start.Q2.set()  # или можно await Start.next()
