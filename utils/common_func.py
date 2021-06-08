# Модуль общих функций (Common functions)
from aiogram.types import Message
from aiogram.dispatcher import FSMContext


# Ввод неотрицательного числа
async def get_digit(message: Message, state: FSMContext, d_min, d_max):  # d_min: int, d_max: int):
    data = await state.get_data()  # Достаем имя пользователя
    name_user = data.get("name_user")
    try:
        d = int(message.text)  # проверяем, что цифра введена корректно
    except Exception as e:
        await message.answer('Ошибка: {0}'.format(e))
        await message.answer('{0}, введи цифрами, пожалуйста!'.format(name_user))
        d = -1
    else:
        if d < d_min or d > d_max:
            await message.answer('{0}, введи значение от {1} до {2}, пожалуйста!'.format(name_user, d_min, d_max))
            d = -2
    await state.update_data(result=d)
