from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.weather_forecast import Weather_Forecast
from keyboards.weather_forecast import *
from keyboards.start import *
import datetime
import requests
from config import open_weather_token


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

@router.callback_query(F.data.startswith('weather_time_'))
async def get_weather_handler(callback: types.CallbackQuery, state: FSMContext):
    print(state, type(state))
    data = await state.get_data()
    print(data)

    city = data.get('city', None)
    time = data.get('time', None)


    if city is None or time is None:
        await callback.message.answer("Сначала укажите город и время для получения прогноза погоды.")
        return

    try:
        time_obj = datetime.datetime.strptime(time, "%H:%M").time()

        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        weather_forecast = None
        for forecast in data['list']:
            forecast_time = datetime.datetime.fromtimestamp(forecast['dt']).time()
            if forecast_time.hour == time_obj.hour and forecast_time.minute == time_obj.minute:
                weather_forecast = forecast
                break

        if weather_forecast:
            cur_weather = weather_forecast["main"]["temp"]
            weather_description = weather_forecast["weather"][0]["main"]
            code_to_smile = {
                "Clear": "Ясно \U00002600",
                "Clouds": "Облачно \U00002601",
                "Rain": "Дождь \U00002614",
                "Drizzle": "Дождь \U00002614",
                "Thunderstorm": "Гроза \U000026A1",
                "Snow": "Снег \U0001F328",
                "Mist": "Туман \U0001F32B"
            }
            wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!")
            humidity = weather_forecast["main"]["humidity"]
            pressure = weather_forecast["main"]["pressure"]
            wind = weather_forecast["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["city"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["city"]["sunset"])
            length_of_the_day = datetime.timedelta(seconds=data["city"]["sunset"] - data["city"]["sunrise"])

            await callback.message.answer(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share)
            await state.clear()
        else:
            await callback.message.answer("Прогноз погоды на указанное время не найден.")

    except ValueError:
        code_to_smile = {
            "Clear": "Ясно \U00002600",
            "Clouds": "Облачно \U00002601",
            "Rain": "Дождь \U00002614",
            "Drizzle": "Дождь \U00002614",
            "Thunderstorm": "Гроза \U000026A1",
            "Snow": "Снег \U0001F328",
            "Mist": "Туман \U0001F32B"
        }

        try:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric"
            )

            data = r.json()
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!")
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.timedelta(seconds=data["sys"]["sunset"] - data["sys"]["sunrise"])

            await callback.message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share
                                )
            await state.clear()

        except:
            await callback.message.answer("\U00002620 Извините, я не понимаю ваш запрос. Проверьте название города \U00002620")
            await callback.message.answer("Предупреждение: Я принимаю запросы на русском и английском языках", reply_markup=keyboard_back)

    except Exception as e:
        print(e)
        await callback.message.answer("\U00002620 Что-то пошло не так. Пожалуйста, попробуйте позже. \U00002620")
        await callback.message.answer("Предупреждение: Я принимаю запросы на русском и английском языках")
        await callback.message.answer("Если ошибка сохраняется в течение длительного промежутка времени, обращайтесь к @e_gooor_abs с подробно-изложенной ситуацией")







