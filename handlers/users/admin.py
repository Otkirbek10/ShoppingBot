import asyncio
from aiogram import types
from data.config import ADMINS
from loader import dp,db,bot
import pandas as pd
import aiogram

from keyboards.default.button import menu_aks

from keyboards.inline.category import aksiya_markup
from filters import IsAdmin
from states.aksiyastate import Aksiya

from aiogram.dispatcher import FSMContext

from aiogram.types import *

aksiya = "🎉 Aksiya qo'shish"
bc = '◀️ Orqaga'
fr = '⏩ Keyingisi'

@dp.message_handler(text = "/allusers", user_id = ADMINS)
async def get_all_users(message: types.Message):
    users = db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)

@dp.message_handler(text = '/reklama',user_id = ADMINS)
async def send_ad_to_all(message:types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="Assalomu alaykum")
        await asyncio.sleep(0.05)

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")

    


@dp.message_handler(IsAdmin(),text = aksiya)
async def aksiyas(message:types.Message):
    keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(bc)
    await message.answer('Aksiyani yaratishni boshladik🚀')
    await message.answer('Aksiyaning tavsifini batafsil yozing!',reply_markup=keybord)
    await Aksiya.text.set()

@dp.message_handler(IsAdmin(),text = bc,state=Aksiya.text)
async def aksiya_s(message:types.Message,state:FSMContext):

    await message.answer('⚙️ Settings',reply_markup=menu_aks)  
    await state.finish()

@dp.message_handler(IsAdmin(),state=Aksiya.text)
async def aksiya_t(message:types.Message,state:FSMContext):

    keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(bc,fr)

    async with state.proxy() as data:
        data['text'] = message.text


    await message.answer('Aksiya rasmini yuboring!',reply_markup=keybord)
    await Aksiya.next()

@dp.message_handler(IsAdmin(),content_types=ContentType.PHOTO,state=Aksiya.photo)
async def aksiya_p(message:types.Message,state:FSMContext):

    photo = message.photo[-1].file_id

    async with state.proxy() as data:
        data['photo'] = photo


    keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add('✅Ha',"❌Yo'q")
    keybord.add(bc)
    await message.answer("Tugma qo'shishni xohlaysizmi?",reply_markup=keybord)
    await Aksiya.next()



@dp.message_handler(IsAdmin(),content_types=ContentType.TEXT,state=Aksiya.photo)
async def aksiya_ph(message:types.Message,state:FSMContext):
    msg = message.text
    if msg == fr:
        keybord = ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add('✅Ha',"❌Yo'q")
        keybord.add(bc)
        await message.answer("Post tagiga tugma qo'shishni xohlaysizmi?",reply_markup=keybord)
        await Aksiya.next()

    elif msg == bc:

        await Aksiya.text.set()
        keybord = ReplyKeyboardMarkup(resize_keyboard=True)
        keybord.add(bc)
        async with state.proxy() as data:
            text = data['text']
            await message.answer(f"<b>{text}</b> ni o'zgartirmoqchimisiz?",reply_markup=keybord)
            

    else:
        await message.answer('Iltimos rasm yuboring')

@dp.message_handler(IsAdmin(),text = bc,state=Aksiya.button)
async def aksiya_cc(message:types.Message,state:FSMContext):
    

    await Aksiya.photo.set()


    keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    keybord.add(bc,fr)
    await message.answer("Aksiya rasmini o'zgartirmoqchimisiz?",reply_markup=keybord)

@dp.message_handler(IsAdmin(),text = "✅Ha",state=Aksiya.button)
async def aksiya_cc(message:types.Message,state:FSMContext):

    await message.answer('Tugmani qanday nomlaysiz?',reply_markup=ReplyKeyboardRemove())
    await Aksiya.next()

@dp.message_handler(IsAdmin(),state=Aksiya.name)
async def button_name(message:types.Message,state:FSMContext):
    msg = message.text

    async with state.proxy() as data:
        data['name'] = msg
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(bc)
    await message.answer('Endi tugma uchun url ssilka yuboring!',reply_markup=keyboard)
    await Aksiya.next()

@dp.message_handler(IsAdmin(),content_types=ContentType.TEXT,state=Aksiya.link)
async def bc_link(message:types.Message,state:FSMContext):
    url = message.text

    if url == bc:

        await Aksiya.name.set()
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(bc)

        async with state.proxy() as data:
            name = data['name']
            await message.answer(f"<b>{name}</b> ni o'zgartirmoqchimisiz?",reply_markup=ReplyKeyboardRemove())
    else:
        async with state.proxy() as data:
            data['url'] = url
            if 'photo' in data.keys():
                photo = data['photo']
                text = data['text']
                name = data['name']
                markup = aksiya_markup(name=name,url=url)
                keyb = ReplyKeyboardMarkup(resize_keyboard=True)
                keyb.add('🚫 Bekor qilish','✅ Tasdiqlash')
                await message.answer_photo(photo=photo,caption=text,reply_markup=markup)
                await message.answer("Hammasini tasdiqlaysizmi",reply_markup=keyb)
                await Aksiya.next()

            else:
                text = data['text']
                name = data['name']
                markup = aksiya_markup(name=name,url=url)
                await message.answer(text,reply_markup=markup)
                keyb = ReplyKeyboardMarkup(resize_keyboard=True)
                keyb.add('🚫 Bekor qilish','✅ Tasdiqlash')
                await message.answer("Hammasini tasdiqlaysizmi",reply_markup=keyb)
                await Aksiya.next()
            



            



@dp.message_handler(IsAdmin(),text = "❌Yo'q",state=Aksiya.button)
async def aksiya_cc(message:types.Message,state:FSMContext):

    async with state.proxy() as data:
        if 'photo' in data.keys():
            photo = data['photo']
            text = data['text']
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🚫 Bekor qilish','✅ Tasdiqlash')
            await message.answer_photo(photo=photo,caption=text,reply_markup=markup)
            await Aksiya.confirm.set()
        else:
            text = data['text']
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('🚫 Bekor qilish','✅ Tasdiqlash')
            await message.answer(text,reply_markup=markup)
            await message.answer('Hammasini tasdiqlaysizmi?')
            await Aksiya.confirm.set()

    
@dp.message_handler(IsAdmin(),text = '🚫 Bekor qilish',state=Aksiya.confirm)
async def aksiya_c(message:types.Message,state:FSMContext):

    await message.answer("Bekor qilindi 🚫",reply_markup=menu_aks)
    await state.finish()



@dp.message_handler(IsAdmin(),text = '✅ Tasdiqlash',state=Aksiya.confirm)
async def aksiya_c(message:types.Message,state:FSMContext):
    await message.answer('Muvaffaqiyli yuborildi ✅',reply_markup=menu_aks)
    users = db.select_all_users()
    async with state.proxy() as data:
        if 'photo' in data.keys():
            photo = data['photo']
            text = data['text']
            if 'name' in data.keys():
                name = data['name']
                url = data['url']
                markup = aksiya_markup(name=name,url=url)
                cnt = 0
                for user in users:
                    user_id = user[1]
                    try:
                        await bot.send_photo(chat_id=user_id,photo=photo,caption=text,reply_markup=markup)
                        await asyncio.sleep(0.07)
                        await state.finish()
                        cnt += 1
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
                    except aiogram.utils.exceptions.UserDeactivated:
                        pass
                    except aiogram.utils.exceptions.BadRequest:
                        pass
                await message.answer(f"Muvaffaqiyli yuborildi ✅\n\n{cnt} ta foydalanuvchiga yuborildi")
            else:
                cnt = 0
                for user in users:
                    user_id = user[1]
                    try:
                        await bot.send_photo(chat_id=user_id,photo=photo,caption=text)
                        await asyncio.sleep(0.07)
                        await state.finish()
                        cnt += 1
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
                    except aiogram.utils.exceptions.UserDeactivated:
                        pass
                    except aiogram.utils.exceptions.BadRequest:
                        pass
                await message.answer(f"Muvaffaqiyli yuborildi ✅\n\n{cnt} ta foydalanuvchiga yuborildi")
        else:
            text = data['text']     
            if 'name' in data.keys():
                name = data['name']
                url = data['url']
                markup = aksiya_markup(name=name,url=url)
                cnt = 0
                for user in users:
                    user_id = user[1]
                    try:
                        await bot.send_message(chat_id=user_id,text=text,reply_markup=markup)
                        await asyncio.sleep(0.05)
                        await state.finish()
                        cnt += 1
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
                    except aiogram.utils.exceptions.UserDeactivated:
                        pass
                    except aiogram.utils.exceptions.BadRequest:
                        pass
                await message.answer(f"Muvaffaqiyli yuborildi ✅\n\n{cnt} ta foydalanuvchiga yuborildi")

            else:
                cnt = 0
                text = data['text']    
                # users = db.select_all_users()
                for user in users:
                    user_id = user[1]

                    try:

                        await bot.send_message(chat_id=user_id,text=text)
                        await asyncio.sleep(0.07)
                        await state.finish()
                        cnt +=1
                        
                    except aiogram.utils.exceptions.BotBlocked:
                        pass
                    except aiogram.utils.exceptions.UserDeactivated:
                        pass
                    except aiogram.utils.exceptions.BadRequest:
                        pass
                await message.answer(f"Muvaffaqiyli yuborildi ✅\n\n{cnt} ta foydalanuvchiga yuborildi")