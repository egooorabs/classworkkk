import datetime
import requests
from aiogram import Router, types
from config import open_weather_token
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()

@router.message()
async def get_weather(message: types.Message):
    try:
        city, time_str = message.text.split(maxsplit=1)
        time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()

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

            inline_markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Поделиться', switch_inline_query='')]
            ])
            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time_obj.strftime('%H:%M')}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=inline_markup
                                )
        else:
            await message.reply("Прогноз погоды на указанное время не найден.")


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
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
            )

            data = r.json()
            city = data["name"]
            cur_weather = data["main"]["temp"]
            weather_description = data["weather"][0]["main"]
            wd = code_to_smile.get(weather_description, "Посмотри в окно, не пойму что там за погода!")
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.timedelta(seconds=data["sys"]["sunset"] - data["sys"]["sunrise"])

            inline_markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Поделиться', switch_inline_query='')]
            ])
            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=inline_markup
                                )


        except:
            await message.reply("\U00002620 Извините, я не понимаю ваш запрос. Проверьте название города \U00002620")
            await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")

    except Exception as e:
        print(e)
        await message.reply("\U00002620 Проверьте название города и формат времени \U00002620")
        await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")
