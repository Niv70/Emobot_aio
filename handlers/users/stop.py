from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from utils.notify_admins import on_notify


# Обработка повторного вызова команды /stop
@dp.message_handler(Command("stop"), state=None)
async def bot_restop(message: types.Message):
    await message.answer("ЗаБотик уже остановлен :)")
    # д.б. добавлена команда по закрытию БД


# Обработка правильного вызова команды /stop
@dp.message_handler(Command("stop"), state='*')
async def bot_stop(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Жалостливо что-то выпрашивает
    await state.reset_state()  # для сохранения даннанных в data можно писать await state.reset_state(with_data=False)
    await message.answer_sticker(sticker=sti)
    await message.answer("Возвращайся, {0}! Я буду скучать.".format(name_user))
    await on_notify(dp, "Пользователь {0}(id={1}) остановил бота".format(name_user, message.from_user.id))
    # д.б. добавлена команда по закрытию БД
