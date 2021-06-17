# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 5го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk07_01
from loader import dp
from states.states import Start, Task07


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 7-го дня
@dp.message_handler(state=Task07.Answer_07_01)
async def answer_07_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Начать решение задачки":
        sti = open("./a_stickers/AnimatedSticker9.tgs", 'rb')  # радуется
        await message.answer_sticker(sticker=sti)
        await message.answer("Отлично! Посмотрим, как ты научился определять эмоции\n Отвечай на мои вопросы:",
                             reply_markup=tsk07_01)
        await message.answer("Я чувствовал это тогда, когда впервые получил двойку в школе")
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать".format(name_user), reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Начать решение задачки» под строкой ввода "
                             "текста.\n Или «Выполнить позже»".format(name_user))
        return
    await Task07.next()


# 1.	Я чувствовал это тогда, когда впервые получил 2 (вина/страх)
@dp.message_handler(state=Task07.Answer_07_02)
async def answer_07_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "стах" or s.lower() == 'вину' or s.lower() == 'вина':
        await message.answer("Отлично! {0}, ты прав на 100%".format(name_user))
    else:
        await message.answer("Подумай {0}, может быть это страх или вина?\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда руководитель снова возвращает документ на доработку")
    await Task07.next()


# 2.	Я чувствую это тогда, когда руководитель снова возвращает документ на доработку (раздражение/злость)
@dp.message_handler(state=Task07.Answer_07_03)
async def answer_07_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "раздражение" or s.lower() == 'злость':
        await message.answer("Да {0}, это обычная реакция".format(name_user))
    else:
        await message.answer("Подумай {0}, может быть это раздражение/злость?\nПопробуй еще раз".format(name_user))
    await message.answer(
        "Я чувствую это тогда, когда получаю на доработку документ, который считал идеально подготовленным")
    await Task07.next()


# 3.	Я чувствую это тогда, когда получаю на доработку документ, который считал идеально подготовленным (удивление)
@dp.message_handler(state=Task07.Answer_07_04)
async def answer_07_04(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "удивление":
        await message.answer("{0}, я тоже удивляюсь такому".format(name_user))
    else:
        await message.answer("{0},а может быть первая эмоция - удивление?\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда вижу точно такую же вещь на ком-нибудь другом")
    await Task07.next()


# 4.	Я чувствую это тогда, когда вижу точно такую же вещь на ком-нибудь другом (досада)
@dp.message_handler(state=Task07.Answer_07_05)
async def answer_07_05(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "досада" or s.lower() == "досаду":
        await message.answer("{0}, поддерживаю!".format(name_user))
    else:
        await message.answer("Может - досаду?\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда жду результаты экзамена")
    await Task07.next()


# 5.	Я чувствую это тогда, когда жду результаты экзамена (волнение)
@dp.message_handler(state=Task07.Answer_07_05)
async def answer_07_05(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "волнение":
        await message.answer("Да {0}, да!".format(name_user))
    else:
        await message.answer("А я например испытываю волнение?\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда вижу точно такую же вещь на ком-нибудь другом")
    await Task07.next()


# 6.	Я чувствую это тогда, когда кто-то не сдерживает своего обещания (Обида)
@dp.message_handler(state=Task07.Answer_07_06)
async def answer_07_06(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "обида" or s.lower() == "обиду":
        await message.answer("Правильная, нормальная реакция {0}!".format(name_user))
    else:
        await message.answer("Обычно люди чувствуют обиду.\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда смотрю на горящий костер в кругу теплой компании")
    await Task07.next()


# 7.	Я чувствую это тогда, когда смотрю на горящий костер в кругу теплой компании (умиротворение/спокойствие)
@dp.message_handler(state=Task07.Answer_07_07)
async def answer_07_07(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "умиротворение" or s.lower() == "спокойствие":
        await message.answer("И я тоже {0}!".format(name_user))
    else:
        await message.answer("Многие при этом чувствуют умиротворение/спокойствие.\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда не признают мои заслуги")
    await Task07.next()


# 8.	Я чувствую это тогда, когда не признают мои заслуги (обида)
@dp.message_handler(state=Task07.Answer_07_08)
async def answer_07_08(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "обида" or s.lower() == "обиду":
        await message.answer("{0}, а кто туту не почувствует обиду!".format(name_user))
    else:
        await message.answer("Большинство - обижается.\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда слушаю любимую музыку")
    await Task07.next()


# 9.	Я чувствую это тогда, когда слушаю любимую музыку (радость)
@dp.message_handler(state=Task07.Answer_07_09)
async def answer_07_09(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "радость" or s.lower() == "удовольствие":
        await message.answer("Согласен с тобой {0}!".format(name_user))
    else:
        await message.answer("А я чувствую удовольствие/радость.\nПопробуй еще раз".format(name_user))
    await message.answer("Я чувствую это тогда, когда признают результаты моего труда")
    await Task07.next()


# 10.	Я чувствую это тогда, когда признают результаты моего труда (гордость)
@dp.message_handler(state=Task07.Answer_07_10)
async def answer_07_10(message: Message):
    s = message.text
    if s.lower() == "гордость":
        await message.answer("Конечно же! Молодец!")
    else:
        await message.answer("А я чувствую удовольствие/радость.\nПопробуй еще раз")
    await message.answer("Я чувствую это тогда, когда мой ребенок выигрывает соревнования")
    await Task07.next()


# 11.	Я чувствую это тогда, когда мой ребенок выигрывает соревнования (гордость)
@dp.message_handler(state=Task07.Answer_07_11)
async def answer_07_11(message: Message):
    s = message.text
    if s.lower() == "гордость":
        await message.answer("Как и все родители!!!")
    else:
        await message.answer("Подумай может это - гордость.\nПопробуй еще раз")
    await message.answer("Я чувствую это тогда, когда интересную идею предлагает человек, от которого этого не ожидал")
    await Task07.next()


# 12.	Я чувствую это тогда, когда интересную идею предлагает человек, от которого этого не ожидал (удивление)
@dp.message_handler(state=Task07.Answer_07_12)
async def answer_07_12(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.lower() == "удивление":
        await message.answer("На верное все вокруг удивились!")
    else:
        await message.answer("{0}, многие обычно удивляются!".format(name_user))
    sti = open("./a_stickers/AnimatedSticker4.tgs", 'rb')  # хлопушка
    await message.answer_sticker(sticker=sti)
    await message.answer("Ух ты, удивил!!! Твое мастерство растет с каждым днем! Кстати, ты знал,"
                         " что удивление — это самая быстротечная из всех эмоций, длящаяся не более "
                         "нескольких секунд, ее относят к эмоциям -переключателям. "
                         "Основная функция удивления – сосредоточение внимание, чтобы мы могли"
                         " наиболее эффективно определить, что происходит, и находимся ли мы в опасности."
                         " Удивление быстро появляется, быстро переживается и проходит. Дальше оно может"
                         " перерасти в страх, радость, веселье, облегчение, гнев и так далее, в зависимости"
                         " от того, что нас удивило, или в полное отсутствие эмоций, если мы вдруг решаем, "
                         "что удивительное событие на самом деле не имеет для нас никакого значения. "
                         "Понимать причины возникновения эмоций очень важно. "
                         "Завтра мы с тобой продолжим изучать эту тему", reply_markup=menu)
    await Start.Wait.set()
