from aiogram import types, Router
from aiogram.filters import Command
from keyboards.start import *
from weather_body import get_weather


router = Router()

@router.message(Command("button"))
async def handle_buttons(message: types.Message):
    await message.answer(
        text="Кнопки успешно добавлены",
        reply_markup=keyboard_markup
    )

@router.message(Command("weather"))
async def weather_handler(message: types.Message):
    await message.answer("Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время.")

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00")
    await message.answer('Запрос вводи в формате "Населенный пункт ЧЧ:ММ"')

@router.message(Command("version"))
async def version_handler(message: types.Message):
    await message.answer("Обновление от 24 апреля 2024 года. Исправлены проблемы, связанные с работой кнопок в стартовом сообщении, а, также, ряд мелких ошибок. Если обнаружил баг, пиши: @e_gooor_abs")

@router.message(Command("info"))
async def team_handler(message: types.Message):
    await message.answer("С уважением, команда разработчиков NET")

@router.message(Command("main1"))
async def developer_handler(message: types.Message):
    await message.answer("Привет от @e_gooor_abs")


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
        await get_weather(message)
