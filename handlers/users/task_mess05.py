# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 5го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk04_00
from loader import dp
from states.states import Start, Task05
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 5-го дня
@dp.message_handler(state=Task05.Answer_05_01)
async def answer_05_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Начать решение задачки":
        await message.answer("https://www.youtube.com/watch?v=QgR2ozFrzk4")
        await message.answer("Какие эмоции удалось заменить у Новосельцева в этом фрагменте (перечисли через запятую)?",
                             reply_markup=tsk04_00)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Начать решение задачки» под строкой ввода "
                             "текста.".format(name_user))
        return
    await Task05.next()


# Обработчик ввода 2го ответа (Эмоции) к "задачке на прокачку" 5-го дня
@dp.message_handler(state=Task05.Answer_05_02)
async def answer_05_02(message: Message):
    s = message.text
    await db_save_task(message.from_user.id, 5, s)
    await message.answer('Я заметил у Новосельцева целую палитру эмоций:\nПеред входом в кабинет - тревога.\nПри встреч'
                         'е со старым приятелем - растерянность, которая быстро сменилась радостью от встречи.\nРеакция'
                         ' на вопросы руководителя:\n-  “Это ваш отчет?” - ожидание (в том числе ее реакции и замечаний'
                         ').\n-  “Как вы можете пользоваться не проверенными данными?” - досада.\nНовость о новом замес'
                         'тителе вызвала удивление.\nА перед выходом из кабинета при попытке задать вопрос он испытал р'
                         'астерянность.')
    await message.answer('С Новосельцевым все понятно, а ты попробуй прямо сейчас посмотреть на своего коллегу (или тог'
                         'о, кто есть рядом) и определить его эмоцию. Какую эмоцию он сейчас испытывает (ответь одним с'
                         'ловом)?')
    await Task05.next()


# Обработчик ввода 3го ответа (Эмоция соседа) к "задачке на прокачку" 5-го дня
@dp.message_handler(state=Task05.Answer_05_03)
async def answer_05_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 5, s)
    await message.answer("Учти эту эмоцию, {0}, когда будешь обращаться к нему/ней. :)".format(name_user),
                         reply_markup=menu)
    await Start.Wait.set()
