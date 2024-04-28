@router.message(Command("start"))
async def start_handler(message: types.Message):
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='version', description='Версия'),
    ])

    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперед', callback_data='next')]
    ])
    await message.answer(text="Страница 1", reply_markup=inline_markup)

@router.callback_query(F.data == 'next')
async def next_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Страница 2',
        reply_markup=inline_markup
    )

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вперед', callback_data='next')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text="Страница 1",
        reply_markup=inline_markup
    )

@router.callback_query(Command("start"))
async def inline_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("Погода", callback_data="weather")
    button2 = InlineKeyboardButton("Помощь", callback_data="help")
    button3 = InlineKeyboardButton("Версия", callback_data="version")
    inline_markup.add(button1, button2, button3)
    await callback_query.message.answer("Выберите действие:", reply_markup=inline_markup)



import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from config import open_weather_token, tg_bot_token
import datetime
import requests

bot = Bot(token=tg_bot_token)
dp = Dispatcher()

router = Router()
dp.include_router(router)


@router.message(Command("start"))
async def start_handler(message: types.Message):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь', callback_data='help')],
        [InlineKeyboardButton(text='Версия', callback_data='version')]
    ])

    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='version', description='Версия'),
    ])

    await message.answer_text(text="Привет! Нажми на кнопку, чтобы получить погоду или помощь.", reply_markup=inline_markup)



@router.callback_query(F.data == 'weather')
async def weather_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.")

@router.callback_query(F.data == 'help')
async def help_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await callback_query.message.answer('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"')

@router.callback_query(F.data == 'version')
async def version_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.answer("Обновление от 16 апреля 2024 года. Исправлены ошибки, связанные с распознаванием различных типов сообщений. Если обнаружил баг, пиши: @e_gooor_abs")


@dp.message()
async def handle_text(message: types.Message):
    if message.text == 'Помощь':
        await help_command(message)
    elif message.text == 'Погода':
        await weather_command(message)
    elif message.text == 'Версия':
        await version_command(message)
    else:
        await get_weather(message)

async def help_command(message: types.Message):
    await message.reply(
        "Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await message.reply('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"')

async def weather_command(message: types.Message):
    await message.reply(
        "Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.")

async def version_command(message: types.Message):
    await message.reply("Обновление от 16 апреля 2024 года. Исправлены ошибки, связанные с распознаванием различных типов сообщений. Если обнаружил баг, пиши: @e_gooor_abs")



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
