from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    sti = open("./a_stickers/AnimatedSticker5.tgs", 'rb')  # Ест попкорн в 3д очках
    await message.answer_sticker(sticker=sti)
    await message.answer("Оба-на! Я незнаю зачем и как, ты послал мне это соообщение: "
                         "<b><i>{0}</i></b>!".format(message.text))


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker5.tgs", 'rb')  # Ест попкорн в 3д очках
    await message.answer_sticker(sticker=sti)
    await message.answer("{0}, я не жду от тебя этого <b><i>{1}</i></b> сообщения. Ответь корректно"
                         "!".format(name_user, message.text))
    # state = await state.get_state()
    # await message.answer(f"Эхо в состоянии <code>{state}</code>.\n"
    #                     f"\nСодержание сообщения:\n"
    #                     f"<code>{message}</code>")
