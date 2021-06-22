# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 4го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.states import Start, Task03
from utils.db_api.db_commands import db_save_task
from keyboards.default.menu import tsk03_01, menu, tsk03_06


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_01)
async def answer_03_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас!":
        await message.answer("Прослушай музыкальный фрагмент и напиши в чат эмоцию, которую почувствуешь.",
                             reply_markup=tsk03_01)
        audio = open("./SND/Задача 3-1.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("{0}, что ты чувствуешь после прослушивания музыки?".format(name_user))
    elif s == "Выполнить позже!":
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке до начала следующего дня.",
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода текста или на"
                             " «Выполнить позже!»".format(name_user))
        return
    await Task03.next()


# Обработчик ввода 2го ответа (Эмоция 1) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_02)
async def answer_03_02(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 3, s2)
    await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода текста "
                         "или на «Следующий музыкальный фрагмент».".format(name_user))
    await Task03.next()


# Обработчик ввода 2го ответа (Кнопка) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_03)
async def answer_03_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Интересный факт о композиторе":
        await message.answer("Ты только что прослушал музыкальный фрагмент Войцеха Киляра к фильму «Дракула»."
                             " У поклонников хоррора кровь стыла в жилах от фильма, снятого Фрэнсисом Фордом Копполой,"
                             " во многом благодаря музыке классического композитора Войцеха Киляра. Симфонические "
                             "произведения Киляра звучат в более чем ста фильмах. Сам же автор утверждал, что больше"
                             " тяготеет к романтической музыке.")
        await message.answer("{0}, предлагаю кликнуть на служебное сообщение «Следующий музыкальный фрагмент» под "
                             "строкой ввода текста.".format(name_user))
        return
    elif s == "Следующий музыкальный фрагмент":
        audio = open("./SND/Задача 3-2.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("{0}, что ты чувствуешь после прослушивания музыки?".format(name_user))
    else:
        await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода "
                             "текста или на «Следующий музыкальный фрагмент».".format(name_user))
        return
    await Task03.next()


# Обработчик ввода 4го ответа (Эмоция 2) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_04)
async def answer_03_04(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 3, s2)
    await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода текста "
                         "или на «Следующий музыкальный фрагмент».".format(name_user))
    await Task03.next()


# Обработчик ввода 5го ответа (Кнопка) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_05)
async def answer_03_05(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Интересный факт о композиторе":
        await message.answer("Ты только что прослушал сонату Бетховена, известную как «Лунная». Однако сам Бетховен"
                             " такого названия не давал. Соната числилась под номером 14 и имела подзаголовок "
                             "«В духе фантазии». Уже после смерти композитора критик Людвиг Рельштаб сравнил первую"
                             " часть сонаты с «лунным светом над Фирвальдштетским озером», а затем эпитет «Лунная» "
                             " закрепился за всем произведением.")
        await message.answer("{0}, предлагаю кликнуть на служебное сообщение «Следующий музыкальный фрагмент» под "
                             "строкой ввода текста.".format(name_user))
        return
    elif s == "Следующий музыкальный фрагмент":
        audio = open("./SND/Задача 3-3.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("{0}, что ты чувствуешь после прослушивания музыки?".format(name_user),
                             reply_markup=tsk03_06)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода "
                             "текста или на «Следующий музыкальный фрагмент».".format(name_user))
        return
    await Task03.next()


# Обработчик ввода 6го ответа (Эмоция 3) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_06)
async def answer_03_06(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 3, s2)
    await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода текста "
                         "или на «Завершить упражнение».".format(name_user), reply_markup=tsk03_06)
    await Task03.next()


# Обработчик ввода 7го ответа (Кнопка) к "задачке на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_07)
async def answer_03_07(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Интересный факт о композиторе":
        await message.answer("Ты только что прослушал произведение лучшего композитора в истории человечества по версии"
                             " «NewYorkTimes» - Иогана Себастьяна Баха, которое называется «Шутка». А всего в течение ж"
                             "изни Бах написал более тысячи музыкальных произведений. Гёте утверждал, что музыка Баха п"
                             "омогает ощутить гармонию с самим собой. И я с ним полностью согласен.")
        await message.answer("{0}, предлагаю кликнуть на служебное сообщение «Завершить упражнение» под "
                             "строкой ввода текста.".format(name_user))
        return
    elif s == "Завершить упражнение":
        await message.answer("Благодарю тебя за интересный эксперимент с фиксацией эмоций при прослушивании музыки.",
                             reply_markup=menu)
    else:
        await message.answer("{0}, кликни на служебное сообщение «Интересный факт о композиторе» под строкой ввода "
                             "текста или на «Завершить упражнение».".format(name_user))
        return
    await Start.Wait.set()
