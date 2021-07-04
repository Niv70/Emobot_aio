# В этом модуле выполняется обработка сообщений для задачи 8-го дня
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import asyncio

from keyboards.default.menu import menu
from loader import dp, LAST_DAY_2
from states.states import Start, TskRunBye
from utils.common_func import run_bye
from utils.notify_admins import on_notify


# Обработчик ввода 1го ответа
@dp.message_handler(state=TskRunBye.Answer_RB_01)
async def answer_rb_01(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text
    if s == "Да, давай продолжим!":
        await message.answer("Отлично! Напоминание о фиксации эмоций по графику начнется со следующего дня. Сегодня "
                             "фиксацию эмоции можно выполнять кликнув по служебному сообщению «Фиксировать эмоцию "
                             "сейчас» под строкой ввода текста. Ты можешь изменить настройки фиксации эмоций кликнув по"
                             " служебному сообщению «Настройки» под строкой ввода текста.",
                             reply_markup=menu)
        last_day = LAST_DAY_2
    elif s == "Нет, спасибо! Я буду самостоятельно вести Дневник эмоций.":
        task = asyncio.create_task(on_notify(dp, "Пользователь {0}(id={1}) не захотел брать доп."
                                                 "дни!".format(name_user, message.from_user.id)))
        await task
        name_task = data.get("name_task")
        all_task = asyncio.all_tasks(asyncio.get_running_loop())
        for i in all_task:
            if name_task == i.get_name():
                i.cancel()
        await run_bye(message, state)  # выводим статистику и сбрасываем состояние
        return
    else:
        await message.answer("{}, Кликни на служебное сообщение под строкой ввода текста для задания режима"
                             " работы!»".format(name_user))
        return
    await state.update_data(last_day=last_day)  # TODO здесь нужно сделать запись в БД
    await Start.Wait.set()
