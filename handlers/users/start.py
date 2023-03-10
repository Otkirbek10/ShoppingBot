
import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardMarkup
from data import config
# from aiogram.dispatcher.filters import
from filters import IsAdmin
from data.config import ADMINS
from loader import dp, db, bot

user_message = 'đââī¸ Foydalanuvchi'
admin_message = 'đ¨âđ§ Admin'

menu  = 'đ Menyu'
cart = 'đ Korzina'
about = 'âšī¸ Biz haqimizda' 

settings = 'âī¸ Katalog sozlamalari'
orders = 'đ Buyurtmalar'
questions = 'â Savollar'

@dp.message_handler(IsAdmin(),commands='start',state='*')
async def cmd_start(message: types.Message):

    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)

    markup.row(admin_message, user_message)

    await message.answer(f"đ Salom {message.from_user.full_name}! đ¤ Men sizning botingizman \n\n Meni admin rejimida sozlashni unutmang!", reply_markup=markup)

@dp.message_handler(IsAdmin(),text=user_message)
async def on_user(message:types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    markup.add(menu)
    markup.add(about,cart)
    await message.answer('Foydalanuvchi rejimi yoqildi',reply_markup=markup)

    tg_id = message.chat.id
    if tg_id in config.ADMINS:
        config.ADMINS.remove(tg_id)

@dp.message_handler(IsAdmin(),text=admin_message)
async def on_user(message:types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    markup.add(settings)
    markup.add(questions, orders)
    markup.add(user_message)
    await message.answer('Admin rejimi yoqildi',reply_markup=markup)

    tg_id = message.chat.id
    if tg_id not in config.ADMINS:
        config.ADMINS.append(tg_id)

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    name = message.from_user.full_name
    usr = message.from_user.username
    id = message.from_user.id
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(tg_id=id,
                    name=name,user_name=usr)
        markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
        markup.add(menu)
        markup.add(about,cart)
        await message.answer(f"đ {name}.\n\nđ¤ Men  har qanday toifadagi tovarlarni sotish uchun bot-do'konman.!\n\nDavom etish uchun <b>Menu</b> bosing!!",parse_mode='Html',reply_markup=markup)

        # Adminga xabar beramiz
        count = db.count_users()[0]
        msg = f"{message.from_user.full_name} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)

    except sqlite3.IntegrityError as err:
        markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
        markup.add(menu)
        markup.add(about,cart)
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} bazaga oldin qo'shilgan")
        await message.answer(f"đ {name}.\n\nđ¤ Men  har qanday toifadagi tovarlarni sotish uchun bot-do'konman.!\n\nDavom etish uchun <b>Menu</b> ni bosing",parse_mode='HTML',reply_markup=markup)
