from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from keyboards.inline.callback_datas import choice_callback

# Вариант 1, похожий на создание текстовой клавиатуры
choice01 = InlineKeyboardMarkup(inline_keyboard=[
    [
        # InlineKeyboardButton(text="Начнем", callback_data=choice_callback.new(state="Start", answer="Начнем")),
        InlineKeyboardButton(text="Начнем", callback_data="choice:Start:Начнем"),
        InlineKeyboardButton(text="Зачем?", callback_data=choice_callback.new(state="Start", answer="Зачем?"))
    ]
])
# Вариант 2 - с помощью row_width и insert.
# choice = InlineKeyboardMarkup(row_width=2)
# Key1 = InlineKeyboardButton(text="Начнем", callback_data=choice_callback.new(state="Start", answer="Начнем"))
# choice.insert(Key1)
# Key2 = InlineKeyboardButton(text="Зачем?", callback_data="choice:Start:Зачем?")
# choice.insert(Key2)

"""
# А теперь клавиатуры со ссылками на товары
pear_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купи тут", url=URL_APPLES)
    ]
])
apples_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купи тут", url=URL_PEAR)
    ]
])
"""
