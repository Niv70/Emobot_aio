# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 6го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk06_01, tsk06_02, pool
from loader import dp
from states.states import Start, Task06
from utils.db_api.db_commands import db_save_task, upload_xls


@dp.message_handler(state=Task06.Answer_06_01)
async def answer_06_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас!":
        await message.answer("Кликни на плашку «Выгрузка» и сделай выгрузку эмоций и причин за шесть дней.\n"
                             "{0}, поисследуй результаты под призмой следующих вопросов: Каких эмоций больше:"
                             " положительных или отрицательных? Чаще всего утром какие эмоции ты испытываешь?"
                             " Какие эмоции ты испытываешь на работе, а какие - дома? Что ты чувствуешь"
                             " вечером?".format(name_user), reply_markup=tsk06_01)
    elif s == "Выполнить позже!":
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке до начала следующего дня.",
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода текста или на"
                             " «Выполнить позже!»".format(name_user))
        return
    await Task06.next()


@dp.message_handler(state=Task06.Answer_06_02)
async def answer_06_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выгрузка":
        filename = await upload_xls(message.from_user.id)
        file = open(filename, "rb")
        await message.answer_document(file, caption="Выгрузка зарегистрированных эмоций")
        await message.answer("Что интересного можешь отметить, {0}?".format(name_user), reply_markup=pool)
    else:
        await message.answer("{0}, Нажми кнопку «Выгрузка» под строкой ввода "
                             "текста.".format(name_user))
        return
    await Task06.next()


@dp.message_handler(state=Task06.Answer_06_03)
async def answer_06_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 6, s)
    await message.answer("Все делают очень интересные выводы."
                         " А вот мой вывод: Утренний настрой очень важен."
                         "  Я вспомнил интересную историю по этому поводу.".format(name_user),
                         reply_markup=tsk06_02)
    await Task06.next()


@dp.message_handler(state=Task06.Answer_06_04)
async def answer_06_04(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Прочитать историю сейчас":
        await message.answer(
            "Детская площадка. Две девочки качаются на качелях и ведут неторопливую, светскую беседу.\n"
            "— Что-то давно никакого праздника не было, — задумчиво говорит одна. — Жалко!\n"
            "— Мне не жалко, — говорит вторая.\n"
            "— Ты праздники не любишь?!\n"
            "— Люблю! Очень! У меня их полно, каждый день — праздник!\n"
            "— Не может быть!\n"
            "— Может. Мы празднуем Дня рождение.\n"
            "— День рождения, ты хотела сказать.\n"
            "— Дни рождения мы тоже празднуем, но редко, только раз в год. А"
            " Дня рождения — каждый день. Мой папа этот праздник выдумал.\n"
            "— И как вы его празднуете?\n"
            "— Очень просто! Папа будит утром меня и маму, мы все бежим на кухню,"
            " берем стаканы с водой,"
            " и папа говорит тост: «Отличный день сегодня родился!"
            " Нам с ним очень повезло! За Новый День!» "
            "И мы пьем воду, едим мед и поем какую-нибудь песню.\n"
            "— А если день плохим получится?\n"
            "— Так раньше и было. А как только мы стали отмечать этот"
            " праздник, почти все дни или хорошие "
            "или очень хорошие. Редко-редко что-то не очень хорошее происходит.\n"
            " Почему же тогда у других людей такого праздника нет?\n"
            " Папа сказал, что этот праздник есть у всех, только не все"
            " его замечают. Многие просто забыли"
            " об этом празднике. Если хочешь, приходи в субботу к нам. Переночуешь,"
            " а утром вместе с нами попразднуешь!\n".format(name_user), reply_markup=menu)
        await message.answer("Интересная история, не правда-ли? Поделись, пожалуйста, своим "
                             "секретом утреннего настроя! Напиши в чат в произвольной форме.")
        await Task06.next()
        return
    elif s == "Завершить упражнение":
        await message.answer("До встречи! Жди напоминалку по графику.", reply_markup=menu)
    else:
        await message.answer("{0}, Нажми кнопку «Прочитать притчу сейчас» под строкой ввода "
                             "текста.\n Или «Завершить упражнение»".format(name_user))
        return
    await Start.Wait.set()


@dp.message_handler(state=Task06.Answer_06_05)
async def answer_06_05(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    await db_save_task(message.from_user.id, 6, s)
    await message.answer("{0}, спасибо! Возьму на вооружение твой способ утреннего настроя! "
                         "До встречи!".format(name_user), reply_markup=menu)
    await Start.Wait.set()
