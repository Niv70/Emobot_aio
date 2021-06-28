# Выделил обработку стартовых сообщений в отдельный файл, чтобы корректно отрабатывала команда /stop
import asyncio
import datetime
from aiogram.types import Message, CallbackQuery
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext
import logging


from loader import dp
from states.states import Start
from utils.common_func import get_digit, loop_action
from keyboards.inline.choice_buttons import choice01, choice02, choice03, choice04, choice05, choice06, choice07
from keyboards.default import menu
from utils.db_api.db_commands import get_name_by_id, db_add_user, db_update_user_settings


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
    await state.update_data(flag_pool=1)
    await state.update_data(flag_task=0)
    await message.answer("Я - ЗаБотик - веселый и заботливый Телеграм-бот. Я помогаю людям фиксировать и исследовать"
                         " собственные эмоции.\n{0}, если ты соглашаешься участвовать в этой работе, то я начну "
                         "регулярно измерять твою «эмоциональную температуру» в течение дня.".format(answer),
                         reply_markup=choice01)
    await Start.Call_01.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Зачем?"
@dp.callback_query_handler(text="choice:Start_Call01:Зачем?", state=Start.Call_01)
async def press_call01_key2(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда на нажатие кнопки будет идти ответ из кэша.
    await call.answer(cache_time=60)
    # Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы убрать ее из сообщения
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
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
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    await call.message.answer("В предвкушении потираю лапы! Но, перед тем как приступить, предлагаю познакомиться с "
                              "<b><i>Эмоциональным термометром</i></b>. Это нужно, чтобы мы быстро и точно могли "
                              "измерить твою «эмоциональную температуру».", reply_markup=choice03)
    await Start.Call_02.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Интересно!"
@dp.callback_query_handler(text="choice:Start_Call02:Интересно!", state=Start.Call_02)
async def press_call02_key2(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    img = open("./IMG/Термометр.jpg", "rb")
    await call.message.answer_photo(img)
    await call.message.answer("Это шкала из 27 эмоций (см. картинку), расположенных по интенсивности, с помощью которой"
                              " ты сможешь ориентироваться в своем состоянии.", reply_markup=choice04)


# Обработчик нажатия кнопки "Уже_знаком"
@dp.callback_query_handler(text="choice:Start_Call02:Уже_знаком", state=Start.Call_02)
async def press_call02_key1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("Отлично, {0}! Всегда обращайся к нему особенно по началу, чтобы дать максимально точный"
                              " ответ, который я смогу считать и зафиксировать. Если ты захочешь заглянуть в него, "
                              " выбери служебное сообщение «Термометр», которое по завершению настроек опроса появится"
                              " под строкой ввода текста.".format(name_user), reply_markup=choice05)
    await Start.Call_03.set()


# Обработчик нажатия нажатия 1й кнопки "Дальше"
@dp.callback_query_handler(text="choice:Start_Call03_04:Дальше", state=Start.Call_03)
async def press_call03_key(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("{0}, вероятно, ты знаешь, что есть разные модели эмоций. Иногда мы употребляем "
                              "интересные слова для страха, злости и печали минимальной интенсивности, например, "
                              "страшок, злобинушка, печалька или грустинка. И это важно, потому что  чаще всего именно"
                              " эти слабые сигналы мы и упускаем. В итоге осознание, того, что именно с нами происходит"
                              ", появляется гораздо позднее, чем могло бы. Если ты не сможешь найти в «Эмоциональном "
                              "термометре» точное название своей эмоции, выбери служебное сообщение  «Список эмоций и"
                              " чувств», которое по завершению настроек опроса также появится под строкой ввода текста."
                              " Отобразится свыше 120 различных эмоций и чувств. Эмоция – это кратковременное "
                              "переживание человека по поводу ситуации или события. Чувство – это уже более длительное"
                              " и более сложное состояние. Ты можешь фиксировать чувство или эмоцию.\nЕсли ты захочешь,"
                              " то можешь использовать собственные формулировки эмоций.".format(name_user),
                              reply_markup=choice05)
    await Start.Call_04.set()  # или можно await Start.next()


# Обработчик нажатия 2й кнопки "Дальше"
@dp.callback_query_handler(text="choice:Start_Call03_04:Дальше", state=Start.Call_04)
async def press_call04_key(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("Итак, {0}, я буду периодически снимать твои эмоциональные показатели. Ты будешь получать"
                              " сообщение: «Что ты чувствуешь прямо сейчас?». И где бы оно тебя ни застало, шли мне в"
                              " ответ, какую эмоцию ты чувствуешь в эту минуту. Договорились"
                              "?".format(name_user), reply_markup=choice06)
    await Start.Call_05.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Договорились"
@dp.callback_query_handler(text="choice:Start_Call05:Договорились", state=Start.Call_05)
async def press_call05_key(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
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
        await message.answer("У тебя здорово получается!\nЗачастую, один раз в день, я буду давать"
                             " тебе интересную ”задачку на прокачку”. Постарайся выполнить ее честно и быстро - это"
                             " ОЧЕНЬ ВАЖНО!", reply_markup=choice05)
        await Start.Call_05_1.set()  # выполняю неожиданную просьбу о кнопке здесь от ОРП
    else:
        await message.answer("{0}, я не распознаю твой ответ. Напиши в формулировке  <b><i>Я чувствую "
                             "интерес</i></b>".format(name_user))


# Обработчик нажатия 3й (непланирумой мной) кнопки "Дальше"
@dp.callback_query_handler(text="choice:Start_Call03_04:Дальше", state=Start.Call_05_1)
async def press_call05_1_key(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("Отлично, {0}! Блок ознакомительной информации закончен, можно перейти к настройкам "
                              "времени опроса. Если ты захочешь их позже изменить, то можешь это сделать выбрав "
                              "служебное сообщение «Настройки», которое по завершению настроек опроса также появится "
                              "под строкой ввода текста.".format(name_user))
    await set_settings(call.message, state)  # следующее состояние установится внутри этой функции


# Функция для настроек времени опроса бота
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
    await message.answer("Сейчас мое время совпадает с твоим?\n(если оно отличается на минуту-другую - это нормально)",
                         reply_markup=choice07)
    await Start.Call_06.set()


# Обработчик нажатия кнопки "Да"
@dp.callback_query_handler(text="choice:Start_Call06:Да", state=Start.Call_06)
async def press_call06_key1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    data = await state.get_data()  # достаем имя пользователя
    name_user = data.get("name_user")
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
    await call.message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> удобное <b>время начала опроса</b> от"
                              " 0 до 22:".format(name_user))
    await Start.set_start_t.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Нет"
@dp.callback_query_handler(text="choice:Start_Call06:Нет", state=Start.Call_06)
async def press_call06_key2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<s>-  кнопка нажата  -</s>")  # отмечаю место, где были кнопки
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
                         " от {1} до 23:".format(name_user, d+1))
    await Start.set_end_t.set()  # или можно await Start.next()


# Обработчик ввода цифры Время завершения опроса
@dp.message_handler(state=Start.set_end_t)
async def answer_end_t(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    d = await get_digit(message, state, start_t+1, 23)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    await state.update_data(end_t=d)
    await message.answer("Итак, завершение опроса в {0:0>2}:00.".format(d))
    await message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> удобную <b>периодичность опроса</b>"
                         " от 1 до 4:".format(name_user))
    await Start.set_period.set()  # или можно await Start.next()


# Обработчик ввода цифры Период опроса
@dp.message_handler(state=Start.set_period)
async def answer_period(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 4)  # преобразовываем сообщение в цифру
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
    await message.answer('{0}, пожалуйста, введи <i>одним числом в часах</i> удобное <b>время выполнения ”задачки'
                         ' на прокачку”</b> от {1} до {2} (если время задачки и время опроса совпадут, выполнение '
                         'задачки начнется сразу после опроса):'.format(name_user, start_t, end_t))
    await Start.set_tsk_t.set()  # или можно await Start.next()


# Обработчик ввода цифры Время ”задачки на прокачку”
@dp.message_handler(state=Start.set_tsk_t)
async def answer_tsk_t(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    d = await get_digit(message, state, start_t, end_t)  # преобразовываем сообщение в цифру
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    await state.update_data(tsk_t=d)
    await message.answer('Итак, выполнение ”задачки на прокачку” в: {0:0>2}:00'.format(d))
    await message.answer("Отлично, {0}! Настройки заверешены - опрос начнется с наступлением следующего "
                         "дня.".format(name_user))
    await message.answer('А, вот ещё. Если ты захочешь зафиксировать эмоцию или решить ”задачку на прокачку” для '
                         'текущего дня работы без моего напоминания - просто выбери служебное сообщение "Фиксировать '
                         'эмоцию сейчас" или "Выполнить ”задачку на прокачку”" под строкой ввода текста',
                         reply_markup=menu)
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=1, task_time=data.get("tsk_t"))
    await Start.Wait.set()  # это состояние не имеет обработчиков - все сообщения "не команды" попадают в Эхо
    task_loop_action = asyncio.create_task(loop_action(message, state))
    name_task = task_loop_action.get_name()
    await state.update_data(name_task=name_task)
    data = await state.get_data()
    logging.info('answer_tsk_t 0: start_t={0} end_t={1} data={2}'.format(start_t, end_t, data))
    await task_loop_action  # ждем завершения бесконечного цикла действий
