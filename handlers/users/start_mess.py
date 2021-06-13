# Выделил обработку стартовых сообщени в отдельный файл, чтобы корректно отрабатывала команда /stop
import datetime
from aiogram.types import Message, CallbackQuery
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging

from loader import dp
from states.states import Start
from utils.common_func import get_digit, loop_action
from keyboards.inline.choice_buttons import choice01, choice02, choice03, choice04, choice05, choice06
from utils.db_api.db_commands import get_name_by_id, db_add_user, get_settings_by_id, db_update_user_settings
from utils.db_api.models import Emo_users


# Обработчик ввода имени пользователя на стадии начала работы бота
@dp.message_handler(state=Start.set_user_name)
async def answer_name(message: Message, state: FSMContext):
    answer = message.text[:20]  # ограничиваем фантазию пользователя 20ю символами
    # инициализируем список ключей данных
    sss = await get_name_by_id(message.from_user.id)
    if sss is None:
        await db_add_user(message.from_user.id, message.from_user.first_name, answer)
    await state.update_data(name_user=answer)
    await state.update_data(tmz=0)
    await state.update_data(start_t=8)
    await state.update_data(end_t=17)
    await state.update_data(period=2)
    await state.update_data(tsk_t=99)
    await state.update_data(current_day=0)
    await state.update_data(flag_pool=0)
    await state.update_data(flag_task=0)
    await message.answer("{0}, я хочу помочь тебе исследовать и фиксировать "
                         "собственные эмоции. Если ты соглашаешься участвовать в этой работе,"
                         " то я начну регулярно измерять твою «эмоциональную температуру» в "
                         "течение дня.".format(answer), reply_markup=choice01)
    await Start.Call_01.set()  # или можно await Start.next()


# функция инициализации переменных при повтороном запуске ботика пользователем
async def user_settings_from_db(message: Message, state: FSMContext):
    user_settings: Emo_users = await get_settings_by_id(message.from_user.id)
    # инициализируем список ключей данных
    await state.update_data(name_user=user_settings.name)
    await state.update_data(tmz=user_settings.ZoneTime)
    await state.update_data(start_t=user_settings.StartTime)
    await state.update_data(end_t=user_settings.EndTime)
    await state.update_data(period=user_settings.Period)
    await state.update_data(tsk_t=user_settings.TaskTime)
    await state.update_data(current_day=user_settings.CurrentDay)
    await state.update_data(flag_pool=1)
    await state.update_data(flag_task=0)


# Обработчик нажатия кнопки "Зачем?"
@dp.callback_query_handler(text="choice:Start_Call01:Зачем?", state=Start.Call_01)
async def press_call01_key2(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда на нажатие кнопки будет идти ответ из кэша.
    await call.answer(cache_time=60)
    # Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы убрать ее из сообщения
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    await call.message.answer("Ну как зачем? Представь, что твоя жизнь – это суп. Если ты просто сваливаешь продукты в"
                              " кастрюлю, ставишь огонь наугад и варишь, не заглядывая под крышку, то что получится?"
                              " Так вот, жизнь, где игнорируются эмоции и их сигналы, выглядит примерно так же. А "
                              "бывает такое: игнорируешь, игнорируешь, а потом у кастрюли «срывает крышку», и ты "
                              "совершаешь нечто из ряда вон.")
    await call.message.answer("Но есть и хорошая новость: эмоции поддаются управлению. Первый шаг к этой цели - "
                              "научиться их замечать и осознавать. Такой навык поможет наладить контакт с собой, "
                              "получить доступ к истинным желаниям и пониманию себя. А это значит – видеть картину"
                              " происходящего в гораздо большем объеме и принимать максимально полезные для себя и "
                              "других решения. Звучит вкусно, правда?", reply_markup=choice02)


# Обработчик нажатия кнопки "Начнем" для первого сообщения (или для обработчика кнопки "Зачем?")
@dp.callback_query_handler(text="choice:Start_Call01:Начнем", state=Start.Call_01)
async def press_call01_key1(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    await call.message.answer("В предвкушении потираю лапы! Но, перед тем как приступить, предлагаю познакомиться с "
                              "<b><i>Эмоциональным термометром</i></b>. Это нужно, чтобы мы быстро и точно могли "
                              "измерить твою «эмоциональную температуру».", reply_markup=choice03)
    await Start.Call_02.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Интересно!"
@dp.callback_query_handler(text="choice:Start_Call02:Интересно!", state=Start.Call_02)
async def press_call02_key2(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    await call.message.answer("Это шкала из 27 эмоций, расположенных по интенсивности, с помощью которой ты "
                              " ориентироваться в своем состоянии. Всегда обращайся к ней, особенно по началу, "
                              "чтобы дать максимально точный ответ, который я смогу считать и зафиксировать.",
                              reply_markup=choice04)


# Обработчик нажатия кнопки "Уже_знаком"
@dp.callback_query_handler(text="choice:Start_Call02:Уже_знаком", state=Start.Call_02)
async def press_call02_key2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("Отлично, {0}! Всегда обращайся к нему особенно по началу, чтобы дать максимально точный"
                              " ответ, который я смогу считать и зафиксировать. Если ты захочешь заглянуть в него, "
                              "нажми на кнопку «Эмоциональный термометр», которая по завершению настроек опроса "
                              "появится под строкой ввода текста.".format(name_user))  # reply_markup=choice05
    await call.message.answer("Я буду периодически снимать твои эмоциональные показатели. Ты будешь получать "
                              "сообщение: «Что ты чувствуешь прямо сейчас?». И где бы оно тебя ни застало, шли мне в"
                              " ответ, какую эмоцию ты чувствуешь в эту минуту. Договорились?",
                              reply_markup=choice05)
    await Start.Call_03.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Договорились"
@dp.callback_query_handler(text="choice:Start_Call03:Договорились", state=Start.Call_03)
async def press_call02_key2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("Я смогу зарегистрировать эмоцию только тогда, когда ты напишешь ее в формулировке "
                              "«Я чувствую (эмоция из Термометра)». Произнеси «я чувствую страх», «я в ужасе» и «меня "
                              "напугали». Замечаешь разницу? «Я в ужасе» - и эмоция полностью захватила тебя, остается"
                              " только бежать. «Меня напугали» - эмоция есть, но как будто не твоя, ответственность за"
                              " нее нести не нужно. А вот «я чувствую страх» - формулировка, в которой есть и признание"
                              " своей эмоции как факта, и дистанция, чтобы ее наблюдать как исследователь. Я – субъект,"
                              " чувство – объект. Можем потренироваться прямо сейчас.")
    await call.message.answer("{0}, напиши <b><i>Я чувствую интерес</i></b>".format(name_user))
    await Start.Tst.set()  # или можно await Start.next()


# Обработчик ввода "Я чувствую интерес"
@dp.message_handler(state=Start.Tst)
async def answer_tst(message: Message, state: FSMContext):
    answer = message.text.lower()  # делаем ответ пользователя регистронезависимым
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    if answer == "я чувствую интерес":
        await message.answer("У тебя здорово получается!\nНачиная со 2-го дня работы, один раз в день, я буду задавать"
                             " тебе интересное задание «на прокачку». Постарайся выполнить его честно и быстро - это"
                             " ОЧЕНЬ ВАЖНО! ")
        await message.answer("Отлично, {0}! Блок ознакомительной информации закончен, можно "
                             "перейти к настройкам времени опроса.".format(name_user))
        await set_settings(message, state)  # следующее состояние установится внутри этой функции
    else:
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую интерес</i></b>".format(name_user))


# Функция для настроек времени опроса бота (при наступлении времени опроса м.б. прервана без записи в БД)
async def set_settings(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    c_data = datetime.datetime.now()
    await message.answer("Давай сверим наши часы!\nМое текущее время: "
                         "{0:0>2}:{1:0>2}.".format(c_data.hour, c_data.minute))
    await message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> от 0 до 23 <b>разницу с "
                         "твоим текущим временем</b>:".format(name_user))
    await Start.set_tmz.set()  # или можно await Start.next()


# Обработчик ввода цифры Часовой пояс
@dp.message_handler(state=Start.set_tmz)
async def answer_tmz(message: Message, state: FSMContext):
    d = await get_digit(message, state, 0, 23)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка корректности ввода пользователя
        return
    await state.update_data(tmz=d)
    c_data = datetime.datetime.now() + datetime.timedelta(hours=d)
    await message.answer("Мое текущее время {0:0>2}:{1:0>2}.".format(c_data.hour, c_data.minute))
    await message.answer("Сейчас мое время совпадает с твоим?\n(если оно меньше на минуту-другую - это нормально)",
                         reply_markup=choice06)
    await Start.Call_04.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Да"
@dp.callback_query_handler(text="choice:Start_Call04:Да", state=Start.Call_04)
async def press_call04_key1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()  # достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    await call.message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> удобное <b>время начала опроса</b> от"
                              " 0 до 22:".format(name_user))
    await Start.set_start_t.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Нет"
@dp.callback_query_handler(text="choice:Start_Call04:Нет", state=Start.Call_04)
async def press_call04_key2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<code>------- обработка нажатия кнопки -------</code>")  # отмечаю место, где были кнопки
    await set_settings(call.message, state)  # следующее состояние установится внутри этой функции


# Обработчик ввода цифры Время начала опроса
@dp.message_handler(state=Start.set_start_t)
async def answer_start_t(message: Message, state: FSMContext):
    d = await get_digit(message, state, 0, 22)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await state.update_data(start_t=d)
    await message.answer("Итак, начало опроса в {0:0>2}:00.".format(d))
    await message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> удобное <b>время завершения опроса</b>"
                         " от 1 до 23:".format(name_user))
    await Start.set_end_t.set()  # или можно await Start.next()


# Обработчик ввода цифры Время завершения опроса
@dp.message_handler(state=Start.set_end_t)
async def answer_end_t(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 23)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    if d <= start_t:
        await message.answer('{0}, время завершения опроса д.б. больше времени начала опроса!'.format(name_user))
        return
    await state.update_data(end_t=d)
    await message.answer("Итак, начало опроса в {0:0>2}:00.".format(d))
    await message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> удобный <b>период опроса</b>"
                         " от 1 до 23:".format(name_user))
    await Start.set_period.set()  # или можно await Start.next()


# Обработчик ввода цифры Период опроса
@dp.message_handler(state=Start.set_period)
async def answer_period(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 23)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    await state.update_data(period=d)
    await message.answer("Итак, я буду опрашивать что ты чувствуешь в:")
    i = 0
    while start_t + i < end_t:
        await message.answer("{0:0>2}:00".format(start_t + i))
        i = i + d
    await message.answer("и {0:0>2}:00".format(end_t))
    await message.answer('{0}, пожалуйста, введи <i>одним числом в часах</i> удобное <b>время выполнения задачки'
                         ' "на прокачку"</b> от 0 до 23 (если время задачки и время опроса совпадут, выполнение '
                         'задачки начнется сразу после опроса):'.format(name_user))
    await Start.set_tsk_t.set()  # или можно await Start.next()


# Обработчик ввода цифры Время задачки "на прокачку"
@dp.message_handler(state=Start.set_tsk_t)
async def answer_tsk_t(message: Message, state: FSMContext):
    d = await get_digit(message, state, 0, 23)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    if d < start_t or d > end_t:
        await message.answer('{0}, время выполнения задачки "на прокачку" д.б. в границах начала и завершения'
                             ' опроса!'.format(name_user))
        return
    await state.update_data(tsk_t=d)
    await message.answer('Итак, выполнение задачки "на прокачку" в: {0:0>2}:00'.format(d))
    await message.answer("Отлично, {0}! Настройки завершены - опрос начнется с наступлением следующего "
                         "дня.".format(name_user))
    logging.info('answer_tsk_t 0: start_t={0} end_t={1} data={2}'.format(start_t, end_t, data))
    # TODO Добавить создание текстовой клавиатуры
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"), period=data.get("period"),
                                  end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=d)
    await Start.Wait.set()  # это состояние не имеет обработчиков - все сообщения "не команды" попадают в Эхо
    await loop_action(message, state)  # вызов бесконечного цикла действий
