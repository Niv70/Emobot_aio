from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from loader import dp
from utils.db_api.db_commands import db_update_user_settings
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
    current_day = data.get("current_day")
    sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Жалостливо что-то выпрашивает
    await state.reset_state()  # для сохранения данных в data можно писать await state.reset_state(with_data=False)
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"), period=data.get("period"),
                                  end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await message.answer_sticker(sticker=sti)
    await message.answer("Возвращайся, {0}! Я буду скучать.".format(name_user))
    await on_notify(dp, "Пользователь {0}(id={1}) остановил бота. "
                        "current_day={2}".format(name_user, message.from_user.id, current_day))

