# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 4го дня
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from keyboards.default.menu import menu, pool, tsk04_02, tsk04_10
from loader import dp
from states.states import Start, Task04
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_01)
async def answer_04_01(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Выполнить сейчас!":
        img = open("./IMG/День_04_1.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Я приготовил для тебя несколько фотографий. Посмотри на первую из них и попробуй определи"
                             "ть эмоцию героя. Напиши ответ в виде одного слова <b><i>ЭМОЦИЯ</i></b>.",
                             reply_markup=pool)
    elif s == "Выполнить позже!":
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке до начала следующего дня.",
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода т"
                             "екста или на «Выполнить позже!»".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 2го ответа (ЭМОЦИЯ 1) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_02)
async def answer_04_02(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    if s == "ликование" or s == "восторг":
        await message.answer("Мяу!! Я тоже заметил эту эмоцию!")
    else:
        await message.answer("Интересно! А еще <b><i>ликование</i></b> и <b><i>восторг</i></b>! Я тоже иногда испытываю"
                             " такую эмоцию и тогда слышу в свой адрес «Ой, распушил усы»!")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 3го ответа (Следующее 1) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_03)
async def answer_04_03(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        img = open("./IMG/День_04_2.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Напиши название эмоции, которую ты видишь на этой картинке.", reply_markup=pool)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 4го ответа (ЭМОЦИЯ 2) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_04)
async def answer_04_04(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    if s == "удивление" or s == "изумление":
        await message.answer("Мяу!! Удивительная эмоция, не правда ли! Глаза широко раскрыты и нижняя челюсть "
                             "опускается, так что губы и зубы размыкаются, и рот находится в ненапряженном состоянии.")
    else:
        await message.answer("Любопытно. А ты заметил, что глаза широко раскрыты и нижняя челюсть опускается, так что "
                             "губы и зубы размыкаются, и рот находится в ненапряженном состоянии. Это характерно для "
                             "эмоций <b><i>удивления</i></b> и <b><i>изумления</i></b>.")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 5го ответа (Следующее 2) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_05)
async def answer_04_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        img = open("./IMG/День_04_3.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Напиши название эмоции, которую ты здесь видишь.", reply_markup=pool)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 6го ответа (ЭМОЦИЯ 3) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_06)
async def answer_04_06(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    if s == "радость" or s == "гордость":
        await message.answer("Я их понимаю!! Сам испытывал похожую эмоцию, когда мне вручали диплом «хвостатого "
                             "защитника Эрмитажа».")
    else:
        await message.answer("Многие замечают на лицах молодых людей эмоции <b><i>радости</i></b> и "
                             "<b><i>гордости</i></b>! Я их понимаю! Сам испытывал похожую эмоцию, когда мне вручали "
                             "диплом «хвостатого защитника Эрмитажа».")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 7го ответа (Следующее 3) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_07)
async def answer_04_07(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        img = open("./IMG/День_04_4.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Напиши название эмоции девушки.", reply_markup=pool)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 8го ответа (ЭМОЦИЯ 4) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_08)
async def answer_04_08(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    if s == "обида":
        await message.answer("Точно!! Девушка чувствует обиду! А вот лица молодого человека не видно. Уверен, что он "
                             "чувствует интерес и увлеченность! Ведь смотреть футбол, это так здорово! Странно, что "
                             "девушки не всегда разделяют это мнение!")
    else:
        await message.answer("Интересно! А еще многие замечают на лице девушки выражение <b><i>обиды</i></b>! А вот "
                             "лица молодого человека не видно. Уверен, что он чувствует интерес и увлеченность! Ведь "
                             "смотреть футбол, это так здорово! Странно, что девушки не всегда разделяют это мнение!")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 9го ответа (Следующее 4) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_09)
async def answer_04_09(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        img = open("./IMG/День_04_5.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Напиши название эмоции мальчика слева от стола.", reply_markup=pool)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 10го ответа (ЭМОЦИЯ 5) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_10)
async def answer_04_10(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    if s == "триумф":
        await message.answer("А еще говорят, что шахматы – это игра без эмоций!! Удивительно, что выражение триумфа - "
                             "врожденный, а не приобретенный жест. Воздетые вверх руки, даже поднятый к небу взгляд… "
                             "Когда профессиональному спортсмену удается одержать победу на состязаниях, мы нередко "
                             "видим этот триумфальный жест. Подумай, а что переживает в данный момент проигравшая "
                             "сторона? Жесты мальчика справа говорят сами за себя.")
    else:
        await message.answer("Интересно! А еще говорят, что шахматы – это игра без эмоций! А ты заметил триумфальный "
                             "жест? Удивительно, что выражение <b><i>триумфа</i></b> - врожденный, а не приобретенный "
                             "жест. Воздетые вверх руки, даже поднятый к небу взгляд… Когда профессиональному "
                             "спортсмену удается одержать победу на состязаниях, мы нередко видим этот триумфальный "
                             "жест. Подумай, а что переживает в данный момент проигравшая сторона? Жесты мальчика "
                             "справа говорят сами за себя.")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 11го ответа (Следующее 5) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_11)
async def answer_04_11(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        img = open("./IMG/День_04_6.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Напиши название эмоции, которую ты видишь на этой картинке.", reply_markup=pool)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 12го ответа (ЭМОЦИЯ 6) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_12)
async def answer_04_12(message: Message):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 4, s)
    await message.answer("Если тебе интересно, что заметил я, то я поделюсь своими наблюдениями. Это сплав <b><i>предв"
                         "кушения</i></b> и <b><i>восторга</i></b>! Обрати внимание на глаза! Я тоже так смотрю на тар"
                         "елку с деревенскими сливками.")
    await message.answer("Кликни на служебное сообщение «Следующее фото» под строкой ввода текста",
                         reply_markup=tsk04_02)
    await Task04.next()


# Обработчик ввода 13го ответа (Следующее 6) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_13)
async def answer_04_13(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Следующее фото":
        await message.answer(
            "Спасибо, что поделился своим мнением об эмоциях героев на фото. Это был интересный опыт. И я "
            "даже немного завидую тебе. Ведь для того чтобы выразить полный спектр эмоций, природа "
            "наградила тебя 43 мускулами, отвечающими за мимику. И если наблюдать за мимикой, за жестами и"
            " не упускать из виду контекст ситуации, то определить эмоцию становится намного проще. Но и "
            "такие, как я, даже без мускулов, могут изобразить некоторые эмоции. Не веришь?")
        img = open("./IMG/День_04_7.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("Кликни на служебное сообщение «Завершить упражнение» под строкой ввода текста",
                             reply_markup=tsk04_10)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Следующее фото» под строкой ввода "
                             "текста".format(name_user))
        return
    await Task04.next()


# Обработчик ввода 14го ответа (Следующее 6) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task04.Answer_04_14)
async def answer_04_14(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Завершить упражнение":
        await message.answer("До встречи! Жди напоминалку по графику.", reply_markup=menu)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Завершить упражнение» под строкой ввода "
                             "текста".format(name_user))
        return
    await Start.Wait.set()
