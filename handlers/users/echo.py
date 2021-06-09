from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    sti = open("./a_stickers/AnimatedSticker6.tgs", 'rb')  # Ест попкорн в 3д очках
    await message.answer_sticker(sticker=sti)
    await message.reply("Оба-на! Ты послал мне соообщение, но я не знаю как его понять :)")


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker6.tgs", 'rb')  # Ест попкорн в 3д очках
    await message.answer_sticker(sticker=sti)
    await message.reply("{0}, я не ждал от тебя этого сообщения и не знаю как его понять :)".format(name_user))
    # state = await state.get_state()
    # await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
    #                     f"\nСодержание сообщения:\n"
    #                     f"<code>{message}</code>")
