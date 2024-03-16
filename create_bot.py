from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import os

from aiogram import types
import openai

storage=MemoryStorage()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot,storage=storage)

