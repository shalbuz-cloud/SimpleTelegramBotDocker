import logging
from asyncio import get_event_loop

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN
from sql import create_pool


# from aiogram.contrib.fsm_storage.redis import RedisStorage2

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s '
                           u'[%(asctime)s] %(message)s', level=logging.INFO)
loop = get_event_loop()


# Set up storage (either in Redis or Memory)
storage = MemoryStorage()
# storage = RedisStorage2()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=storage)

db = loop.run_until_complete(create_pool())
