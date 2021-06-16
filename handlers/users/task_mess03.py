# В этом модуле выполняется обработка сообщений в состоянии Задача (Task) для 4го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from loader import dp
from states.states import Start, Task03
from utils.db_api.db_commands import db_save_task
from keyboards.default.menu import tsk03_00, tsk03_01, menu


# Обработчик ввода 1го ответа (ЭМОЦИЯ) к задачке "на прокачку" 3-го дня
@dp.message_handler(state=Task03.Answer_03_01)
async def answer_03_01(message: Message, state: FSMContext):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "интересный факт о композиторе":
        await message.answer("Ты только что прослушал музыкальный фрагмент Войцеха Киляра к фильму «Дракула»."
                             " У поклонников хоррора кровь стыла в жилах от фильма, снятого Фрэнсисом Фордом Копполой,"
                             " во многом благодаря музыке классического композитора Войцеха Киляра. Симфонические "
                             "произведения Киляра звучат в более чем ста фильмах. Сам же автор утверждал, что больше"
                             " тяготеет к романтической музыке..")
        await message.answer("{0}, предлагаю нажать кнопку «Следующий музыкальный фрагмент» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "следующий музыкальный фрагмент":
        audio = open("./SND/Задача 3-2.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("Напиши название эмоции, которую ты здесь видишь.", reply_markup=tsk03_00)
        await Task03.next()
    elif s == "решить задачу позднее":
        await message.answer("До встречи!", reply_markup=menu)
        await Start.Wait.set()
    else:
        await db_save_task(message.from_user.id, 3, s)
        audio = open("./SND/Задача 3-2.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("Напиши название эмоции, которую ты здесь видишь.", reply_markup=tsk03_00)
        await Task03.next()


# Обработчик ввода 2го ответа (ЭМОЦИЯ) к задачке "на прокачку" 4-го дня
@dp.message_handler(state=Task03.Answer_03_02)
async def answer_03_02(message: Message, state: FSMContext):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "интересный факт о композиторе":
        await message.answer("Ты только что прослушал сонату Бетховена, известную как «Лунная». Однако сам Бетховен"
                             " такого названия не давал. Соната числилась под номером 14 и имела подзаголовок "
                             "«В духе фантазии». Уже после смерти композитора критик Людвиг Рельштаб сравнил первую"
                             " часть сонаты с «лунным светом над Фирвальдштетским озером», а затем эпитет «Лунная» "
                             " закрепился за всем произведением.")
        await message.answer("{0}, предлагаю нажать кнопку «Следующий музыкальный фрагмент» под строкой ввода "
                             "текста".format(name_user))
        return
    elif s == "следующий музыкальный фрагмент":
        audio = open("./SND/Задача 3-3.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("Напиши название эмоции, которую ты здесь видишь.", reply_markup=tsk03_01)
        await Task03.next()
    elif s == "решить задачу позднее":
        await message.answer("До встречи!", reply_markup=menu)
        await Start.Wait.set()
    else:
        await db_save_task(message.from_user.id, 3, s)
        audio = open("./SND/Задача 3-2.mp3", "rb")
        await message.answer_audio(audio)
        await message.answer("Напиши название эмоции, которую ты здесь видишь.", reply_markup=tsk03_01)
        await Task03.next()


@dp.message_handler(state=Task03.Answer_03_03)
async def answer_03_03(message: Message, state: FSMContext):
    s = message.text.lower()
    s = s[0:100]  # ограничиваем фантазию пользователя 100 символами
    data = await state.get_data()
    name_user = data.get("name_user")
    if s == "интересный факт о композиторе":
        await message.answer("{0}, ты только что прослушал сонату Бетховена, известную как «Лунная». Однако "
                             "сам Бетховен такого названия не давал. Соната числилась под номером 14 и"
                             " имела подзаголовок «В духе фантазии». Уже после смерти композитора критик Людвиг "
                             "Рельштаб сравнил первую часть сонаты с «лунным светом над Фирвальдштетским озером»,"
                             " а затем эпитет «Лунная» закрепился за всем произведением.".format(name_user))

    elif s == "решить задачу позднее":
        await message.answer("До встречи {0}!".format(name_user), reply_markup=menu)
        await Start.Wait.set()
    else:
        await db_save_task(message.from_user.id, 3, s)
        await message.answer("{0}! Благодарю тебя за интересный эксперимент с фиксацией эмоций при"
                             " прослушивании музыки.".format(name_user))
        sti = open("./a_stickers/AnimatedSticker4.tgs", 'rb')  # Смотрит кино
        await message.answer_sticker(sticker=sti)
        await message.answer("До встречи! Дальше будет еще интереснее.", reply_markup=menu)
        await Start.Wait.set()
