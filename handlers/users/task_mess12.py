# В этом модуле выполняется обработка сообщений для задачи 12-го дня
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from keyboards.default.menu import menu, pool
from loader import dp
from states.states import Start, Task12
from utils.db_api.db_commands import db_save_task


# Обработчик ввода 1го ответа (Начать) к задачке "на прокачку" 12-го дня
@dp.message_handler(state=Task12.Answer_12_01)
async def answer_12_01(message: Message, state: FSMContext):
    data = await state.get_data()
    name_user = data.get("name_user")
    s = message.text
    if s == "Выполнить сейчас!":
        video = open("./VIDEO/Походка.mp4", "rb")
        await message.answer_video(video)
        await message.answer("Посмотри, как может меняться эмоция в зависимости от походки (обрати внимание, как в конц"
                             "е меняется положение тела Людмилы Прокофьевны при появлении подчиненных).\nНапиши (в своб"
                             "одной форме), как выглядит портрет эмоции «Интерес». Что нужно сделать с телом (жесты, по"
                             "за, мимика), чтобы вызвать у себя эту эмоцию?", reply_markup=pool)
    elif s == "Выполнить позже!":
        await message.answer("Ага, понимаю! Но у тебя есть шанс вернуться к этой задачке до начала следующего дня.",
                             reply_markup=menu)
        await Start.Wait.set()
        return
    else:
        await message.answer("{0}, кликни на служебное сообщение «Выполнить сейчас!» под строкой ввода текста \n"
                             "или на «Выполнить позже!»".format(name_user))
        return
    await Task12.next()


# Обработчик ввода 2го ответа (Показать пример) к задачке "на прокачку" 12-го дня
@dp.message_handler(state=Task12.Answer_12_02)
async def answer_12_02(message: Message):
    s = message.text[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 12, s)
    await message.answer("Спасибо! А чтобы тебе было проще, поделюсь своими наработками о портретах базовых эмоций:\n"
                         "https://disk.yandex.ru/i/rFZ4hFMNFWQRgg")
    await message.answer("Какие еще способы управления эмоциями через тело ты знаешь? ( напиши в свободной форме)")
    await Task12.next()


# Обработчик ввода 3го ответа (Показать пример) к задачке "на прокачку" 12-го дня
@dp.message_handler(state=Task12.Answer_12_03)
async def answer_12_03(message: Message):
    s = message.text[:100]  # ограничиваем фантазию пользователя 100 символами
    await db_save_task(message.from_user.id, 12, s)
    await message.answer("Воссоздание «портрета» эмоции – это только один из способов. Еще можно управлять эмоциями чер"
                         "ез дыхание, физические упражнения, и даже приятные запахи/вкусы/тактильные ощущения. Это все "
                         "переключает наше тело на нужную эмоцию. Используй эти способы.")
    await message.answer("Упражнение завершено 😊", reply_markup=menu)
    await Start.Wait.set()
