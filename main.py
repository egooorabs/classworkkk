import asyncio
from aiogram import Bot, Dispatcher, Router
from config import tg_bot_token
from handlers import include_routers
from db import Database
from send_m_db import DB
from datetime import datetime, timedelta, time
from handlers.start import on_startup



bot = Bot(token=tg_bot_token)
dp = Dispatcher()
db = Database('database.db')
dbb = DB('sqlite.db')
#SEND_TIME = None


router = Router()
#dp.include_router(router)


#async def main():
    #include_routers(dp)
    #await dp.start_polling(bot)



async def main():
    '''Старт бота'''
    dp.startup.register(on_startup)
    include_routers(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())


