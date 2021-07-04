# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 11го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk11_00, tsk02_01
from loader import dp
from states.states import Start, Task11
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 11-го дня
@dp.message_handler(state=Task11.Answer_11_01)
async def answer_11_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 11, s)
    await message.answer("Вот тебе задачка на прокачку!", reply_markup=tsk02_01)
    await Task11.next()


@dp.message_handler(state=Task11.Answer_11_02)
async def answer_11_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас!":
        await message.answer("Помогает ли сейчас твоя эмоция выполнять текущую задачу? Да или нет?",
                             reply_markup=tsk11_00)
    elif s == "Выполнить позже!":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать тебя до конца дня".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода "
                             "текста или на «Выполнить позже!».".format(name_user))
        return
    await Task11.next()


#
@dp.message_handler(state=Task11.Answer_11_03)
async def answer_11_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 11, s)
    if s.lower() == "да":
        await message.answer("Важно использовать потенциал эмоции. Какие еще задачи продуктивны в этой эмоции?")
    elif s.lower() == "нет":
        await message.answer("Важно использовать потенциал эмоции. Какие задачи были бы продуктивны в твоей "
                             "эмоции?".format(name_user))
    elif s == "Выполнить позже!":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать тебя до конца дня".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, Набери пожалуйста или Да или Нет\nИли выбери «Выполнить позже»".format(name_user))
        return
    await Task11.next()


#
@dp.message_handler(state=Task11.Answer_11_04)
async def answer_11_04(message: Message, state: FSMContext):
    s = message.text
    await db_save_task(message.from_user.id, 11, s)
    await message.answer("Используй свои эмоции по полной 😉")
    await message.answer("На сегодня - все! Жди напоминалку по графику.", reply_markup=menu)
    await Start.Wait.set()
