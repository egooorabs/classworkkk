from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

inline_markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Погода☀️', callback_data='weather')],
        [InlineKeyboardButton(text='Помощь🆘', callback_data='help')],
        [InlineKeyboardButton(text='Версия💻', callback_data='version')],
        [InlineKeyboardButton(text='Добавить кнопки⌨', callback_data='button')]
    ])

keyboard_markup = ReplyKeyboardMarkup(keyboard=[
        [
            KeyboardButton(text="☀️Погода☀️", callback_data='weather'),
            KeyboardButton(text="🆘", callback_data='help'),
            KeyboardButton(text="💻Версия💻", callback_data='version'),
        ]
    ], resize_keyboard=True)

