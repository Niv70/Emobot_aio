# Выделил обработку стартовых сообщени в отдельный файл, чтобы корректно отрабатывала команда /stop
# from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
# import logging

from loader import dp
from states.states import Start
from keyboards.inline.choice_buttons import choice01, choice02, choice03, choice04, choice05


# Обработчик ввода имени пользователя на стадии начала работы бота
@dp.message_handler(state=Start.Name)
async def answer_name(message: Message, state: FSMContext):
    answer = message.text
    await state.update_data(name_user=answer)
    await message.answer("{0}, я хочу помочь тебе исследовать и фиксировать "
                         "собственные эмоции. Если ты соглашаешься участвовать в этой работе,"
                         " то я начну регулярно измерять твою «эмоциональную температуру» в "
                         "течение дня.".format(answer), reply_markup=choice01)
    await Start.Call_01.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Зачем?"
@dp.callback_query_handler(text="choice:Start_Call01:Зачем?", state=Start.Call_01)
async def press_call01_key2(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда на нажатие кнопки будет идти ответ из кэша.
    await call.answer(cache_time=60)
    # Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы убрать ее из сообщения
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<i>------- здесь была нажата кнопка -------</i>")  # помечаю места откуда исчезли кнопки
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
    await call.message.answer("<i>------- здесь была нажата кнопка -------</i>")  # помечаю места откуда исчезли кнопки
    await call.message.answer("В предвкушении потираю лапы! Но, перед тем как приступить, предлагаю познакомиться с "
                              "<b><i>Эмоциональным термометром</i></b>. Это нужно, чтобы мы быстро и точно могли "
                              "измерить твою «эмоциональную температуру».", reply_markup=choice03)
    await Start.Call_02.set()  # или можно await Start.next()


# Обработчик нажатия кнопки "Интересно!"
@dp.callback_query_handler(text="choice:Start_Call02:Интересно!", state=Start.Call_02)
async def press_call02_key2(call: CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<i>------- здесь была нажата кнопка -------</i>")  # помечаю места откуда исчезли кнопки
    await call.message.answer("Это шкала из 27 эмоций, расположенных по интенсивности, с помощью которой ты "
                              " ориентироваться в своем состоянии. Всегда обращайся к ней, особенно по началу, "
                              "чтобы дать максимально точный ответ, который я смогу считать и зафиксировать.",
                              reply_markup=choice04)


# Обработчик нажатия кнопки "Уже_знаком"
@dp.callback_query_handler(text="choice:Start_Call02:Уже_знаком", state=Start.Call_02)
async def press_call02_key2(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.answer("<i>------- здесь была нажата кнопка -------</i>")  # помечаю места откуда исчезли кнопки
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
    await call.message.answer("<i>------- здесь была нажата кнопка -------</i>")  # помечаю места откуда исчезли кнопки
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
                             " тебе интересное задание на «прокачку». Постарайся выполнить его честно и быстро - это"
                             " ОЧЕНЬ ВАЖНО! ")
        await message.answer("Отлично, {0}! Блок ознакомительной информации закончен, можно "
                             "перейти к настройкам времени опроса...".format(name_user))
        await set_settings()  # следующее состояние установится внутри этой функции
    else:
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую интерес</i></b>".format(name_user))


# Функция для настроек времени опроса бота (при вызове в период опроса м.б. прервана без записи в БД)
async def set_settings():
    await Start.Q6.set()  # или можно await Start.next()
"""
     # my_comm.c_sett(message)
        curr_data = datetime.datetime.now()
        curr_time = curr_data.time()
        gv.bot.send_message(message.chat.id,
                            "Текущее время {0:0>2}:{1:0>2}".format(curr_time.hour, curr_time.minute))
        gv.bot.send_message(message.from_user.id, "{0}, пожалуйста, введи удобное время начала опроса в "
                                                  "часах от 0 до 22".format(name_user))
"""
