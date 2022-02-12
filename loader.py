from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.contrib.fsm_storage.files import JSONStorage
#from aiogram.contrib.fsm_storage.redis import RedisStorage2

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()  # м.б. будет быстрее чем JSONStorage(path="FSM.json")
#storage = JSONStorage(path="FSM.json")
#storage = RedisStorage2(host=config.REDIS_HOST, db=5, port=config.REDIS_PORT, password=config.REDIS_PASS)

dp = Dispatcher(bot, storage=storage)

LAST_DAY = 14  # Последний день опроса - во время отладки меняем c 18 на 1<х<18
SEC_IN_H = 3600  # секунд в часу - во время отладки меняем c 3600 на 60
SEC_IN_M = 60  # секунд в минуте - во время отладки меняем c 60 на 1
HOUR_IN_DAY = 24  # часов в дне - во время отладки меняем c 24 на 60 (чтобы отсчет шел с конца часа)
# SEC_IN_H = 60  # секунд в часу - во время отладки меняем c 3600 на 60
# SEC_IN_M = 1  # секунд в минуте - во время отладки меняем c 60 на 1
# HOUR_IN_DAY = 60  # часов в дне - во время отладки меняем c 24 на 60 (чтобы отсчет шел с конца часа)

LAST_DAY_2 = 29  # Последний день опроса после желания пользователя продолжить опрос еще 14 дней
