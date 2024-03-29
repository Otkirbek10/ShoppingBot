from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from loader import db,dp
from aiogram.utils.callback_data import CallbackData

category_cb = CallbackData('category', 'id', 'action')


def create_category():

    global category_cb
    markup = InlineKeyboardMarkup(row_width=2)
    for id,name in db.select_all_categories():
        markup.add(InlineKeyboardButton(name,callback_data=category_cb.new(id=id,action = 'watch')))
    markup.add(InlineKeyboardButton(text='🔙 Orqaga',callback_data='back'))
    return markup


def aksiya_markup(name,url):

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f'{name}', callback_data=f"{url}"))

    return markup