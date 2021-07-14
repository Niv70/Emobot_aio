# В этом модуле выполняется обработка сообщений для задачи 8-го дня
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, pool, tsk08_11, tsk04_10
from loader import dp
from states.states import Start, Task08
from utils.common_func import get_digit
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_01)
async def answer_08_01(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text
    if s == "Выполнить сейчас!":
        await message.answer("Твоя задача - определить, что является причиной той или иной эмоции. Я уверен, ты справиш"
                             "ься!\nУгроза является причиной (ответь вводом цифры от 1 до 8):\n1. Злости\n2. Радости\n3"
                             ". Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. Удивления",
                             reply_markup=pool)
    elif s == "Выполнить позже!":
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке до начала следующего дня.",
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода текста или на «В"
                             "ыполнить позже!»".format(name_user))
        return
    await Task08.next()


# Обработчик ввода 2го ответа (4.Страх) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_02)
async def answer_08_02(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 4 - Страх, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 4:
        await message.answer("Верно! Обычно, это причина <b><i>страха</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>страха</i></b> (цифра 4)"
                             ".".format(name_user))
    await message.answer("Утрата/потеря являются причиной (ответь вводом цифры от 1 до 8):\n1. Злости\n2. Радости\n3"
                         ". Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. Удивления")
    await Task08.next()


# Обработчик ввода 3го ответа (3.Печаль) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_03)
async def answer_08_03(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 3 - Печаль, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 3:
        await message.answer("Верно! Обычно, это причина <b><i>печали</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>печали</i></b> (цифра 3)"
                             ".".format(name_user))
    await message.answer("Отторжение вещей, людей является причиной (ответь вводом цифры от 1 до 8):\n1. Злости\n2. Рад"
                         "ости\n3. Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. Удивления")
    await Task08.next()


# Обработчик ввода 4го ответа (7.Отвращение) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_04)
async def answer_08_04(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 7 - Отвращение, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 7:
        await message.answer("Верно! Обычно, это причина <b><i>отвращения</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>отвращения</i></b> (цифра 7)"
                             ".".format(name_user))
    await message.answer("Получение желаемого, приобретение чего-то полезного является причиной (ответь вводом цифры от"
                         " 1 до 8):\n1. Злости\n2. Радости\n3. Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращени"
                         "я\n8. Удивления")
    await Task08.next()


# Обработчик ввода 5го ответа (1.Радость) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_05)
async def answer_08_05(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 2 - Радость, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 2:
        await message.answer("Верно! Обычно, это причина <b><i>радости</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>радости</i></b> (цифра 2)"
                             ".".format(name_user))
    await message.answer("Получение новой полезной информации является причиной (ответь вводом цифры от 1 до 8):\n1. Зл"
                         "ости\n2. Радости\n3. Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. Удивления")
    await Task08.next()


# Обработчик ввода 6го ответа (5.Интерес) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_06)
async def answer_08_06(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 5 - Интерес, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 5:
        await message.answer("Верно! Обычно, это причина <b><i>интереса</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>интереса</i></b> (цифра 5)"
                             ".".format(name_user))
    await message.answer("Появление неожиданного, необычного, странного является причиной (ответь вводом цифры от 1 до "
                         "8):\n1. Злости\n2. Радости\n3. Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. "
                         "Удивления")
    await Task08.next()


# Обработчик ввода 7го ответа (8.Удивление) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_07)
async def answer_08_07(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 8 - Удивление, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 8:
        await message.answer("Верно! Обычно, это причина <b><i>удивления</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>удивления</i></b> (цифра 8)"
                             ".".format(name_user))
    await message.answer("Принятие ситуации и другого является причиной (ответь вводом цифры от 1 до 8):\n1. Злости\n2"
                         ". Радости\n3. Печали\n4. Страха\n5. Интереса\n6. Доверия\n7. Отвращения\n8. Удивления")
    await Task08.next()


# Обработчик ввода 8го ответа (6.Доверие) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_08)
async def answer_08_08(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 6 - Доверие, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 6:
        await message.answer("Верно! Обычно, это причина <b><i>доверия</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>доверия</i></b> (цифра 6)"
                             ".".format(name_user))
    await message.answer("Недосягаемость желаемого, препятствия, несправедливость, отстаивание «своих границ» являются "
                         "причиной (ответь вводом цифры от 1 до 8):\n1. Злости\n2. Радости\n3. Печали\n4. Страха\n5. Ин"
                         "тереса\n6. Доверия\n7. Отвращения\n8. Удивления")
    await Task08.next()


# Обработчик ввода 9го ответа (1.Злость) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_09)
async def answer_08_09(message: Message, state: FSMContext):
    d = await get_digit(message, state, 1, 8)
    if d < 0:
        return
    s = "Д.б. 1 - Злость, ответ - {}".format(d)
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    if d == 1:
        await message.answer("Верно! Обычно, это причина <b><i>злости</i></b>.")
    else:
        await message.answer("{}, большинство людей ответили бы, что это причина <b><i>злости</i></b> (цифра 1)"
                             ".".format(name_user))
    await message.answer("Ты замур-р-р-чательно справился с универсальными причинами! А как ты думаешь, могут быть у на"
                         "с  свои причины возникновения эмоций? Конечно!!!! Эмоции очень тесно связаны с ценностями"
                         " человека, а они у каждого свои. Знай, если в процессе общения с тобой возникла сильная эмоци"
                         "я, то ты затронул какую-либо его ценность. И интенсивность эмоции будет показывать на степень"
                         " ее значимости. Вот тебе основное задание:\nПредстав"
                         "ь, что ты руководитель отдела. Вы получили в реализацию новый интересный и сложный проект, од"
                         "нако, чтобы завершить его в срок, потребуется неделю работать сверхурочно. Ты пригласил колле"
                         "г, которые задействованы в проекте, чтобы сообщить эту новость.")
    await message.answer("Какую эмоцию от этой новости испытает сотрудник с сильной ценностью «Семья»? (ответь вводом о"
                         "дного слова-эмоции)")
    await Task08.next()


# Обработчик ввода 10го ответа (Эмоция 1) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_10)
async def answer_08_10(message: Message):
    s = message.text[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 8, s)
    await message.answer("Какую эмоцию от этой новости испытает сотрудник с сильной ценностью «Самореализация»? (ответь"
                         " вводом одного слова-эмоции)")
    await Task08.next()


# Обработчик ввода 11го ответа (Эмоция 2) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_11)
async def answer_08_11(message: Message, state: FSMContext):
    s = message.text[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 8, s)
    data = await state.get_data()
    name_user = data.get("name_user")
    await message.answer("Я тут примерил эти ценности на себя и понял, что в первом случае я бы очень <b><i>злился</i>"
                         "</b>, что рушатся семейные планы, а во втором, наоборот, <b><i>радовался</i></b>, что появила"
                         "сь возможность реализовать свой потенциал. Как по-разному мы можем чувствовать себя в одних и"
                         " тех ж"
                         "е ситуациях 😊\nЗная причину, ты можешь предположить, какую эмоцию испытает человек, как он б"
                         "удет реагировать, и выбрать для себя нужную стратегию поведения с ним. А еще важно понимать, "
                         "что эмоции разные по интенсивности, и сильные эмоции сразу не возникают, как правило, им пред"
                         "шествуют менее интенсивные.")
    await message.answer("{0}, предлагаю кликнуть на служебное сообщение «Показать пример» под строкой ввода"
                         " текста".format(name_user), reply_markup=tsk08_11)
    await Task08.next()


# Обработчик ввода 12го ответа (Показать пример) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_12)
async def answer_08_12(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Показать пример":
        await message.answer("Например, сотрудник работает над задачей, требующей предельной внимательности, и уже сдел"
                             "ал несколько ошибок, т.к. не может сконцентрироваться из-за громких разговоров коллег из "
                             "отдела. Какую эмоцию он испытывает? Верно, пока <b><i>раздражение</i></b>. Он просит колл"
                             "ег разговаривать тише, но через несколько минут о тишине никто не помнит. И тут интенсивн"
                             "ость эмоции возрастает и раздражение перерастает в <b><i>злость</i></b>. Если коллеги по-"
                             "прежнему не услышат его, то и до <b><i>гнева</i></b> недалеко!")
        await message.answer("{0}, предлагаю кликнуть на служебное сообщение «Завершить упражнение» под строкой ввода"
                             " текста".format(name_user), reply_markup=tsk04_10)
    else:
        await message.answer("{}, кликни на служебное сообщение «Показать пример» под строкой ввода текста"
                             ".".format(name_user))
        return
    await Task08.next()


# Обработчик ввода 13го ответа (Завершить упражнение) к задачке "на прокачку" 8-го дня
@dp.message_handler(state=Task08.Answer_08_13)
async def answer_08_13(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Завершить упражнение":
        await message.answer("Ты ударно потрудился, и за это я готов поделиться с тобой секретом, который поможет стать"
                             " Повелителем эмоций:\n<b><i>Чем ниже интенсивность эмоции, тем легче ей управлять</i></b>"
                             "!", reply_markup=menu)
    else:
        await message.answer("{}, кликни на служебное сообщение «Завершить упражнение» под строкой ввода текста"
                             ".".format(name_user))
        return
    await Start.Wait.set()
