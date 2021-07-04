# В этом модуле выполняется обработка сообщений для задачи 8-го дня
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging

from keyboards.default.menu import menu
from loader import dp, LAST_DAY_2
from states.states import Start, TskRunBye
from utils.db_api.db_commands import db_update_last_day


# Обработчик ввода 1го ответа
@dp.message_handler(state=TskRunBye.Answer_RB_01)
async def answer_rb_01(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    logging.info('answer_rb_01 0: data={}'.format(data))
    s = message.text
    if s == "Да, давай продолжим!":
        await message.answer("Отлично! Напоминание о фиксации эмоций по графику начнется со следующего дня. Сегодня "
                             "фиксацию эмоции можно выполнять кликнув по служебному сообщению «Фиксировать эмоцию "
                             "сейчас» под строкой ввода текста. Ты можешь изменить настройки фиксации эмоций кликнув по"
                             " служебному сообщению «Настройки» под строкой ввода текста.",
                             reply_markup=menu)
        last_day = LAST_DAY_2
    elif s == "Нет, спасибо! Я буду самостоятельно вести Дневник эмоций.":
        await message.answer("Отлично! Напоминание о фиксации эмоций по графику прекращено. С началом следующего дня "
                             "отобразится завершающая статистическая информация по результатам нашей совместной "
                             "работы.", reply_markup=menu)
        last_day = 0
    else:
        await message.answer("{}, Кликни на служебное сообщение под строкой ввода текста для задания режима"
                             " работы!»".format(name_user))
        return
    await state.update_data(last_day=last_day)
    await db_update_last_day(message.from_user.id, last_day)
    logging.info('answer_rb_01 1: data={}'.format(data))
    await Start.Wait.set()
