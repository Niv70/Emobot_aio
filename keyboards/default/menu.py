from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Фиксировать эмоцию сейчас"),
        ],
        [
            KeyboardButton(text="Выполнить ”задачку на прокачку”"),
        ],
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)

pool = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)

tsk02_00 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Модель эмоционального интеллекта"),
        ],
        [
            KeyboardButton(text="Начать решение задачки"),
        ],
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)


tsk02_02 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Интересный факт о картине"),
        ],
        [
            KeyboardButton(text="Следующая картина"),
        ],
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)

tsk02_14 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Интересный факт о картине"),
        ],
        [
            KeyboardButton(text="Выход из галереи"),
        ],
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)

tsk04_00 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Список эмоций и чувств"),
        ],
        [
            KeyboardButton(text="Термометр"),
            KeyboardButton(text="Настройки")
        ],
    ],
    resize_keyboard=True
)
