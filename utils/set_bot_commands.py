from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("stop", "Остановить бота"),
            types.BotCommand("stat", "Статистика по зафиксированным эмоциям"),
            # types.BotCommand("reset", "Перезапуск бота"),
            # types.BotCommand("dbdrop", "Зачистить базу"),
            # types.BotCommand("dbcreate", "Создать таблицы"),
        ]
    )
