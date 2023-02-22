from loader import dp,db,bot
from aiogram import types
from handlers.users.menu import settings
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
from keyboards.default.button import *
from filters import IsAdmin
from data.config import ADMINS
from aiogram.types.chat import ChatActions
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton,Message,CallbackQuery,ReplyKeyboardMarkup,ReplyKeyboardRemove,ContentType
from states.state import CategoryState,ProductState
from hashlib import md5

category_cb = CallbackData('category', 'id', 'action')
product_cb = CallbackData('product', 'id', 'action')

add_category = "➕ Kategoriya qo'shish"

add_product = "➕ Mahsulot qo'shish"
delete_category = "🗑️ Kategoriyani o'chirish"

category = db.select_all_categories()

@dp.message_handler(IsAdmin(),text=settings)
async def process_settings(message:Message):
    markup = InlineKeyboardMarkup()
    global category
    for id,name in db.select_all_categories():
        markup.add(InlineKeyboardButton(name,callback_data=category_cb.new(id=id,action = 'watch')))

    markup.add(InlineKeyboardButton(add_category,callback_data='add_category'))
    await message.answer('Kategoriya sozlamalari:',reply_markup=markup)



@dp.callback_query_handler(IsAdmin(),category_cb.filter(action='watch'))
async def category_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):
    category_id = callback_data['id']

    products = db.select_product(category_id=category_id)
    
    await query.message.delete()
    await state.update_data(category_index=category_id)
    await view_products(query.message, products, category_id)


@dp.callback_query_handler(IsAdmin(),text='add_category',state='*')
async def add_cat(call:types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('Kategoriya nomi?')
    await CategoryState.name.set()

@dp.message_handler(IsAdmin(),state=CategoryState.name)
async def cat_name(message:Message, state: FSMContext):
    category_name = message.text
    db.add_category(name=category_name)
    markup = InlineKeyboardMarkup()
    ccc = db.select_all_categories()
    for id,name in ccc:
        markup.add(InlineKeyboardButton(name,callback_data=category_cb.new(id=id,action = 'watch')))

    markup.add(InlineKeyboardButton(add_category,callback_data='add_category'))

    await state.finish()
    await process_settings(message)


@dp.message_handler(IsAdmin(),text=delete_category)
async def delete_categorys(message: types.Message,state:FSMContext):
    async with state.proxy() as data:
        if 'category_index' in data.keys():
            id = data['category_index']
            db.delete_product_for_category(category_id=id)
            db.delete_category(id=id)
            await message.answer("Kategoriya o'chirildi!!",reply_markup=ReplyKeyboardRemove())
            await process_settings(message)



@dp.message_handler(IsAdmin(),text=add_product)
async def add_product_handler(message:Message):
    await ProductState.name.set()

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(cancel)
    await message.answer('Mahsulot nomini kiriting?',reply_markup=markup)


@dp.message_handler(IsAdmin(),text=cancel,state=ProductState.name)
async def name_cancel(message:Message,state:FSMContext):
    await message.answer('Bekor qilindi!',reply_markup=ReplyKeyboardRemove())
    await state.finish()

    await process_settings(message)

@dp.message_handler(IsAdmin(),text=back, state=ProductState.name)
async def process_title_back(message: Message, state: FSMContext):
    await add_product_handler(message)

@dp.message_handler(IsAdmin(),state=ProductState.name)
async def product_name(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['name'] = message.text

    await ProductState.next()
    await message.answer("Mahsulotning tavsifi?",reply_markup=back_markup)


@dp.message_handler(IsAdmin(),text=back,state=ProductState.description)
async def description_back(message:Message,state:FSMContext):
    await ProductState.name.set()

    async with state.proxy() as data:
        await message.answer(f"<i>{data['name']}</i> nomini o'zgartirmoqchimisiz?",reply_markup=back_markup)


@dp.message_handler(IsAdmin(),state=ProductState.description)
async def product_description(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['description'] = message.text

    await ProductState.next()
    await message.answer("Mahsulot rasmi?",reply_markup=back_markup)

@dp.message_handler(IsAdmin(),content_types=ContentType.TEXT,state=ProductState.photo)
async def text_photo(message:Message,state:FSMContext):
    if message.text == back:
        await ProductState.description.set()
        async with state.proxy() as data:
            await message.answer(f"<i>{data['description']}</i> ni o'zgartirmoqchimisiz?",reply_markup=back_markup)
    else:
        await message.answer("Iltimos mahsulot rasmini yuboring!!")

@dp.message_handler(IsAdmin(),content_types=ContentType.PHOTO,state=ProductState.photo)
async def get_product_photo(message:Message,state:FSMContext):
    file_id = message.photo[-1].file_id
    # file_info = await bot.get_file(file_id)
    # downloaded_photo = (await bot.download_file(file_info.file_path)).read()

    async with state.proxy() as data:
        data['photo'] = file_id

    await message.answer('Mahsulotnig narxi?',reply_markup=back_markup)
    await ProductState.next()


@dp.message_handler(IsAdmin(),lambda message: not message.text.isdigit(), state=ProductState.price)
async def check_price(message:Message,state:FSMContext):
    if message.text == back:
        await ProductState.photo.set()
        async with state.proxy() as data:
            await message.answer("Mahsulot rasmini o'zgartirmoqchmisiz?",reply_markup=back_markup)

    else:
        await message.answer('Iltimos mahsulot narxini son bilan kiriting!')

@dp.message_handler(IsAdmin(),lambda message: message.text.isdigit(), state=ProductState.price)
async def get_price(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['price'] = message.text

        
        name = data['name']
        description = data['description']
        photo = data['photo']
        price = data['price']

        await ProductState.next()
        msg = f"<i>{name}</i>\n\n{description}\n\nNarxi: {price} so'm."

        await message.answer_photo(photo=photo,
                                   caption=msg,
                                   reply_markup=conf_markup())

                                

@dp.message_handler(IsAdmin(),lambda message: message.text not in [back,admin_confirm],state=ProductState.confirm)
async def other_message(message:Message,state:FSMContext):
    await message.answer("Iltimos quyidagilardan birini tanlang!👇")


@dp.message_handler(IsAdmin(),text=back,state=ProductState.confirm)
async def back_price(message:Message,state:FSMContext):
    await ProductState.price.set()

    async with state.proxy() as data:
        msg = f"<i>{data['price']}</i> ni o'zgartirmoqchimisiz?"

    await message.answer(msg,reply_markup=back_markup)

@dp.message_handler(IsAdmin(),text=admin_confirm,state=ProductState.confirm)
async def conf_product(message:Message,state:FSMContext):

    async with state.proxy() as data:
        name = data['name']
        description = data['description']
        photo = data['photo']
        price = data['price']
        id = data['category_index']

    prod = db.add_product(name=name,description=description,photo=photo,price=price,category_id=id)
    await message.answer("Mahsulot qo'shildi!!",reply_markup=ReplyKeyboardRemove())
    await state.finish()
    await process_settings(message)



@dp.callback_query_handler(IsAdmin(),product_cb.filter(action='delete'))
async def delete_product_callback_handler(query: CallbackQuery, callback_data: dict):

    product_id = callback_data['id']
    aa = db.delete_product(id=product_id)
    await query.answer("Mahsulot o'chirildi!!")
    await query.message.delete()



async def view_products(msg, products, category_id):

    await bot.send_chat_action(msg.chat.id, ChatActions.TYPING)

    for id, name, photo, description, price,cc  in products:

        temp = f"<b>{name}</b>\n\n{description}\n\nNarxi: {price} so'm."

        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("🗑️ O'chirish ", callback_data=product_cb.new(id=id, action='delete')))

        await msg.answer_photo(photo=photo,
                             caption=temp,
                             reply_markup=markup)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(add_product)
    markup.add(delete_category)

    await msg.answer("Nimadir qo'shishni yoki o'chirishni xohlaysizmi?", reply_markup=markup)

