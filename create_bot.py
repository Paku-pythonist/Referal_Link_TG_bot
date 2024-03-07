from aiogram import Bot
from aiogram.dispatcher import Dispatcher   # Обработка событий.
from aiogram.contrib.fsm_storage.memory import MemoryStorage   # БД в памяти.

from data import config


# TOKEN = os.getenv('TOKEN')
TOKEN = config['TOKEN']

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)