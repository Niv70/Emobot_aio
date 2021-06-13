from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Фиксировать эмоцию сейчас"),
        ],
        [
            KeyboardButton(text="Выполнить задачку ”на прокачку”"),
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
