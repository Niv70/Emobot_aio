from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.files import JSONStorage

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()  # м.б. будет быстрее чем JSONStorage(path="FSM.json")
dp = Dispatcher(bot, storage=storage)

LAST_DAY = 14  # Последний день опроса - во время отладки меняем c 18 на 1<х<18
SEC_IN_H = 60  # секунд в часу - во время отладки меняем c 3600 на 60
SEC_IN_M = 1  # секунд в минуте - во время отладки меняем c 60 на 1
HOUR_IN_DAY = 60  # часов в дне - во время отладки меняем c 24 на 60 (чтобы отсчет шел с конца часа)
