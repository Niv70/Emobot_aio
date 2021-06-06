from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# from keyboards.inline.callback_datas import choice_callback

# Вариант 1, похожий на создание текстовой клавиатуры
choice01 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Я в деле. Давай начнем.", callback_data="choice:Start_Call01:Начнем")
    ],
    [
        InlineKeyboardButton(text="Зачем мне это надо?", callback_data="choice:Start_Call01:Зачем?")
    ]
])
# Вариант 2 - с помощью row_width и insert.
# choice = InlineKeyboardMarkup(row_width=2)
# Key1 = InlineKeyboardButton(text="Начнем", callback_data=choice_callback.new(state="Start", answer="Начнем"))
# choice.insert(Key1)
# Key2 = InlineKeyboardButton(text="Зачем?", callback_data="choice:Start:Зачем?")
# choice.insert(Key2)

choice02 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Понятно! К делу!", callback_data="choice:Start_Call01:Начнем")
    ]
])

choice03 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Я уже знаком с термометром.", callback_data="choice:Start_Call02:Уже_знаком")
    ],
    [
        InlineKeyboardButton(text="Интересно! Что это такое?", callback_data="choice:Start_Call02:Интересно!")
    ]
])

choice04 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Все понятно.", callback_data="choice:Start_Call02:Уже_знаком")
    ]
])

choice05 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Договорились! Понятно.", callback_data="choice:Start_Call03:Договорились")
    ]
])