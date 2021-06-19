# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 10го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk07_01
from loader import dp
from states.states import Start, Task10
from utils.db_api.db_commands import db_save_task

# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 10-го дня
@dp.message_handler(state=Task10.Answer_10_01)
async def Answer_10_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас":
        await message.answer_photo("https://disk.yandex.ru/i/NzWJ1A-WdpqA4Q", caption="Измеритель настроения")
        await message.answer("Подумай и напиши, какие свои рабочие задачи ты мог бы эффективно выполнить, "
                             "находясь в эмоциях «красного» квадрата Измерителя настроения.\n(это неприятные по "
                             "ощущениям эмоции с высокой энергией (например, гнев, злость, отвращение, досада))",
                             reply_markup=tsk07_01)
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать тебя до конца дня".format(name_user), reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас» под строкой ввода "
                             "текста.\n Или «Выполнить позже»".format(name_user))
        return
    await Task10.next()


# красный
@dp.message_handler(state=Task10.Answer_10_02)
async def Answer_10_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 10, s)
    await message.answer("Эмоции красного квадрата лучше использовать для задач, которые связаны с борьбой"
                         " за права, критическим подходом и добыванием новой информации")
    await message.answer("Подумай и напиши, какие свои рабочие задачи ты мог бы эффективно выполнить,"
                         " находясь в эмоциях «зеленого» квадрата Измерителя настроения.\n"
                         "(это приятные по ощущениям эмоции с низкой энергией (например, "
                         "доверие, безмятежность, принятие)".format(name_user))
    await Task10.next()

# зеленый
@dp.message_handler(state=Task10.Answer_10_03)
async def Answer_10_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 10, s)
    await message.answer("Эмоции зеленого квадрата лучше использовать для постановки задач, подведения "
                         "итогов и достижения соглашений.")
    await message.answer("В какой бы эмоции я ни находился, я всегда знаю, как ее лучше использовать в работе.\n"
                         "А чтобы не забыть, какие задачи решать в той или иной эмоции, я "
                         "использую «Измеритель настроения» с подсказкой.")
    await message.answer_photo("https://disk.yandex.ru/i/vEKB_kpAUZ64Gw")
    await message.answer("На сегодня - все! Жди напоминалку по графику.", reply_markup=menu)
    await Start.Wait.set()
