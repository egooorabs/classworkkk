
@dp.message()
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
            wd = weather_description
            humidity = weather_forecast["main"]["humidity"]
            pressure = weather_forecast["main"]["pressure"]
            wind = weather_forecast["wind"]["speed"]

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time_obj.strftime('%H:%M')}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"***Хорошего дня!***"
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
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]

            else:
                wd = "Посмотри в окно, не пойму что там за погода!"
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***"
                                )


        except:
            await message.reply("\U00002620 Извините, я не понимаю ваш запрос. Проверьте название города \U00002620")
            await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")

    except Exception as e:
        print(e)
        await message.reply("\U00002620 Проверьте название города и формат времени \U00002620")
        await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")

async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())



import datetime
import requests
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from config import tg_bot_token, open_weather_token




bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


#router = Router()
#@router.message(Command("start"))
#async def start_handler(msg: Message):
    #await bot.set_my_commands(BotCommand(command ='start', description = 'Запуск бота'))

#@router.callback_query(F.data == '1')
#async def callback_query_handler(callback_query:CallbackQuery):
    #await callback_query.message.answer(text='Разработка')

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    weather_button = KeyboardButton("Погода")
    help_button = KeyboardButton("Помощь")
    version_button = KeyboardButton("Версия")
    keyboard_markup.add(weather_button, help_button, version_button)
    await message.reply("Привет! Нажми на кнопку, чтобы получить погоду или помощь.", reply_markup=keyboard_markup)

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply(
        "Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await message.reply('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"')


@dp.message_handler(commands=["weather"])
async def weather_command(message: types.Message):
    #keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    #yandex_weather_button = KeyboardButton("Яндекс Погода")
    #openweather_button = KeyboardButton("OpenWeatherMap")
    #keyboard_markup.add(yandex_weather_button, openweather_button)
    await message.reply(
        "Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.")

@dp.message_handler(content_types=["photo"])
async def handle_photo(message: types.Message):
    await message.reply("Спасибо за фото! Я обработаю его как только смогу.")

@dp.message_handler(content_types=["video"])
async def handle_video(message: types.Message):
    await message.reply("Спасибо за видео! Я обработаю его как только смогу.")

@dp.message_handler(content_types=["sticker", "emoji"])
async def handle_sticker(message: types.Message):
    await message.reply("Спасибо за стикер! Я обработаю его как только смогу.")

@dp.message_handler(content_types=["video_note"])
async def handle_video_message(message: types.Message):
    await message.reply("Спасибо за кружок! Я обработаю его как только смогу.")

@dp.message_handler(content_types=["voice"])
async def handle_voice_message(message: types.Message):
    await message.reply("Спасибо за голосовушку! Я обработаю его как только смогу.")

@dp.message_handler(commands=["info"])
async def team_command(message: types.Message):
    await message.reply("С уважением, команда разработчиков NET")

@dp.message_handler(commands=["main1"])
async def developer_command(message: types.Message):
    await message.reply("Привет от @e_gooor_abs")

@dp.message_handler(commands=["version"])
async def version_command(message: types.Message):
    await message.reply("Обновление от 16 апреля 2024 года. Исправлены ошибки, связанные с распознаванием различных типов сообщений. Если обнаружил баг, пиши: @e_gooor_abs")


@dp.message_handler()
async def handle_text(message: types.Message):
    if message.text == "Помощь":
        await help_command(message)
    elif message.text == "Погода":
        await weather_command(message)
    elif message.text == "Версия":
        await version_command(message)
    else:
        await get_weather(message)



async def get_weather(message: types.Message):
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
            wd = weather_description
            humidity = weather_forecast["main"]["humidity"]
            pressure = weather_forecast["main"]["pressure"]
            wind = weather_forecast["wind"]["speed"]

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time_obj.strftime('%H:%M')}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"***Хорошего дня!***"
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
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Посмотри в окно, не пойму что там за погода!"

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
            sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
            length_of_the_day = datetime.datetime.fromtimestamp(
                data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
                data["sys"]["sunrise"])

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***"
                                )

        except:
            await message.reply("\U00002620 Извините, я не понимаю ваш запрос. Проверьте название города \U00002620")
            await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")
    except Exception as e:
        print(e)
        await message.reply("\U00002620 Проверьте название города и формат времени \U00002620")
        await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")

if __name__ == '__main__':
    executor.start_polling(dp)



import requests
import datetime
from pprint import pprint
from config import open_weather_token


def get_weather(city, open_weather_token):

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
        pprint(data)

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        print(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!"
              )

    except Exception as ex:
        print(ex)
        print("Проверьте название города")


def main():
    city = input("Введите город: ")
    get_weather(city, open_weather_token)


if __name__ == '__main__':
    main()



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


            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time_obj.strftime('%H:%M')}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share
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


            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share
                                )


        except:
            await message.reply("\U00002620 Извините, я не понимаю ваш запрос. Проверьте название города \U00002620")
            await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")

    except Exception as e:
        print(e)
        await message.reply("\U00002620 Проверьте название города и формат времени \U00002620")
        await message.reply("Предупреждение: Я принимаю запросы на русском и английском языках")


@router.message
async def get_weather_function(message: types.Message):
    from main import bot
    @router.message()
    async def get_weather(message: types.Message):
        try:
            await message.reply("Введите название города:")
        except Exception as e:
            print(e)

    @router.callback_query(lambda c: c.data == '', state="*")
    async def process_callback_button(message: types.Message):
        try:
            await bot.send_message(text="Выберите время:", reply_markup=keyboard_time)
        except Exception as e:
            print(e)

    @router.callback_query(lambda c: c.data != '', state="*")
    async def process_time_selection(callback_query: types.CallbackQuery):
        try:
            city = callback_query.message.text
            time_str = callback_query.data
            time_obj = datetime.datetime.strptime(time_str, "%H:%M").time()

            await handle_weather_request(callback_query.message, city, time_obj)
        except Exception as e:
            print(e)

    async def handle_weather_request(message, city, time_obj=None):
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        weather_forecast = None
        if time_obj:
            for forecast in data['list']:
                forecast_time = datetime.datetime.fromtimestamp(forecast['dt']).time()
                if forecast_time.hour == time_obj.hour and forecast_time.minute == time_obj.minute:
                    weather_forecast = forecast
                    break
        else:
            weather_forecast = data['list'][0]

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

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share
                                )
        else:
            await message.reply("Прогноз погоды не найден.")
    await message.reply('Что-то пошло не так:(')


@router.message()
async def get_weather(message: types.Message, state: FSMContext):
    # Получаем данные о городе и времени из состояния
    async with state.proxy() as data:
        city = data.get('city')
        time = data.get('time')

    if city is None or time is None:
        await message.reply("Сначала укажите город и время для получения прогноза погоды.")
        return

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        weather_forecast = None
        for forecast in data['list']:
            forecast_time = datetime.datetime.fromtimestamp(forecast['dt']).time()
            if forecast_time.hour == time.hour and forecast_time.minute == time.minute:
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

            await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                                f"Прогноз погоды в городе {city} на {time_obj.strftime('%H:%M')}:\n"
                                f"Температура: {cur_weather}C° {wd}\n"
                                f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
                                f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
                                f"***Хорошего дня!***",
                                reply_markup=keyboard_share
                                )
        else:
            await message.reply("Прогноз погоды на указанное время не найден.")


    except Exception as e:
        print(e)
        await message.reply("Что-то пошло не так. Пожалуйста, попробуйте позже.")



from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.weather_forecast import Weather_Forecast
from keyboards.weather_forecast import *
import datetime
from weather_body import get_weather

router = Router()

@router.callback_query(F.data == 'forecast')
async def forecast_callback_handler(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.answer('Введите название населенного пункта', reply_markup=forecast_cancel)
    await state.set_state(Weather_Forecast.city)

@router.message(Weather_Forecast.city)
async def set_city_by_forecast_handler(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await state.set_state(Weather_Forecast.time)
    await message.answer("Выберите подходящее время", reply_markup=forecast_choose_time)

@router.callback_query(F.data.startswith('time_') and Weather_Forecast.time)
async def set_time_by_forecast_handler(callback_query: CallbackQuery,state: FSMContext):
    time = {'time_0': '0:00', 'time_3': '3:00' }[callback_query.data]
    await state.update_data(time=time)
    await callback_query.message.answer(str(await state.get_data()))
    await state.clear()


@router.callback_query(F.data == 'weather_time_0')
async def set_time_0_handler(callback_query: CallbackQuery, state: FSMContext):
    time = datetime.datetime.strptime("00:00", "%H:%M").time()

    # Сохраняем время в состоянии
    await state.update_data(time=time)

    # Отправляем сообщение об успешном выборе времени
    await callback_query.message.answer("Время успешно выбрано: 00:00")

    # Получаем город из состояния
    data = await state.get_data()
    city = data.get('city')
    time = data.get('time')

    # Проверяем, что город был сохранен в состоянии
    if city is None:
        await callback_query.answer("Сначала укажите город для получения прогноза погоды.")
        return

    # Вызываем функцию get_weather с передачей города и времени
    await get_weather(city, time)

@router.callback_query(Weather_Forecast.time)
async def set_time_by_weather_forecast_handler(message: Message, state: FSMContext):
    try:
        await state.update_data(time=int)
    except ValueError:
        await message.answer('Вы неверно ввели время')
        await message.answer(text='Выберите подходящее для вас время', reply_markup=forecast_choose_time)

@router.callback_query(F.data == 'cancel_forecast')
async def cancel_forecast(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback_query.message.answer('Отмена запроса')
