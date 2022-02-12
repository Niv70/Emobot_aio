import asyncio
import logging
# from aiogram import types
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from handlers.users.start import user_settings_from_db, user_settings_from_db1
from states.states import Start

from utils.common_func import loop_action
from utils.db_api.models import Emo_users, Emotions, Tasks
from utils.db_api.database import db
from utils.db_api.db_commands import get_active_users


async def RestartActiveUsers(dp: Dispatcher):
    ausers = await get_active_users()
    for au in ausers:
        message: types.Message = await dp.bot.send_message(au, "...restarting.")
        message.from_user.id = au
        state: FSMContext = dp.current_state(chat=au)
        await user_settings_from_db1(au, state)
        data = await state.get_data()
        tsk_t = data.get("tsk_t")
        current_day = data.get("current_day")
        start_t = data.get("start_t")
        await state.set_state(Start.Wait)
        task_loop_action = asyncio.create_task(loop_action(message, state))
        name_task = task_loop_action.get_name()
        await state.update_data(name_task=name_task)
        data = await state.get_data()
        logging.info('перезапуск: {} data={}'.format(name_task, data))


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "АДМИНу: Бот Запущен")
        except Exception as err:
            logging.exception(err)
    await RestartActiveUsers(dp)


async def on_notify(dp: Dispatcher, text: str):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "АДМИНу: " + text)
        except Exception as err:
            logging.exception(err)
