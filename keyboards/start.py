from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



keyboard_start_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода☀️', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь🆘', callback_data='help')],
        [InlineKeyboardButton(text='Версия💻', callback_data='version')],
        [InlineKeyboardButton(text='Добавить кнопки⌨', callback_data='button')]
    ])

keyboard_back = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад⬅️', callback_data='back')]
    ])

keyboard_back_next = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода☀️', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь🆘', callback_data='help')],
        [InlineKeyboardButton(text='Версия💻', callback_data='version')]
        #[InlineKeyboardButton(text='Добавить кнопки⌨', callback_data='button')]
    ])

keyboard_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="☀️Погода☀️", callback_data='weather'),
            KeyboardButton(text="🆘", callback_data='help'),
            KeyboardButton(text="💻Версия💻", callback_data='version'),
        ]
    ], resize_keyboard=True)