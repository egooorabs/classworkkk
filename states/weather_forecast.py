from aiogram.fsm.state import State, StatesGroup

class Weather_Forecast(StatesGroup):
    city = State()
    time = State()