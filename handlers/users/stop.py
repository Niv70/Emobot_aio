import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from utils.notify_admins import on_notify


# Обработка повторного вызова команды /stop
@dp.message_handler(Command("stop"), state=None)
async def bot_restop(message: Message):
    await message.answer("ЗаБотик уже остановлен :)")
    # д.б. добавлена команда по закрытию БД


# Обработка правильного вызова команды /stop
@dp.message_handler(Command("stop"), state='*')
async def bot_stop(message: Message, state: FSMContext):
    c_state = await state.get_state()
    c_state = c_state[:10]
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    task = asyncio.create_task(on_notify(dp, ""))
    name_task = data.get("name_task")
    all_task = task.all_tasks(asyncio.get_running_loop())
    for i in all_task:
        if name_task == i.get_name():
            i.cancel()
            print(i.get_name())
    await message.answer("Останов пользователем {0} в состянии {1}".format(name_user, c_state))
    await state.reset_state()  # для сохранения даннанных в data можно писать await state.reset_state(with_data=False)

    sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Жалостливо что-то выпрашивает
    await message.answer_sticker(sticker=sti)
    await message.answer("Возвращайся, {0}! Я буду скучать. Работу можно будет начать сразу с {1}-го "
                         "дня.".format(name_user, current_day), reply_markup=ReplyKeyboardRemove())
    await on_notify(dp, "Пользователь {0}(id={1}) остановил бота. "
                        "current_day={2}".format(name_user, message.from_user.id, current_day))
