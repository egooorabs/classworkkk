from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

forecast_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена❌', callback_data='cancel_forecast')]
])

forecast_choose_time = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='0️⃣:0️⃣0️⃣', callback_data='weather_time_0'),
        InlineKeyboardButton(text='3️⃣:0️⃣0️⃣', callback_data='weather_time_3'),
    ],
    [
        InlineKeyboardButton(text='6️⃣:0️⃣0️⃣', callback_data='weather_time_6'),
        InlineKeyboardButton(text='9️⃣:0️⃣0️⃣', callback_data='weather_time_9'),
    ],
    [
        InlineKeyboardButton(text='1️⃣2️⃣:0️⃣0️⃣', callback_data='weather_time_12'),
        InlineKeyboardButton(text='1️⃣5️⃣:0️⃣0️⃣', callback_data='weather_time_15'),
    ],
    [
        InlineKeyboardButton(text='1️⃣8️⃣:0️⃣0️⃣', callback_data='weather_time_18'),
        InlineKeyboardButton(text='2️⃣1️⃣:0️⃣0️⃣', callback_data='weather_time_21'),
    ],
    [
        InlineKeyboardButton(text='Текущее время', callback_data='weather_time_current'),
    ],
    [
        InlineKeyboardButton(text='Назад⬅️', callback_data='forecast')
    ],
    [
        #InlineKeyboardButton(text='Отмена❌️', callback_data='cancel_forecast')
    ]])

