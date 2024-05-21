import asyncio
import datetime
from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.types import BotCommand, CallbackQuery, Message
from keyboards.start import *
from db import Database
from send_m_db import DB, User, UserDoesNotExist
from datetime import datetime, timedelta, time
#from send_m_db import *


router = Router()
db = Database('database.db')
dbb = DB('sqlite.db')
SEND_TIME = None


@router.message(Command("set_time"))
async def set_time_handler(message: Message):
    try:
        print(message.text)
        time_split = message.text.replace('/set_time ', '').split(':')
        hour = int(time_split[0])
        min = int(time_split[1])
        global SEND_TIME
        SEND_TIME = time(hour, min)
        try:
            user = User.get_by_id(1)
            user.time = SEND_TIME
            user.save()
            await message.answer(text='Время успешно установлено!')
        except UserDoesNotExist:
            user = User.create(id=1, time=SEND_TIME)
            await message.answer(text='Время успешно установлено!')

    except ValueError as e:
        await message.answer(text=f'Ошибка: Некорректный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.')
    except Exception as e:
        await message.answer(text=f'Произошла ошибка: {e}')



@router.message(Command("start"))
async def start_handler(message: types.Message):
    from main import bot
    await bot.set_my_commands([
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='version', description='Версия'),
        BotCommand(command='button', description='Добавить кнопки'),
        BotCommand(command='set_time', description='Установить время'),
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


async def get_time_notify():
    now = datetime.now()
    users = User.filter(User.time > now).order_by(User.time.asc())
    if users.count() > 0:
        return (users.first()).time


async def send_admin():
    from main import bot
    global SEND_TIME
    SEND_TIME = await get_time_notify()
    await bot.send_message(913732153, "Бот запущен!")
    while True:
        print(datetime.now().time(), SEND_TIME)
        now_time = datetime.now().time()
        now_time = time(now_time.hour, now_time.minute)
        if SEND_TIME and SEND_TIME == now_time:
            for user in User.filter(time=SEND_TIME):
                await bot.send_message(user.tg_user, 'ping')

            SEND_TIME = await get_time_notify()
            print(SEND_TIME)

        now_time = (datetime.now() + timedelta(minutes=1))
        now_time = datetime(now_time.year, now_time.month, now_time.day,
                            now_time.hour, now_time.minute)
        seconds = (now_time - datetime.now()).seconds + 1
        print(datetime.now().time(), now_time.time(), seconds)
        await asyncio.sleep(seconds)

async def on_startup():
    asyncio.create_task(send_admin())


