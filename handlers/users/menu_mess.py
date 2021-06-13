# В этом модуле выполняется обработка сообщений из текстового меню
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from handlers.users.pool_mess import run_poll
from handlers.users.task_mess import run_task
from loader import dp


@dp.message_handler(Text(equals="Фиксировать эмоцию сейчас"), state='*')
async def get_emo(message: Message, state: FSMContext):
    c_state = await state.get_state()
    if c_state != "Start:Wait":
        data = await state.get_data()
        name_user = data.get("name_user")
        await message.answer('{0}, для внеочередной фиксации эмоции сначала заверши ответ на текущий '
                             'вопрос!'.format(name_user))
    await run_poll(message, state)


@dp.message_handler(Text(equals="Выполнить задачку ”на прокачку”"), state='*')
async def get_tsk(message: Message, state: FSMContext):
    c_state = await state.get_state()
    if c_state != "Start:Wait":
        data = await state.get_data()
        name_user = data.get("name_user")
        await message.answer('{0}, для внеочередного выполнения задачки ”на прокачку”" сначала заверши ответ на'
                             ' текущий вопрос!'.format(name_user))
    await run_task(message, state)




@dp.message_handler(Text(equals="Выполнить задачку ”на прокачку”"), state='*')
async def get_list(message: Message, state: FSMContext):
    c_state = await state.get_state()
    if c_state != "Start:Wait":
        data = await state.get_data()
        name_user = data.get("name_user")
        await message.answer('{0}, для внеочередного выполнения задачки ”на прокачку”" сначала заверши ответ на'
                             ' текущий вопрос!'.format(name_user))
    await run_task(message, state)
