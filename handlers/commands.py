from aiogram import types, Router
from aiogram.filters import Command
from keyboards.start import *
from weather_func import get_weather_func
from db import Database
from config import admin_tg_id


router = Router()
db = Database('database.db')

@router.message(Command("button"))
async def handle_buttons(message: types.Message):
    await message.answer(
        text="Кнопки успешно добавлены",
        reply_markup=keyboard_markup
    )

@router.message(Command("weather"))
async def weather_handler(message: types.Message):
    if message.chat.type == 'private':
        if not await db.user_exists(message.from_user.id):
            await db.add_user(message.from_user.id)
    await message.answer("Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00.", reply_markup=keyboard_back)

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await message.answer('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"', reply_markup=keyboard_back)

@router.message(Command("version"))
async def version_handler(message: types.Message):
    await message.answer("Обновление от 24 апреля 2024 года. Исправлены проблемы, связанные с работой кнопок в стартовом сообщении, а, также, ряд мелких ошибок. Если обнаружил баг, пиши: @e_gooor_abs", reply_markup=keyboard_back)

@router.message(Command("info"))
async def team_handler(message: types.Message):
    await message.answer("С уважением, команда разработчиков NET", reply_markup=keyboard_back)

@router.message(Command("main1"))
async def developer_handler(message: types.Message):
    await message.answer("Привет от @e_gooor_abs", reply_markup=keyboard_back)

@router.message(Command("send"))
async def send_handler(message: types.Message):
    from main import bot
    if message.chat.type == 'private':
        if message.from_user.id == admin_tg_id:
            text = message.text[6:]
            users = await db.get_users()
            count_sent = 0
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if row[1] != 1:
                        await db.set_active(row[0], 1)
                    count_sent += 1
                except:
                    await db.set_active(row[0], 0)
            await message.reply(f'Сообщение успешно отправлено {count_sent} пользователям')
        else: await message.answer("Отказано в доступе")

@router.message(Command("users"))
async def list_users_handler(message: types.Message):
    if message.chat.type == 'private':
        if message.from_user.id == admin_tg_id:
            users = await db.get_users()
            if users:
                user_list = "\n".join([f"User ID: {row[0]}, Active: {row[1]}" for row in users])
                await message.answer(f"Список пользователей:\n{user_list}")
            else:
                await message.reply("Нет зарегистрированных пользователей.")
        else:
            await message.answer("Отказано в доступе")



@router.message()
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
        await get_weather_func(message)
