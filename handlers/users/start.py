# import logging
import logging

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext

from handlers.users.start_mess import user_settings_from_db
from loader import dp
from states.states import Start
from utils.common_func import loop_action
from utils.db_api.db_commands import get_name_by_id


# Обработка первого вызова команды /start
@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message, state: FSMContext):
    str0 = await get_name_by_id(message.from_user.id)
    #  это делается из FSM.json файла?
    # Для удобства использования задаем локальные для модуля переменные
    help_m = "При ответах на вопрос боту регистр букв неважен.\n" \
             "!!ВАЖНО: Для продолжения работы после использования команды, следует ответить на заданный ранее вопрос."
    await message.answer(help_m)
    sti = open("./a_stickers/AnimatedSticker9.tgs", 'rb')  # Подмигивает, снимая очки
    await message.answer_sticker(sticker=sti)
    if str0 is None:
        await message.answer("Привет! Как тебя зовут?")
        await Start.set_user_name.set()  # или можно await Start.first()
    else:
        await message.answer(
            "Привет! Я - ЗаБотик - заботливый и веселый Телеграм-бот.\n Рад еще раз видеть тебя {0}!".format(str0))
        await user_settings_from_db(message, state)
        data = await state.get_data()
        tskd = data.get("tsk_t")
        if tskd > 90:
            await message.answer("Привет! Я - ЗаБотик - заботливый и веселый Телеграм-бот. А тебя как зовут?")
            await Start.set_user_name.set()  # или можно await Start.first()
            return
        await message.answer("Снова здравствуй, {0}! Твои настройки восстановлены из БД - опрос начнется с "
                             "наступлением следующего дня.".format(str0))
        # TODO      Добавить   создание  текстовой        клавиатуры
        await Start.Wait.set()  # это состояние не имеет обработчиков - все сообщения "не команды" попадают в Эхо
        logging.info('answer_tsk_t 0:  data={0}'.format(data))
        await loop_action(message, state)  # вызов бесконечного цикла действий


# Обработка повторного вызова команды /start
@dp.message_handler(CommandStart(), state='*')
async def bot_restart(message: types.Message):
    await message.answer("ЗаБотик уже работает :)")
