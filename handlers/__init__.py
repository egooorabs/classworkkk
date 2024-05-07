from aiogram import Dispatcher

from handlers import commands, start, weather_forecast
def include_routers(dp: Dispatcher):
    dp.include_routers(
        start.router,
        weather_forecast.router,
        commands.router,
    )
