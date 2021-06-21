# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 10го дня
from aiogram.types import Message, ParseMode
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk07_01, tsk13_01, tsk13_02, tsk13_03
from loader import dp
from states.states import Start, Task13
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 10-го дня
@dp.message_handler(state=Task13.Answer_13_01)
async def answer_13_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас":
        await message.answer("В психологии есть такое понятие, как подстройка. Если два собеседника "
                             "ведут себя похожим образом, эта похожесть поведения сближает их и"
                             " делает контакт между ними более прочным. В частности, один из важных "
                             "параметров для установления контакта - похожесть голосовых характеристик"
                             " (высота тона, скорость, интонация). Что происходит, когда мы игнорируем "
                             "речевую подстройку, ты можешь прочитать в кейсах", reply_markup=tsk13_01)
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке в"
                             " течение 24 часов.".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас» под строкой ввода "
                             "текста.\n Или «Выполнить позже»".format(name_user))
        return
    await Task13.next()


#
@dp.message_handler(state=Task13.Answer_13_02)
async def answer_13_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Кейс 1":
        await message.answer("<b>Как-то раз мы своей командой котиков-Заботиков "
                             "консультировали менеджера по продажам, который все никак не"
                             " мог наладить контакт с клиентом. Став свидетелями очередной "
                             "попытки договориться о встрече, мы заметили, что темп речи менеджера"
                             " был раза в 3 быстрее, чем темп речи клиента. «Я стараюсь как можно"
                             " быстрее проговорить свое предложение, чтобы сэкономить время у столь "
                             "занятого человека», - так объяснил он свою торопливость. Клиента это, "
                             "похоже, раздражало, и он раз за разом откладывал встречу. "
                             "Стоило нашему менеджеру в следующем телефонном разговоре "
                             "замедлить темп речи до уровня клиента, как дело сдвинулось"
                             " с мертвой точки, и встреча была назначена.</b>", reply_markup=tsk13_01)
        return
    if s == "Кейс 2":
        await message.answer("<b>У другого менеджера была иная проблема. Обычно он говорил очень"
                             " медленно, и тех клиентов, которые привыкли к быстрому, даже "
                             "стремительному стилю обмена информацией, это просто бесило, "
                             " когда им м-е-д-л-е-н-н-о и неторопливо что-то объясняли. "
                             "Стоило менеджеру чуть увеличить темп своей речи, как раздражение "
                             "клиентов сошло на нет.</b>", reply_markup=tsk13_01)
        return
    elif s == "Продолжить":
        await message.answer("Легко сказать, но трудно сделать скажешь ты. И будешь прав – лучше один раз увидеть, "
                             "чем 100 раз услышать. Я приготовил для тебя видео – посмотри, как это работает и"
                             " возвращайся, нам нужно будет делать небольшое задание. ".format(name_user),
                             reply_markup=tsk13_02)
        video = open("./VIDEO/Активное слушание.mp4","rb")
        await message.answer_video(video)
    else:
        await message.answer("{0}, выбери кейс который хочешь посмотреть.\nИли «Продолжить»".format(name_user))
        return
    await Task13.next()


#
@dp.message_handler(state=Task13.Answer_13_03)
async def answer_13_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить задание":
        await message.answer("Представь, что вы собрались на рабочую встречу по"
                             " распределению нового функционала между подразделениями "
                             "(без увеличения численности). Вопрос сложный, мнения высказываются "
                             "разные и с каждым новым вступающим обстановка накаляется. Уже никто "
                             "никого не слышит, когда очередь доходит до тебя.")
        await message.answer("Необходимо снизить "
                             "эмоциональный фон беседы, как ты будешь высказывать "
                             "свою позицию?:", reply_markup=tsk13_03)
        await message.answer("1) Говорить громче и быстрее\n"
                             "2) Говорить тише и быстрее\n"
                             "3) Говорить тише и медленнее\n"
                             "4) Говорить громче и медленнее")
        await message.answer("Набери номер ответа:")
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке в"
                             " течение 24 часов.".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, выбери «Выполнить задание»\n Или «Выполнить позже»".format(name_user))
        return
    await Task13.next()


@dp.message_handler(state=Task13.Answer_13_04)
async def answer_13_04(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "3":
        await message.answer("Замур-р-р-чательно! Я вижу, ты уловил суть!", reply_markup=menu)
        await message.answer("В завершении этой темы хочу поделиться с тобой одним наблюдением. "
                             "Негативное мышление вызывает негативные мысли. Как с этим работать,"
                             " ты можешь ознакомиться в <a href=\"https://4brain.ru/blog/%D1%83%D0%"
                             "BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D1%81%D0%B2%D0%BE"
                             "%D0%B8%D0%BC%D0%B8-%D0%BC%D1%8B%D1%81%D0%BB%D1%8F%D0%BC%D0%B8/\">"
                             " «Руководстве по управлению своими мыслями» </a>", parse_mode=ParseMode.HTML)
        await message.answer("До завтра !!!")
    else:
        await message.answer("Попробуй еще раз".format(name_user))
        return
    await Start.Wait.set()
