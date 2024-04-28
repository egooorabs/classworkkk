import asyncio
from aiogram import Bot, Dispatcher, Router
from config import tg_bot_token
from handlers import include_routers


bot = Bot(token=tg_bot_token)
dp = Dispatcher()

router = Router()
dp.include_router(router)

async def main():
    include_routers(dp)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
