from config import dp
from aiogram.utils import executor
from functions import update_prices
import aioschedule
import asyncio
import start
import support
import admin
import userfaq
import catalog
import box
import usermenu
import review


# made by mlt_melt
# you can visit my github page - https://github.com/mlt_melt


async def timer():
    aioschedule.every(1).day.at('05:00').do(update_prices)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(5)


async def start_timer(_):
    asyncio.create_task(timer())



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=start_timer)