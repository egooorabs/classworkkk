from aiogram import Dispatcher

from handlers import commands, start
def include_routers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        commands.router,
    )
