from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import DB



db = DB('db.db')

bot = Bot(token='', parse_mode='html') # bot's token

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


admins = []                         # list of admin's IDs (for example - [345345234, 557546745, 745985797])
feedback_channel_url = ''           # [str]  url of the channel with feedbacks (for example: https://t.me/+RDE2gELnj6A1NTRa)
feedback_channel_id = int()         # [int]  id of the channel with feedbacks (for example: -1001802130500)
bot_url = ''                        # [str]  url of the bot (for example: https://t.me/test_bot)