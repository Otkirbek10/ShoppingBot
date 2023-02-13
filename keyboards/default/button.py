from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

cancel = '🚫 Bekor qilish'
back = '🔙 Orqaga'



back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=back)]
    ],
    resize_keyboard=True,
    selective=True
)