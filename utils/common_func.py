# Модуль общих функций (Common functions)
from asyncio import sleep
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from random import choice
import datetime
import logging

from loader import SEC_IN_H, SEC_IN_M, HOUR_IN_DAY, LAST_DAY
from states.states import Start, Pool, Task02, Task03, Task04, Task05, Task06, Task07, Task08, Task09, Task10, Task11, \
    Task12, Task13, Task14
from keyboards.default.menu import menu, pool, tsk02_00, tsk02_01
from utils.db_api.db_commands import db_update_user_settings, stat_five_emotions, upload_xls, db_update_current_day


# Ввод неотрицательного числа
async def get_digit(message: Message, state: FSMContext, d_min: int, d_max: int):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    try:
        d = int(message.text)  # проверяем, что цифра введена корректно
    except Exception as e:
        await message.answer('Ошибка: {0}'.format(e))
        await message.answer('{0}, введи цифрами, пожалуйста!'.format(name_user))
        d = -1
    else:
        if d < d_min or d > d_max:
            await message.answer('{0}, введи значение от {1} до {2}, пожалуйста!'.format(name_user, d_min, d_max))
            d = -2
    return d


# Бесконечный цикл действия ботика
async def loop_action(message: Message, state: FSMContext):
    t = await get_time_next_action(state, 1)  # первый запуск
    while True:
        data = await state.get_data()
        name_user = data.get("name_user")
        tmz = data.get("tmz")
        prev_data = data.get("prev_data")
        current_day = data.get("current_day")
        flag_pool = data.get("flag_pool")
        flag_task = data.get("flag_task")
        # тайм-аут до начала следующего действия
        logging.info('loop_action 0: засыпаю на {0} сек, prev_data={1} current_day='
                     '{2}'.format(t, prev_data, current_day))
        await sleep(t)
        # Рассчет и изменение номера текущего дня
        c_data = datetime.datetime.now() + datetime.timedelta(hours=tmz)
        if SEC_IN_H == 3600:  # Проверяем работаем ли мы по боевому или в режиме отладки
            c_day = c_data.day
        else:
            c_day = c_data.hour
        if c_day != prev_data:
            current_day = current_day + 1
            if current_day > LAST_DAY:  # проверяем условие на завершение работы
                await run_bye(message, state)
                return
            await state.update_data(current_day=current_day)
            await db_update_current_day(message.from_user.id, current_day=current_day)
            prev_data = c_day
            await state.update_data(prev_data=prev_data)
            await message.answer('<code>=== начался {0}-й день ===</code>'.format(current_day))
        logging.info('loop_action 1: c_day={0} prev_data={1} current_day={2}'.format(c_day, prev_data, current_day))
        # Проверка закончил ли пользователь за тайм-аут с предыдущим опросом/задачей/настройкой (<-можно детализировать)
        c_state = await state.get_state()
        logging.info('loop_action 2: c_state={0}'.format(c_state))
        if c_state == "None":  # дополнительная проверка завершения цикла по команде /stop
            return
        if c_state != "Start:Wait":
            c_state = c_state[:4]  # берем только название класса без состояния
            if c_state == "Pool":
                await message.answer('Прошлое напоминание пропущено', reply_markup=menu)
            elif c_state == "Task":
                await message.answer('Решение задачки пропущено', reply_markup=menu)
            else:  # или было можно сделать elif c_state == "Sett":
                await message.answer('Изменение настроек пропущено'.format(name_user), reply_markup=menu)
        # Запуск следующего действия и рассчет времени сна с установкой флагов
        logging.info('loop_action 3: flag_pool={0} flag_task={1}'.format(flag_pool, flag_task))
        if flag_pool and flag_task:
            await run_poll_task(message, state)  # запуск опроса с последующим запуском задачи
        elif flag_pool:
            await run_poll(message, state)  # запуск  одного опроса
        elif flag_task:  # можно было бы поставить else, но пусть для надежности будет так
            await run_task(message, state)  # запуск одной задачи
        t = await get_time_next_action(state, 0)


# Определяем время до следующего действия в секундах
async def get_time_next_action(state: FSMContext, flag: int) -> int:
    data = await state.get_data()  # Достаем имя пользователя
    tmz = data.get("tmz")
    start_t = data.get("start_t")
    end_t = data.get("end_t")
    period = data.get("period")
    tsk_t = data.get("tsk_t")
    c_data = datetime.datetime.now() + datetime.timedelta(hours=tmz)
    flag_pool = 1  # взводим флажок выполнения опроса
    flag_task = 0  # сбрасываем флажок выполнения задачи
    # Проверяем работаем ли мы по боевому или в режиме отладки
    if SEC_IN_H == 3600:
        c_hour = c_data.hour
        c_minute = c_data.minute
    else:
        c_hour = c_data.minute
        c_minute = c_data.second
    # обработка 1го вызова функции
    if flag:
        if SEC_IN_H == 3600:  # инициализируем prev_data
            prev_data = c_data.day
        else:
            prev_data = c_data.hour
        await state.update_data(prev_data=prev_data)
        if c_hour < start_t:  # настройки завершены сегодня до наступления начала опроса
            t = (start_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
            current_day = data.get("current_day")
            if current_day == 0:
                await state.update_data(current_day=1)  # считаем, что пошел 1-й день опроса
        else:  # настройки завершены после наступления начала опроса - выполнение опроса начнется завтра
            t = ((HOUR_IN_DAY - c_hour) * SEC_IN_H - c_minute * SEC_IN_M) + start_t * SEC_IN_H
        if tsk_t == start_t:
            flag_task = 1
            await state.update_data(flag_task=flag_task)  # взводим флажок выполнения задачи
        logging.info('g_t_n_a 0: c_hour={0} c_minute={1} start_t={2} prev_data={3} flag_task={4} t='
                     '{5}'.format(c_hour, c_minute, start_t, prev_data, flag_task, t))
        return t + 10  # запас надежности в 10 секунд
    # обработка вызова функции из цикла действий
    if c_hour >= end_t:  # рассчет времени задержки после завершения опроса в текущем дне
        t = ((HOUR_IN_DAY - c_hour) * SEC_IN_H - c_minute * SEC_IN_M) + start_t * SEC_IN_H
        if tsk_t == start_t:
            flag_task = 1
    elif c_hour < start_t:  # никогда не должно выполниться (раньше- выполнится если задержали ответ на последний опрос)
        t = (start_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
        if tsk_t == start_t:
            flag_task = 1
        logging.info('g_t_n_a 1: !!_ЧУШЬ_!! c_hour={0} c_minute={1} start_t={2} flag_task={3} t='
                     '{4}'.format(c_hour, c_minute, start_t, flag_task, t))
    else:  # рассчет времени задержки в рамках опроса текущего дня
        p = period
        while c_hour >= start_t + p:  # находим час следующего опроса
            p = p + period
        # м.б. следующей должна выполняться задача? (+ м.б. без опроса?) - помним, что tsk_t <= end_t
        if (start_t + p >= tsk_t) and (tsk_t > c_hour):
            t = (tsk_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
            flag_task = 1  # взводим флажок выполнения задачи
            if (start_t + p > tsk_t) and (tsk_t < end_t):
                flag_pool = 0  # опускаем флажок выполнения опроса
        elif start_t + p > end_t:  # вышли за время опроса из-за сокращенного последнего врменного отрезка
            t = (end_t - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
        else:  # расчет задержки в рамках опроса без необходимости запуска задачи
            t = (start_t + p - c_hour) * SEC_IN_H - c_minute * SEC_IN_M
    await state.update_data(flag_pool=flag_pool)
    await state.update_data(flag_task=flag_task)
    logging.info('g_t_n_a 2: c_hour={0} c_minute={1} start_t={2} end_t={3} flag_pool={4} flag_task={5} t='
                 '{6}'.format(c_hour, c_minute, start_t, end_t, flag_pool, flag_task, t))
    return t + 10  # запас надежности в 10 секунд


# Штатное завершение работы бота
async def run_bye(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    sti = open("./a_stickers/AnimatedSticker2.tgs", 'rb')  # Приветствует воздушным поцелуем
    await message.answer_sticker(sticker=sti)
    await message.answer("Мы полезно с тобой пообщались, {0}! До новых встреч!".format(name_user),
                         reply_markup=ReplyKeyboardRemove())
    await state.reset_state()  # для сохранения данных в data можно писать await state.reset_state(with_data=False)
    filename = await upload_xls(message.from_user.id)
    file = open(filename, "rb")
    await message.answer_document(file, caption="Выгрузка зарегистрированных эмоций")
    str0 = await stat_five_emotions(message.from_user.id)
    await message.answer(str0)
    await db_update_user_settings(message.from_user.id, name=data.get("name_user"), start_time=data.get("start_t"),
                                  period=data.get("period"), end_time=data.get("end_t"), zone_time=data.get("tmz"),
                                  current_day=data.get("current_day"), task_time=data.get("tsk_t"))
    logging.info("run_bye 0: Бот пользователя {0}(id={1}) штатно завершил работу. "
                 "current_day={2}".format(name_user, message.from_user.id, current_day))


# ===================== Блок функций вытащенных из других модулей для инкапсуляции common_func.py =====================
quest = [", что ты сейчас чувствуешь?", ", какая эмоция сейчас внутри тебя?",
         ", прислушайся какая эмоция сейчас внутри тебя?", ", тук-тук-тук, что ты сейчас чувствуешь?"]
r_p = "{0}{1}"


# Запуск опроса эмоции
async def run_poll(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker3.tgs", 'rb')  # Приветствует наступив на хвост мышке
    await message.answer_sticker(sticker=sti)
    await message.answer(r_p.format(name_user, choice(quest)), reply_markup=pool)
    await Pool.Emo.set()


# Запуск опроса эмоции c последующим запуском задачи
async def run_poll_task(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    sti = open("./a_stickers/AnimatedSticker3.tgs", 'rb')  # Приветствует наступив на хвост мышке
    await message.answer_sticker(sticker=sti)
    await message.answer(r_p.format(name_user, choice(quest)), reply_markup=pool)
    await Pool.EmoTask.set()


async def run_task(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    current_day = data.get("current_day")
    # начинаем выполнение задачки
    if current_day != 0 and current_day != 1:
        sti = open("./a_stickers/AnimatedSticker4.tgs", 'rb')  # Пускает праздничный салют
        await message.answer_sticker(sticker=sti)
        await message.answer('{0}, пришло время для «задачки на прокачку»!'.format(name_user))
        logging.info("run_task 0: current_day={0}".format(current_day))
    if current_day == 2:  # на 2-й (не на 0-й и 1-й) день работы боты запускаем задачи
        await run_tsk02(message, state)
    elif current_day == 3:
        await run_tsk03(message, state)
    elif current_day == 4:
        await run_tsk04(message, state)
    elif current_day == 5:
        await run_tsk05(message, state)
    elif current_day == 6:
        await run_tsk06(message, state)
    elif current_day == 7:
        await run_tsk07(message, state)
    elif current_day == 8:
        await run_tsk08(message, state)
    elif current_day == 9:
        await run_tsk09(message, state)
    elif current_day == 10:
        await run_tsk10(message, state)
    elif current_day == 11:
        await run_tsk11(message, state)
    elif current_day == 12:
        await run_tsk12(message, state)
    elif current_day == 13:
        await run_tsk13(message, state)
    elif current_day == 14:
        await run_tsk14(message, state)
    else:  # переходим в состояние ожидания следующего действия
        sti = open("./a_stickers/AnimatedSticker8.tgs", 'rb')  # Идет с закрытыми глазами по беговой дорожке
        await message.answer_sticker(sticker=sti)
        await message.answer('{0}, для {1}-го дня нет ”задачки на прокачку” - можешь просто немного '
                             'помедитировать вместе со мной... 😊'.format(name_user, current_day), reply_markup=menu)
        await Start.Wait.set()


# Запуск "задачки на прокачку" 2-го дня
async def run_tsk02(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer("{0}, я приготовил для тебя «задачку на прокачку» эмоционального интеллекта. Если ты будешь вы"
                         "полнять все «задачки на прокачку» твоя эмоциональная форма станет сильнее и пластичнее. Сегод"
                         "ня будем прокачивать эмоциональную мышцу, которая отвечает за распознавание эмоций. Если тебе"
                         " интересно узнать, какие еще мышцы мы будем тренировать в предстоящие 2 недели, кликни на слу"
                         "жебное сообщение «Модель эмоционального интеллекта» под строкой ввода текста или на «Выполнит"
                         "ь позже!».".format(name_user),
                         reply_markup=tsk02_00)
    await Task02.Answer_02_01.set()


# Запуск "задачки на прокачку" 3-го дня
async def run_tsk03(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Вчера мы с тобой были в картинной галерее, а сегодня я тебя приглашаю "
                         "на секретное здание в филармонию. Надень наушники и прослушай последовательно три музыкальных"
                         "фрагмента. Слушай внимательно, можешь даже закрыть глаза. Почувствуй, какую эмоцию у тебя"
                         " вызывает эта музыка. Если готов начать кликни на служебное сообщение «Выполнить сейчас!» под"
                         " строкой ввода текста или на «Выполнить позже!».".format(name_user), reply_markup=tsk02_01)
    await Task03.Answer_03_01.set()


# Запуск "задачки на прокачку" 4-го дня
async def run_tsk04(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    await message.answer('Привет, {0}! Очередная "задачка на прокачку" эмоционального интеллекта готова.\nПредлагаю '
                         'кликнуть на служебное сообщение «Выполнить сейчас!» под строкой ввода текста или на '
                         '«Выполнить позже!»'.format(name_user), reply_markup=tsk02_01)
    await Task04.Answer_04_01.set()


# Запуск "задачки на прокачку" 5-го дня
async def run_tsk05(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Я заметил, что мое настроение не всегда совпадает с настроением моей команды. На"
                         "верное, и у тебя такое бывало: то шеф не в духе, а то коллега, наоборот, подозрительно "
                         "весел.".format(name_user))
    await message.answer("Вот тебе задачка на прокачку!\n Мы с командой как раз пересматривали советскую классику кинем"
                         "атографа и нашли интересный фрагмент в фильме “Служебный роман”. Попробуй посмотреть его и оп"
                         "ределить, какие эмоции испытывал Новосельцев в этом фрагменте. Если готов начать кликни на сл"
                         "ужебное сообщение «Выполнить сейчас!» под строкой ввода текста или на «Выполнить позже!»"
                         ".", reply_markup=tsk02_01)
    await Task05.Answer_05_01.set()


# Запуск "задачки на прокачку" 6-го дня
async def run_tsk06(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Сегодня тебе предстоит непростая «задачка на прокачку». Я уверен, что сегодня"
                         " ты обязательно сделаешь маленькие открытия в области своих эмоций.".format(name_user),
                         reply_markup=tsk02_01)
    await Task06.Answer_06_01.set()


# Запуск "задачки на прокачку" 7-го дня
async def run_tsk07(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Уверен, ты готов к новому заданию. Мы с моей командой часто"
                         " играем в игру «Что испытываю?». Задача простая – я задаю ситуацию, а ты "
                         "определяешь эмоцию. Сыграем сейчас?".format(name_user), reply_markup=tsk02_01)
    await Task07.Answer_07_01.set()


# Запуск "задачки на прокачку" 8-го дня
async def run_tsk08(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Сегодня мы потренируемся анализировать и понимать причины эмоций свои и "
                         "других.  Если готов начать кликни на служебное сообщение «Выполнить сейчас!» под строкой "
                         "ввода текста или на «Выполнить позже!».".format(name_user), reply_markup=tsk02_01)
    await Task08.Answer_08_01.set()


# Запуск "задачки на прокачку" 9-го дня
async def run_tsk09(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Я приготовил для тебя очередную «задачку на прокачку» эмоционального "
                         "интеллекта. Сегодня будем прокачивать мышцу понимания "
                         "причин эмоций".format(name_user), reply_markup=tsk02_01)
    await Task09.Answer_09_01.set()


# Запуск "задачки на прокачку" 10-го дня
async def run_tsk10(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет-привет, {0}! А у нас радостное событие –  юбилей 😊 !\nУже 10-ый день мы с тобой "
                         "общаемся и изучаем эмоциональный интеллект! Я так рад, что не могу сосредоточиться "
                         "и заполнить отчет за прошедшие дни. Поэтому, решил применить свою эмоцию для мотивации"
                         " команды на новые свершения и провести с ними мозговой штурм, чтобы придумать "
                         "интересные задачки на прокачку.\n"
                         "Сильные приятные эмоции помогают в решении "
                         "таких задач.".format(name_user), reply_markup=tsk02_01)
    await Task10.Answer_10_01.set()


# Запуск "задачки на прокачку" 11-го дня
async def run_tsk11(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("И снова здравствуй, {0}! Надеюсь, не отвлекаю? А то мое"
                         " появление может вызвать разные эмоции :-)".format(name_user), reply_markup=pool)
    await message.answer("Кстати, а что ты сейчас чувствуешь?")
    await Task11.Answer_11_01.set()


# Запуск "задачки на прокачку" 12-го дня
async def run_tsk12(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Хочу поделиться с тобой своим «происшествием». Недавно мне нужно было выступать "
                         "перед коллегами из другого чат-бота, и я почувствовал страх. Мне хотелось закрыться лапками и"
                         " спрятаться под стул. Ты уже знаешь, что эффективно использовать эмоцию страха в такой ситуац"
                         "ии не получится. В тот момент пришлось разозлиться, чтобы выступить более ярко и всем доказат"
                         "ь, что наш чат-бот намного лучше.".format(name_user))
    await message.answer("Чтобы управлять своими эмоциями, я использовал “Пульт управления эмоциями” и переключился на "
                         "злость с помощью тела. У каждой эмоции есть свое проявление в теле: когда мы в восторге, то н"
                         "ачинаем прыгать и хлопать в ладоши. А когда в горе, то наши плечи опускаются и все тело сутул"
                         "ится. Зная как и где в теле проявляются эмоции, я могу вызвать их, сделав «портрет этой эмоци"
                         "и», то есть приняв нужную позу и используя соответствующие жесты.\nИ вот что я делал, чтобы п"
                         "ереключиться в эмоцию злости через тело:\n- Импульсивные резкие движения\n- Пристально посмот"
                         "рел в сторону, напрягая нижнее веко\n- Плотно сжал губы")
    await message.answer("Сегодня мы поучимся управлению эмоциями через своё тело. Если готов начать кликни на служебно"
                         "е сообщение «Выполнить сейчас!» под строкой ввода текста или на «Выполнить позже!"
                         "»".format(name_user), reply_markup=tsk02_01)
    await Task12.Answer_12_01.set()


# Запуск "задачки на прокачку" 13-го дня
async def run_tsk13(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! У «Пульта управления эмоциями» несколько кнопок."
                         " Вчера ты познакомился с одной из них – «Тело». Сегодня мы поговорим"
                         ", как можно работать с эмоциями "
                         "через Речь/Мышление. ".format(name_user), reply_markup=tsk02_01)
    await Task13.Answer_13_01.set()


# Запуск "задачки на прокачку" 14-го дня
async def run_tsk14(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Привет, {0}! Я приготовил для тебя «задачку на прокачку» "
                         "мышцы эмоционального интеллекта, связанной с управлением"
                         " собственными эмоциями.".format(name_user), reply_markup=tsk02_01)
    # await message.answer("Кстати, а что ты сейчас чувствуешь?") - !обработчика ввода эмоции нет
    await Task14.Answer_14_01.set()
