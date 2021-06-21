# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 9го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk07_01, tsk09_01

from loader import dp
from states.states import Start, Task09


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 10-го дня
from utils.db_api.db_commands import db_save_task


@dp.message_handler(state=Task09.Answer_09_01)
async def answer_09_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас":
        await message.answer("Я приготовил для тебя интересный кейс. Это кейс я согласовал с одним знакомым "
                             "шейхом из Арабских Эмиратов, поэтому, он максимально достоверный. ")
        await message.answer("«При чем же здесь шейх?» – спросишь ты.")
        await message.answer(" Одним из компонентов эмоционального интеллекта"
                             " является в том числе понимание культурных особенностей партнеров по "
                             "коммуникации.")
        await message.answer("Итак, представь, что ты сотрудник компании «Арсенал» "
                             "и ты вместе с коллегой отправляешься в ОАЭ на встречу с «шейхом». "
                             "Такое может случиться. В процессе вашей коммуникации «шейх» может испытать "
                             "самые разные эмоций. Даже те, которые никак не содействуют эффективному результату"
                             " в переговорах. Хочешь узнать, что в твоем поведении или в "
                             "поведении твоего коллеги могло вызвать такую реакцию?",
                             reply_markup=tsk09_01)
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать тебя до конца дня".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас» под строкой ввода "
                             "текста.\n Или «Выполнить позже»".format(name_user))
        return
    await Task09.next()


@dp.message_handler(state=Task09.Answer_09_02)
async def answer_09_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Презрение":
        await message.answer("<b>Презрение</b>", parse_mode="HTML")
        await message.answer("Твой коллега, надел на официальную встречу национальную одежду ОАЭ. "
                                       "Это может быть воспринято как насмешка.\n"
                                       "Арабы слишком гордятся своей национальной одеждой.")
    elif s == "Недоверие":
        await message.answer("<b>Недоверие</b>", parse_mode="HTML")
        await message.answer("Твой коллега завел разговор про политику, в разговоре дал понять о своей "
                             "дружеской расположенности к недружественной для ОАЭ стране и поддержал их "
                             "политику.\nА еще вы с коллегой, проходя по коридору, протянули руку для"
                             " рукопожатия встречавшей вас женщине. Это может быть расценено как неприличный жест.")
    elif s == "Интерес":
        await message.answer("<b>Интерес</b>", parse_mode="HTML")
        await message.answer("ТВы немного поговорили о культуре, поинтересовались местными традициями и"
                             " поделились своим впечатлением. Вашим оппонентам очень интересно как живут"
                             " люди в других странах и часто от них можно услышать вопрос «А как у вас с этим?».")
    elif s == "Радость":
        await message.answer("<b>Радость</b>", parse_mode="HTML")
        await message.answer("Вы с коллегой старались поддерживать диалог в максимально почтительной "
                             "и уважительной манере и подарили уместный в деловых отношениях подарок. ")
    elif s == "Продолжить":
        await message.answer("А не кажется ли тебе, что мы сами закладываем эмоциональный сценарий"
                             " в коммуникации?  Думаю, что важно анализировать и прогнозировать свои"
                             " действия в коммуникации, и понимать, к чему они могут привести. "
                             "А теперь давай перейдем к национальным особенностям коммуникации. "
                             "Давай разберем три ситуации. ".format(name_user), reply_markup= tsk07_01)
        await message.answer("<b>Ситуация №1</b>", parse_mode="HTML")
        await message.answer("Представь, что ты опоздал на встречу  на 5 минут. Как думаешь, какую эмоцию"
                             " это вызовет у твоего коллеги? Напиши название эмоции.")
        await Task09.next()


@dp.message_handler(state=Task09.Answer_09_03)
async def answer_09_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 9, s)

    await message.answer("И так бывает! Один мой знакомый терпеть не может опозданий и он"
                         " сильно гневается по этому поводу. Я полагаю, что такая интенсивная "
                         "негативная эмоция связана с тем, что задета его ценность «время» или"
                         " «уважение».  А некоторые люди сами всегда опаздывают, поэтому испытывают "
                         "радость и облегчение, если другие тоже опоздали. Если тебе интересно, что "
                         "бы я испытал, опоздай ты на встречу? Я обычно испытываю эмоцию принятия, "
                         "ведь внешняя среда часто непредсказуема.")
    await message.answer("<b>Ситуация №2</b>", parse_mode="HTML")
    await message.answer("Представь, что ты перебил коллегу в разговоре. Как думаешь, какую эмоцию "
                         "это вызовет у твоего коллеги? Напиши название эмоции.")
    await Task09.next()

@dp.message_handler(state=Task09.Answer_09_04)
async def answer_09_04(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 9, s)
    await message.answer("И такое может быт быть. Большинство людей испытываю злость и раздражение,"
                         " если их перебивают. Ведь, не позволяя собеседнику договорить, мы как будто "
                         "произносим фразу «То, что я хочу сказать сейчас, более важно, чем то, что говоришь"
                         " ты». А вот один мой знакомый кот относится к этому спокойно и вежливо "
                         "спрашивает после того, как перебивший договорит: «Я продолжу свою мысль?». "
                         "Кстати, можно даже пошутить словами Жванецкого «Извините, что я говорю, "
                         "когда вы меня перебиваете…»")
    await message.answer("<b>Ситуация №3</b>", parse_mode="HTML")
    await message.answer("Представь, что ты организовал совещание и обозначил "
                         "продолжительность 30 минут, но задержал всех присутствующих на час."
                         " Как думаешь, какую эмоцию это вызовет у твоего коллеги, который был на совещании?")
    await Task09.next()

@dp.message_handler(state=Task09.Answer_09_05)
async def answer_09_05(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 9, s)
    await message.answer("У многих людей такая ситуация вызывает досаду и раздражение.  "
                         "Но если эта ситуация повторяется, то досада может"
                         " перерасти в более сильную эмоцию по шкале интенсивности.\n"
                         "Посмотри в Эмоциональный термометр, как она называется и напиши.")
    await Task09.next()

@dp.message_handler(state=Task09.Answer_09_06)
async def answer_09_06(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 9, s)
    if not (s.lower() == "злость" or s.lower() == "гнев"):
        await message.answer("Внимательно посмотри Эмоциональный термометр!")
        return
    await message.answer("Спасибо, ты отлично справился с «задачкой на прокачку». "
                         "Я рад, что мы обсудили, как наши действия влияют на эмоции.\n"
                         "Жди напоминалку о фиксации эмоций по графику.", reply_markup=menu)
    await Start.Wait.set()
