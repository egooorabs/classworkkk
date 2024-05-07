from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import BotCommand, CallbackQuery
from keyboards.start import *
from db import Database
from aiogram.fsm.context import FSMContext


router = Router()
db = Database('database.db')

@router.message(Command("start"))
async def start_handler(message: types.Message):
    from main import bot
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='version', description='Версия'),
        BotCommand(command='button', description='Добавить кнопки'),
    ])
    if message.chat.type == 'private':
        if not await db.user_exists(message.from_user.id):
            await db.add_user(message.from_user.id)

    await message.answer(text='Привет! Нажми на кнопку, чтобы получить погоду или помощь. Вы можете выбрать: "Добавить кнопки", чтобы взаимодействие со мной стало еще удобнее', reply_markup=keyboard_start_next)

@router.callback_query(F.data == "button")
async def handle_buttons(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Кнопки успешно добавлены",
        reply_markup=keyboard_markup
    )

@router.callback_query(F.data == 'weather')
async def weather_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        text="Напиши название населенного пункта, либо название населенного пункта и время (в формате ЧЧ:ММ), чтобы я прислал прогноз погоды на указанное время. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00.",
        reply_markup=keyboard_back
    )

@router.callback_query(F.data == 'help')
async def weather_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Я принимаю запросы на русском и английском языках. Чтобы получить прогноз погоды для вашего города, отправьте название города. Прогноз погоды могу выдать на каждые 3 часа, выбери подходщее для тебя время: 0:00, 3:00, 6:00, 9:00, 12:00, 15:00, 18:00, 21:00. Запрос вводи в формате "Населенный пункт ЧЧ:ММ"',
        reply_markup=keyboard_back
    )

@router.callback_query(F.data == 'version')
async def weather_callback_handler(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.message.answer(
        text='Обновление от 24 апреля 2024 года. Исправлены проблемы, связанные с работой кнопок в стартовом сообщении, а, также, ряд мелких ошибок. Если обнаружил баг, пиши: @e_gooor_abs',
        reply_markup=keyboard_back
    )

@router.callback_query(F.data == 'back')
async def back_handler(callback_query: CallbackQuery):
    await callback_query.message.answer(
        text="Нажми на кнопку, чтобы получить погоду или помощь.",
        reply_markup=keyboard_start_next
    )