import asyncio
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import Command
from aiogram.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import open_weather_token, tg_bot_token
import datetime
import requests

bot = Bot(token=tg_bot_token)
dp = Dispatcher()

router = Router()
dp.include_router(router)


@dp.message(Command("start"))
async def start_handler(message: types.Message):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода☀️', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь🆘', callback_data='help')],
        [InlineKeyboardButton(text='Версия💻', callback_data='version')],
        [InlineKeyboardButton(text='Добавить кнопки⌨', callback_data='button')]
    ])

    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='version', description='Версия'),
        BotCommand(command='button', description='Добавить кнопки'),
    ])

    await message.answer(text='Привет! Нажми на кнопку, чтобы получить погоду или помощь. Вы можете выбрать: "Добавить кнопки", чтобы взаимодействие со мной стало еще удобнее', reply_markup=inline_markup)

@router.callback_query(F.data == "button")
async def handle_buttons(callback_query: CallbackQuery):
    keyboard_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="☀️Погода☀️", callback_data='weather'),
            KeyboardButton(text="🆘", callback_data='help'),
            KeyboardButton(text="💻Версия💻", callback_data='version'),
        ]
    ], resize_keyboard=True)
    await callback_query.message.answer(
        text="Кнопки успешно добавлены",
        reply_markup=keyboard_markup
    )

@dp.message(Command("button"))
async def handle_buttons(message: types.Message):
    keyboard_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="☀️Погода☀️", callback_data='weather'),
            KeyboardButton(text="🆘", callback_data='help'),
            KeyboardButton(text="💻Версия💻", callback_data='version'),
        ]
    ], resize_keyboard=True)
    await message.answer(
        text="Кнопки успешно добавлены",
        reply_markup=keyboard_markup
    )

@router.callback_query(F.data == 'weather')
async def weather_callback_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад⬅️', callback_data='back')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text="Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.",
        reply_markup=inline_markup
    )

@dp.message(Command("weather"))
async def weather_handler(message: types.Message):
    await message.answer("Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.")


@router.callback_query(F.data == 'help')
async def weather_callback_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад⬅️', callback_data='back')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00. Запрос вводи в формате "Населенный пункт ЧЧ:ММ"',
        reply_markup=inline_markup
    )

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await message.answer('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"')


@router.callback_query(F.data == 'version')
async def weather_callback_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад⬅️', callback_data='back')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Обновление от 16 апреля 2024 года. Исправлены ошибки, связанные с распознаванием различных типов сообщений. Если обнаружил баг, пиши: @e_gooor_abs',
        reply_markup=inline_markup
    )
@dp.message(Command("version"))
async def version_handler(message: types.Message):
    await message.answer("Обновление от 24 апреля 2024 года. Исправлены проблемы, связанные с работой кнопок в стартовом сообщении, а, также, ряд мелких ошибок. Если обнаружил баг, пиши: @e_gooor_abs")

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода☀️', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь🆘', callback_data='help')],
        [InlineKeyboardButton(text='Версия💻', callback_data='version')]
        #[InlineKeyboardButton(text='Добавить кнопки⌨', callback_data='button')]
    ])
    await callback_query.message.delete()
    await callback_query.message.answer(
        text="Нажми на кнопку, чтобы получить погоду или помощь.",
        reply_markup=inline_markup
    )

@dp.message(Command("info"))
async def team_handler(message: types.Message):
    await message.answer("С уважением, команда разработчиков NET")

@dp.message(Command("main1"))
async def developer_handler(message: types.Message):
    await message.answer("Привет от @e_gooor_abs")


@dp.message()
async def handle_text(message: types.Message):
    if message.text == '🆘':
        await help_handler(message)
    elif message.text == 'Помощь':
        await help_handler(message)
    elif message.text == '☀️Погода☀️':
        await weather_handler(message)
    elif message.text == 'Погода':
        await weather_handler(message)
    elif message.text == '💻Версия💻':
        await version_handler(message)
    elif message.text == 'Версия':
        await version_handler(message)
    elif message.text == 'Инфа':
        await team_handler(message)
    elif message.text == 'Разраб':
        await developer_handler(message)
    elif message.text == 'Кнопки':
        await handle_buttons(message)
    else:
        await get_weather(message)


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
