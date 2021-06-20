# В этом модуле выполняется обработка сообщений из текстового меню
import datetime
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.states import Sett, Start
from utils.common_func import get_digit, run_poll, run_task
from utils.db_api.db_commands import db_update_user_settings


Possible_Emotions = ['злость', 'трепет', 'угрюмость', 'отчужденность',
                     'гнев', 'обеспокоенность ', 'серьезность', 'неловкость',
                     'возмущение', 'испуг', 'подавленность', 'удивление',
                     'ненависть', 'тревога', 'разочарование', 'шок',
                     'обида', 'волнение', 'боль', 'поражение',
                     'сердитость', 'боязнь', 'застенчивость', 'остолбенение',
                     'досада', 'ужас', 'покинутость', 'изумление',
                     'раздражение', 'ощущение угрозы', 'удрученность', 'потрясение',
                     'оскорбленность', 'ошеломленность', 'усталость', 'энтузиазм',
                     'воинственность', 'опасение', 'глупость', 'восторг',
                     'бунтарство', 'уныние', 'апатия', 'возбужденность',
                     'сопротивление', 'ощущение тупика', 'самодовольство', 'страсть',
                     'зависть', 'запутанность', 'скука', 'эйфория',
                     'надменность', 'потерянность', 'истощение', 'трепет',
                     'презрение', 'дезориентация', 'расстройство', 'решимость',
                     'отвращение', 'бессвязность', 'упадок сил', 'дерзость',
                     'подавленность', 'одиночество', 'нетерпеливость', 'удовлетворенность',
                     'уязвленность', 'изолированность', 'вспыльчивость', 'гордость',
                     'подозрительноость', 'грусть', 'тоска', 'сентиментальность',
                     'настороженность', 'печаль', 'стыд', 'счастье',
                     'озабоченность', 'горе', 'вина', 'радость',
                     'тревожность', 'угнетенность', 'униженность', 'блаженство',
                     'страх', 'мрачность', 'ущемленность', 'забавность',
                     'нервозность', 'отчаяние', 'смущение', 'восхищение',
                     'ожидание', 'опустошенность', 'неудобство', 'триумф',
                     'взволнованность', 'беспомощность', 'тяжесть', 'удовольствие',
                     'слабость', 'сожаление', 'мечтательность',
                     'ранимость', 'скорбь', 'очарование',
                     'неудовольствие', 'растерянность ', 'принятие']


@dp.message_handler(Text(equals="Список эмоций и чувств"), state='*')
async def get_list(message: Message):
    str1 = "<pre>"
    index = 1
    for iter2 in Possible_Emotions:
        str1 += "{0:16s} ".format(iter2)
        if index % 2 == 0:
            str1 += "\n"
        index += 1
    str1 += "</pre>"
    await message.answer(str1)


@dp.message_handler(Text(equals="Термометр"), state='*')
async def get_list(message: Message):
    img = open("./IMG/Термометр.jpg", "rb")
    await message.answer_photo(img)


@dp.message_handler(Text(equals="Фиксировать эмоцию сейчас"), state='*')
async def get_emo(message: Message, state: FSMContext):
    c_state = await state.get_state()
    if c_state != "Start:Wait":
        data = await state.get_data()
        name_user = data.get("name_user")
        await message.answer('{0}, для внеочередной фиксации эмоции сначала заверши ответ на текущий '
                             'вопрос!'.format(name_user))
        return
    await run_poll(message, state)


@dp.message_handler(Text(equals="Выполнить ”задачку на прокачку”"), state='*')
async def get_tsk(message: Message, state: FSMContext):
    c_state = await state.get_state()
    if c_state != "Start:Wait":
        data = await state.get_data()
        name_user = data.get("name_user")
        await message.answer('{0}, для внеочередного выполнения задачки ”на прокачку”" сначала заверши ответ на'
                             ' текущий вопрос!'.format(name_user))
        return
    await run_task(message, state)


@dp.message_handler(Text(equals="Настройки"), state='*')
async def set_sett(message: Message, state: FSMContext):
    c_state = await state.get_state()
    data = await state.get_data()
    name_user = data.get("name_user")
    tmz = data.get("tmz")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    period = data.get("period")
    tsk_t = data.get("tsk_t")
    if c_state != "Start:Wait":
        await message.answer('{0}, для изменения настроек работы сначала заверши ответ на текущий вопрос'
                             '!'.format(name_user))
        return
    await message.answer('{0}, с помощь ввода соответствующего номера (1 - 7) выбери изменяемый параметр (изменение '
                         'времени опроса применятся после твоего следующего ответа):\n1. Имя ({1})\n2. Часовой пояс '
                         '(+{2})\n3. Время начала опроса ({3:0>2}:00)\n4. Время завершения опроса ({4:0>2}:00)\n'
                         '5. Периодичность опроса ({5})\n6. Время выполнения задачи ({6:0>2}:00)\n'
                         '7. Отмена'.format(name_user, name_user, tmz, start_t, end_t, period, tsk_t))
    await Sett.next()


@dp.message_handler(state=Sett.Stage0)
async def set_sett_0(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    # Время начала опроса start_t(int),\
    # Время завершения опроса end_t(int),\
    d = await get_digit(message, state, 1, 7)
    if d < 0:  # проверка коррктностии ввода пользователя
        return
    if d == 1:
        await message.answer('{0}, введи свое новое имя:'.format(name_user))
        await Sett.next()
    elif d == 2:
        c_data = datetime.datetime.now()
        await message.answer("Давай сверим наши часы!\nМое текущее время: "
                             "{0:0>2}:{1:0>2}.".format(c_data.hour, c_data.minute))
        await message.answer("{0}, пожалуйста, введи <i>одним числом в часах</i> от 0 до 23 <b>разницу с "
                             "твоим текущим временем</b>:".format(name_user))
        await Sett.Stage2.set()
    elif d == 3:
        await message.answer('{0}, введи <i>одним числом в часах</i> удобное <b>время начала опроса</b>'
                             ' от 0 до {1}:'.format(name_user, end_t-1))
        await Sett.Stage3.set()
    elif d == 4:
        await message.answer('{0}, введи <i>одним числом в часах</i> удобное <b>время завершения опроса</b>'
                             ' от {1} до 23:'.format(name_user, start_t+1))
        await Sett.Stage4.set()
    elif d == 5:
        await message.answer('{0}, введи <i>одним числом в часах</i> удобную <b>периодичность опроса</b>'
                             ' от 1 до 4:'.format(name_user))
        await Sett.Stage5.set()
    elif d == 6:
        await message.answer('{0}, введи <i>одним числом в часах</i> удобное <b>время выполнения задачки'
                             ' ”на прокачку”</b> от {1} до {2} (если время задачки и время опроса совпадут, выполнение '
                             'задачки начнется сразу после опроса):'.format(name_user, start_t, end_t))
        await Sett.Stage6.set()
    else:
        await message.answer('Внесение изменения в настройки отменено.')
        await Start.Wait.set()


@dp.message_handler(state=Sett.Stage1)
async def set_sett_1(message: Message, state: FSMContext):
    name_user = message.text[:20]
    await state.update_data(name_user=name_user)
    await message.answer('Теперь я буду звать тебя "{0}".'.format(name_user))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()


@dp.message_handler(state=Sett.Stage2)
async def set_sett_2(message: Message, state: FSMContext):
    d = await get_digit(message, state, 0, 23)
    if d < 0:
        return
    await state.update_data(tmz=d)
    c_data = datetime.datetime.now() + datetime.timedelta(hours=d)
    await message.answer("Мое текущее время стало {0:0>2}:{1:0>2}.".format(c_data.hour, c_data.minute))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()


@dp.message_handler(state=Sett.Stage3)
async def set_sett_3(message: Message, state: FSMContext):
    data = await state.get_data()
    end_t = data.get("end_t")
    d = await get_digit(message, state, 0, end_t-1)
    if d < 0:
        return
    await state.update_data(start_t=d)
    await message.answer("Итак, начало опроса в {0:0>2}:00.".format(d))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()


@dp.message_handler(state=Sett.Stage4)
async def set_sett_4(message: Message, state: FSMContext):
    data = await state.get_data()
    start_t = data.get("start_t")
    d = await get_digit(message, state, start_t+1, 23)
    if d < 0:
        return
    await state.update_data(end_t=d)
    await message.answer("Итак, завершение опроса в {0:0>2}:00.".format(d))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()


@dp.message_handler(state=Sett.Stage5)
async def set_sett_5(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 4)
    if d < 0:
        return
    data = await state.get_data()  # Достаем имя пользователя
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    await state.update_data(period=d)
    await message.answer("Итак, я буду опрашивать что ты чувствуешь в:")
    i = 0
    while start_t + i < end_t:
        await message.answer("{0:0>2}:00".format(start_t + i))
        i = i + d
    await message.answer("и {0:0>2}:00".format(end_t))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()


@dp.message_handler(state=Sett.Stage6)
async def set_sett_6(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    d = await get_digit(message, state, start_t, end_t)
    if d < 0:
        return
    await state.update_data(tsk_t=d)
    await message.answer('Итак, выполнение задачки ”на прокачку” в: {0:0>2}:00'.format(d))
    await message.answer('Внесение изменения в настройки завершено.')
    data = await state.get_data()
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    await Start.Wait.set()
