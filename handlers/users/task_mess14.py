# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 14го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, tsk07_01, tsk14_01, tsk14_02
from loader import dp
from states.states import Start, Task14
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к "задачке на прокачку" 14-го дня
@dp.message_handler(state=Task14.Answer_14_01)
async def answer_14_01(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Выполнить сейчас":
        await message.answer("Замур-р-р-чательно! Сегодня освоим одну из кнопок твоего Пульта"
                             " управления эмоциями, которая называется «фокус». Сейчас расскажу,"
                             " как ею пользоваться.\nКогда мы находимся в напряженном эмоциональном "
                             "состоянии, например, сильно расстроены или чувствуем гнев, то не можем "
                             "сосредоточиться, или, наоборот, сосредотачиваемся только на одном из "
                             "возможных действий. Тебе знакомо такое состояние, когда «мысли нельзя "
                             "собрать в кучу», и они разбросаны, как бусины по полу?\n"
                             " В этот момент важно привести себя в ресурсное состояние, а для этого есть простой "
                             "прием: изменить фокус внимания.\n Эта техника удерживает разрастание "
                             "негативной эмоции и сглаживает её градус.", reply_markup=tsk14_01)
    elif s == "Выполнить позже":
        sti = open("./a_stickers/AnimatedSticker7.tgs", 'rb')  # Плачет
        await message.answer_sticker(sticker=sti)
        await message.answer("{0}, как жаль, я думал мы весело проведем время."
                             " Возвращайся скорее – я буду ждать тебя до конца дня".format(name_user),
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await db_save_task(message.from_user.id, 14, s)
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас» под строкой ввода "
                             "текста.\n Или «Выполнить позже»".format(name_user))
        return
    await Task14.next()


#
@dp.message_handler(state=Task14.Answer_14_02)
async def answer_14_02(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Давай потренируемся":
        await message.answer("Представь на минутку, что ты находишься в яркой деструктивной эмоции,"
                             " которая захватила тебя и делает неэффективным в решении текущей задачи. "
                             "А теперь попробуй переключить свое внимание, и мысленно направить его на "
                             "предметы зеленого цвета, которые находятся вокруг тебя и привлекают взгляд."
                             "  Посчитай, сколько их. А я пока подожду.", reply_markup=tsk14_01)
        await message.answer("Сколько предметов зеленого цвета ты заметил и сосчитал?")
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
                             "текста.\nИли «Выполнить позже»".format(name_user))
        return

    await Task14.next()


# зеленый
@dp.message_handler(state=Task14.Answer_14_03)
async def answer_14_03(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s.isdigit():
        ans = int(s)
        if (ans > 1) and (ans <= 5):
            await message.answer("Это была только разминка. Уверен, что можешь найти гораздо больше предметов зеленых"
                           " предметов вокруг. Нужно только потренироваться переключать внимание!")
        elif ans > 5 and ans <= 10:
            await message.answer("Замур-р-р-чательно! Наверное, ты отметил даже зеленые глаза у коллеги! "
                           "Чем неожиданнее будут находки, тем эффективнее работает техника переключения.")
        else:
            await message.answer("Да ты настоящий сыщик! А сможешь найти еще больше предметов синего цвета?")
        await message.answer("Как тебе это упражнение?", reply_markup=tsk14_02)
        await Task14.next()
    else:
        await message.answer("{0}, пожалуйста набери число зеленых предметов!".format(name_user))


@dp.message_handler(state=Task14.Answer_14_04)
async def answer_14_04(message: Message, state: FSMContext):
    s = message.text
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "Понравилось!":
        await message.answer("Замур-р-р-чательно! Эту технику необходимо тренировать как рефлекс, "
                             "чтобы мгновенно использовать, если тебя «накрыла» яркая негативная"
                             " эмоция. Попробуй её в реальной ситуации. Можно сместить фокус на"
                             " дыхание, на цвета, на звуки. Попробуй хорошенько прислушаться прямо"
                             " сейчас, и ты заметишь целую симфонию разных звуков: коллеги разговаривают"
                             ", из окна доносится гул проезжающих машин, компьютер гудит, в коридоре"
                             " стучат чьи-то каблучки… Слушай дальше, и ты услышишь, как скрипит под "
                             "тобой стул и даже звук собственного дыхания. Это занимает не более минуты "
                             "и помогает быстро регулировать свое состояние.", reply_markup=menu)
    elif s == "Сомневаюсь в его эффективности":
        await message.answer("Я тебя понимаю. Кажется, я знаю один способ снять сомнения – попробовать"
                             " провести испытание техники в реальной ситуации, когда тебя «накрыла»"
                             " яркая негативная эмоция. Можно сместить фокус на дыхание, на цвета, на "
                             "звуки. Попробуй хорошенько прислушаться прямо сейчас, и ты заметишь целую "
                             "симфонию разных звуков: коллеги разговаривают, из окна доносится гул"
                             " проезжающих машин, компьютер гудит, в коридоре стучат чьи-то каблучки… "
                             "Слушай дальше, и ты услышишь, как скрипит под тобой стул и даже звук"
                             " собственного дыхания. Техника «смена фокуса» занимает не более минуты "
                             "и помогает быстро регулировать свое состояние.", reply_markup=menu)
        await message.answer("Если хочешь, посмотри как это работает на опыте других.")
        video = open("./VIDEO/Муха и Самурай.mp4", "rb")
        await message.answer_video(video)
        await message.answer("Благодарю за тренировку! Жди напоминание по графику.")
    else:
        await message.answer("{0}, кликни на «Понравилось!»"
                             "\n Или «Сомневаюсь в его эффективности»".format(name_user))
        return
    await Start.Wait.set()
