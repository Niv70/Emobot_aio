# В этом модуле выполняется обработка сообщений для задачи 2-го дня
from aiogram.types import Message
# Ключи FSMContext: name_user(str[10]),tmz(int),start_t(int),end_t(int),period(int),tsk_t(int),
# prev_data(int),current_day(int),flag_pool(int),flag_task(int)
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import tsk02_02, tsk02_14, menu
from loader import dp
from states.states import Start, Task02
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_01)
async def answer_02_01(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Модель эмоционального интеллекта":
        await message.answer("Модель эмоционального интеллекта включает четыре ветви: распознавание своих эмоций и "
                             "эмоций других людей, использование эмоций для решения задач, понимание причин эмоций и "
                             "управление своими эмоциями и эмоциями других.  Это и есть наш эмоциональный мышечный "
                             "каркас.")
        await message.answer("{0}, предлагаю нажать кнопку «Начать решение задачки» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Начать решение задачки":
        await message.answer("Приглашаю тебя в маленькую картинную галерею. В ней всего пять картин, но каждая из них "
                             "обязательно разбудит в тебе новую эмоцию. Постарайся ее уловить и сформулировать. Но "
                             "прежде, давай узнаем твою текущую эмоцию.")
        await message.answer("{0}, что ты сейчас чувствуешь?".format(name_user))
    else:
        await message.answer("{0}, кликни кнопку «Модель эмоционального интеллекта» под строкой ввода текста или "
                             "кнопку «Начать решение задачки»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 2го ответа  (эмоция текущая) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_02)
async def answer_02_02(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Зафиксировал. А теперь, добро пожаловать в галерею.")
    img = open("./IMG/День_02_1.jpg", "rb")
    await message.answer_photo(img)
    await message.answer("{0}, что ты сейчас чувствуешь, глядя на эту картину?".format(name_user),
                         reply_markup=tsk02_02)
    await Task02.next()


# Обработчик ввода 3го ответа (эмоция к 1-й картине) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_03)
async def answer_02_03(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Как думаешь, почему ты так отреагировал на эту картину?")
    await Task02.next()


# Обработчик ввода 4го ответа (реакция на 1-ю картину) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_04)
async def answer_02_04(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                         "кнопку «Следующая картина»".format(name_user))
    await Task02.next()


# Обработчик ввода 5го ответа (Следующая для 1й картины) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_05)
async def answer_02_05(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Интересный факт о картине":
        await message.answer("Эта картина «Мост Ватерлоо» Клода Моне. При рассмотрении картины с близкого расстояния "
                             "зритель не видит ничего, кроме полотна, на который нанесены частые густые масляные мазки."
                             " Вся магия произведения раскрывается, когда мы постепенно начинаем отодвигаться от "
                             "полотна на большее расстояние.\nСначала перед нами проявляются непонятные полуокружности,"
                             " проходящие через середину картины, затем мы видим явные очертания лодок, а если мы "
                             "отойдем приблизительно на два метра, то перед нами возникнут и выстроятся в логическую "
                             "цепочку все связующие произведения.")
        await message.answer("{0}, предлагаю нажать кнопку «Следующая картина» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Следующая картина":
        img = open("./IMG/День_02_2.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("{0}, что ты сейчас чувствуешь, глядя на эту картину?".format(name_user))
    else:
        await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                             "кнопку «Следующая картина»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 6го ответа (эмоция к 2-й картине) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_06)
async def answer_02_06(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Как думаешь, почему ты так отреагировал на эту картину?")
    await Task02.next()


# Обработчик ввода 7го ответа (реакция на 2-ю картину) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_07)
async def answer_02_07(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                         "кнопку «Следующая картина»".format(name_user))
    await Task02.next()


# Обработчик ввода 8го ответа (Следующая для 2й картины) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_08)
async def answer_02_08(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Интересный факт о картине":
        await message.answer("Это картина «Номер 5, 1948» американского лидера абстрактного экспрессионизма Джексона "
                             "Поллока.\nСтранность этой картины в том, что полотно, которое он нарисовал, разливая "
                             "краску по разложенному на полу куску фибролита, — одна из самых дорогих картин в мире. "
                             "В 2006 году на аукционе Sotheby’s за нее заплатили 140 миллионов долларов. «Я продолжаю "
                             "отходить от обычных инструментов художника, таких как мольберт, палитра и кисти. Я "
                             "предпочитаю палочки, совки, ножи и льющуюся краску или смесь краски с песком, битым "
                             "стеклом или чем-то еще» - говорит автор.")
        await message.answer("{0}, предлагаю нажать кнопку «Следующая картина» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Следующая картина":
        img = open("./IMG/День_02_3.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("{0}, что ты сейчас чувствуешь, глядя на эту картину?".format(name_user))
    else:
        await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                             "кнопку «Следующая картина»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 9го ответа (эмоция к 3-й картине) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_09)
async def answer_02_09(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Как думаешь, почему ты так отреагировал на эту картину?")
    await Task02.next()


# Обработчик ввода 10го ответа (реакция на 3-ю картину) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_10)
async def answer_02_10(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                         "кнопку «Следующая картина»".format(name_user))
    await Task02.next()


# Обработчик ввода 11го ответа (Следующая для 3й картины) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_11)
async def answer_02_11(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Интересный факт о картине":
        await message.answer("Это «Зимний пейзаж» (1811г). Его автор – Каспар Давид Фридрих.\nНа ней мы видим человека"
                             " с костылями, который блуждает в беспросветной зимней тьме среди корявых деревьев. "
                             "Путника окружает холодный мрак и нет никакой надежды на счастливый конец. Интересно, что"
                             " эта картина всегда выставлялась вместе с другой картиной Фридриха «Зимний пейзаж с"
                             " церковью». Таким образом, зрителю становилось понятно, что надежда есть даже тогда, "
                             "когда её совсем не видно. В этих картинах пугающее величие природы и невероятная "
                             "мистичность.")
        await message.answer("{0}, предлагаю нажать кнопку «Следующая картина» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Следующая картина":
        img = open("./IMG/День_02_4.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("{0}, что ты сейчас чувствуешь, глядя на эту картину?".format(name_user))
    else:
        await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                             "кнопку «Следующая картина»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 12го ответа (эмоция к 4-й картине) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_12)
async def answer_02_12(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Как думаешь, почему ты так отреагировал на эту картину?")
    await Task02.next()


# Обработчик ввода 13го ответа (реакция на 4-ю картину) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_13)
async def answer_02_13(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                         "кнопку «Следующая картина»".format(name_user))
    await Task02.next()


# Обработчик ввода 14го ответа (Следующая для 4я картины) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_14)
async def answer_02_11(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Интересный факт о картине":
        await message.answer("Это картина Пабло Пикассо «Стеклянная посуда», которая хранится в Эрмитаже. А знаешь "
                             "такой необычный факт об авторе этой картины? Когда Пабло Пикассо родился, акушерка "
                             "посчитала его мертворожденным. Спас ребёнка его дядя, который курил сигары и увидев "
                             "младенца, лежащего на столе, пустил дым ему в лицо, после чего Пабло заревел. Таким "
                             "образом, можно сказать, что курение спасло Пикассо жизнь.")
        await message.answer("{0}, предлагаю нажать кнопку «Следующая картина» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Следующая картина":
        img = open("./IMG/День_02_5.jpg", "rb")
        await message.answer_photo(img)
        await message.answer("{0}, что ты сейчас чувствуешь, глядя на эту картину?".format(name_user),
                             reply_markup=tsk02_14)
    else:
        await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                             "кнопку «Следующая картина»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 15го ответа (эмоция к 5-й картине) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_15)
async def answer_02_15(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s1 = message.text[0:11]
    s2 = message.text[11:110]  # ограничиваем фантазию пользователя 100 символами
    if s1.lower() != "я чувствую ":
        await message.answer("{0}, попробуй все-таки написать: <b><i>Я чувствую ЭМОЦИЯ</i></b>".format(name_user))
        return
    await db_save_task(message.from_user.id, 2, s2)
    await message.answer("Как думаешь, почему ты так отреагировал на эту картину?")
    await Task02.next()


# Обработчик ввода 16го ответа (реакция на 5-ю картину) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_16)
async def answer_02_16(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                         "кнопку «Выход из галереи»".format(name_user))
    await Task02.next()


# Обработчик ввода 17го ответа (Следующая для 5я картины) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_17)
async def answer_02_17(message: Message, state: FSMContext):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    s = message.text
    if s == "Интересный факт о картине":
        await message.answer("Это картина Ренуара «Луг» (около1880г).  А всего Ренуар успел написать около 6000 картин"
                             " за 60 лет. Когда Ренуар сломал правую руку, вместо того, чтобы расстроиться и горевать "
                             "по этому поводу, он берёт кисть в левую, и через некоторое время ни у кого не возникает "
                             "сомнения, что он сможет писать шедевры обеими руками.\nРенуар был настолько влюблен в "
                             "живопись, что не прекращал работать даже в старости, болея разными формами артрита, и "
                             "рисовал кисточкой, привязанной к рукаву. Однажды его близкий друг Матисс спросил: «Огюст,"
                             " почему вы не оставите живопись, вы же так страдаете?» Ренуар ограничился лишь ответом: "
                             "«Ladouleurpasse, labeautéreste» (Боль проходит, а красота остаётся).")
        await message.answer("{0}, предлагаю нажать кнопку «Выход из галереи» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "Выход из галереи":
        await message.answer("{0}, что нового ты узнал о себе после завершения упражнения?".format(name_user))
    else:
        await message.answer("{0}, кликни кнопку «Интересный факт о картине» под строкой ввода текста или "
                             "кнопку «Выход из галереи»".format(name_user))
        return
    await Task02.next()


# Обработчик ввода 18го ответа (пссле Выход из галереи) к задачке "на прокачку" 2-го дня
@dp.message_handler(state=Task02.Answer_02_18)
async def answer_02_18(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text[0:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 2, s)
    await message.answer("Интересный комментарий! {0}, спасибо за прогулку по галерее! Завтра захвати наушники, у меня"
                         " будет к тебе интересное задание.".format(name_user), reply_markup=menu)
    await Start.Wait.set()

# await message.answer('{0}, я не могу больше ждать твоего ответа, т.к. пришло время следующего '
#                      'вопроса!'.format(name_user), reply_markup=menu)

# ============================== Запуск задачки "на прокачку" N-го дня ==============================
