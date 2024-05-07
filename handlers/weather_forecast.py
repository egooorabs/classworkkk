from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext


from states.weather_forecast import Weather_Forecast
from keyboards.weather_forecast import *
from keyboards.start import *
from weather_body import get_weather_handler



router = Router()

@router.callback_query(F.data == 'forecast')
async def forecast_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Укажите название населенного пункта', reply_markup=forecast_cancel)
    await state.set_state(Weather_Forecast.city)

@router.message(Weather_Forecast.city)
async def set_city_by_forecast_handler(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Weather_Forecast.time)
    await message.answer("Выберите подходящее время", reply_markup=forecast_choose_time)

@router.callback_query(F.data.startswith('weather_time_') and Weather_Forecast.time)
async def set_time_by_forecast_handler(callback_query: CallbackQuery, state: FSMContext):
    time = {
        'weather_time_0': '0:00',
        'weather_time_3': '3:00',
        'weather_time_6': '6:00',
        'weather_time_9': '9:00',
        'weather_time_12': '12:00',
        'weather_time_15': '15:00',
        'weather_time_18': '18:00',
        'weather_time_21': '21:00',
        'weather_time_current': '',
    }[callback_query.data]
    await state.update_data(time=time)
    if time:
        await callback_query.message.answer("Время успешно выбрано: " + time)
        await get_weather_handler(callback_query, state)
    else:
        await callback_query.message.answer("Текущее время успешно выбрано")
        await get_weather_handler(callback_query, state)



@router.callback_query(F.data == 'cancel_forecast')
async def cancel_forecast(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer('Отмена запроса')
    await callback_query.message.delete()
    await callback_query.message.answer(
        text="Нажми на кнопку, чтобы получить погоду или помощь.",
        reply_markup=keyboard_start_next
    )






@router.message(Weather_Forecast.time)
async def set_time_by_weather_forecast_handler(callback_query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        city = data.get('city')
        time = data.get('time')

        if city is None:
            await callback_query.message.answer("Сначала укажите город для получения прогноза погоды.")
            return

        await get_weather_handler(city, time)

    except ValueError:
        await callback_query.message.answer("Текущее время успешно выбрано")
        await get_weather_handler(callback_query, state)






