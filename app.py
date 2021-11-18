from aiogram import executor

from loader import dp
from utils.db_api.database import open_db, close_db
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # пропуск накопившихся апдейтов
    # await dispatcher.skip_updates() - использовал соответствующий ключ при запуске обработки
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    # Уведомляем про запуск
    await on_startup_notify(dispatcher)
    # Открываем соединение с БД
    await open_db()


async def on_shutdown(dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()
    # Закрываем соединение с БД
    await close_db()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown, skip_updates=True)
