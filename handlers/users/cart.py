from loader import dp,db,bot
from aiogram.types import ContentType,ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup,CallbackQuery,Message
from filters import IsUser,IsAdmin
from aiogram.utils.callback_data import CallbackData
# from .menu import cart
from keyboards.default.button import * 
from aiogram.dispatcher import FSMContext
from states.state import Checkout
from keyboards.inline.products import product_markup,product_cb

import sqlite3
con = sqlite3.connect("main/db.sqlite3")
cur = con.cursor()

cart = '🛒 Korzina'

@dp.message_handler(IsUser(),text=cart)
async def cartr(message:Message,state:FSMContext):
    id = message.from_user.id
    cart_data = db.select_cart(tg_id=id)

    if len(cart_data) == 0:
        await message.answer("Sizning korzinangiz bo'sh")

    else:
        async with state.proxy() as data:
            data['products'] = {}
            

        cost = 0

        for _, idx,count_in_cart,product_id in cart_data:

            product = db.select_for_cart(id=product_id)

            if product == None:

                db.delete_from_cart(product=product_id)

            else:
                _, name, photo, description, price, pid = product
                cost += price

                async with state.proxy() as data:
                    data['products'][product_id] = [name, price, count_in_cart]

                markup = product_markup(product_id, count_in_cart)
                text = f"<b>{name}</b>\n\n{description}\n\nNarxi: {price} so'm."

                await message.answer_photo(photo=photo,
                                           caption=text,
                                           reply_markup=markup)\
        
        if cost != 0:
            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('📦 Buyurtmani rasmiylashtirish')
            markup.add(back)
            await message.answer("Rasmiylashtirishga o'tmoqchimisiz?",
                                 reply_markup=markup)
        else:
            await message.answer("Korzinangiz bo'sh,keling uni birgalikda to'ldiramiz ",reply_markup=cart_bak)

@dp.callback_query_handler(IsUser(), product_cb.filter(action='count'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='increase'))
@dp.callback_query_handler(IsUser(), product_cb.filter(action='decrease'))
async def product_callback_handler(query: CallbackQuery, callback_data: dict, state: FSMContext):

    id = callback_data['id']
    id = int(id)
    tg_id = query.message.chat.id
    action = callback_data['action']

    if 'count' == action:
        async with state.proxy() as data:
            if 'products' not in data.keys():
                await cartr(query.message,state)
            else:
                await query.answer('Количество - ' + str(data['products'][id][2]))

    else:
        async with state.proxy() as data:

            if 'products' not in data.keys():

                await cartr(query.message, state)
            
            else:
                data['products'][id][2] += 1 if 'increase' == action else -1
                count_in_cart = data['products'][id][2]

                if count_in_cart == 0:
                    db.delete_from_cart_foruser(tg_id=tg_id,product=id)

                    await query.message.delete()

                else:
                    db.update_cart(quantity=count_in_cart,tg_id=tg_id,product=id)

                    await query.message.edit_reply_markup(product_markup(id, count_in_cart))





@dp.message_handler(IsUser(),text = '📦 Buyurtmani rasmiylashtirish')
async def process_checkout(message:Message,state:FSMContext):

    await Checkout.check_cart.set()
    await checkout(message, state)


@dp.message_handler(IsUser(),text=back)
async def back_cart(message:Message):
    await message.answer('Menyu',reply_markup=cart_bak)

async def checkout(message,state):
    total_price = 0
    msg = ''


    async with state.proxy() as data:
        for title, price, count_in_cart in data['products'].values():
            if count_in_cart == 0:
                pass
            else:
                tp = count_in_cart * price
                msg += f"<b>{title}</b> * {count_in_cart} dona. = {tp} so'm\n"
                total_price += tp

    await message.answer(f"{msg}\nBuyurtmaning umumiy narxi: {total_price} so'm.",
                         reply_markup=conf_markup())

@dp.message_handler(IsUser(),lambda message: message.text not in [admin_confirm,back],state=Checkout.check_cart)
async def not_in_list(message:Message,state:FSMContext):
    await message.answer("Iltimos quydagilardan birini tanlang")

@dp.message_handler(IsUser(),text=back,state=Checkout.check_cart)
async def back_check(message:Message,state:FSMContext):
    await state.finish()
    await cartr(message,state)

@dp.message_handler(IsUser(),text=admin_confirm,state=Checkout.check_cart)
async def check_admin(message:Message,state:FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True,selective=True)
    markup.add(message.from_user.full_name)
    markup.add(back)
    await Checkout.next()
    await message.answer('Ismingizni kiriting.',
                         reply_markup=markup)

@dp.message_handler(IsUser(),text=back,state=Checkout.name)
async def neim_back(message:Message,state:FSMContext):
    await Checkout.check_cart.set()
    await checkout(message, state)



@dp.message_handler(IsUser(),state=Checkout.name)
async def prosecc_name(message:Message,state:FSMContext):

    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer('Manzilingizni yozing.',reply_markup=back_markup)
    await Checkout.next()


@dp.message_handler(IsUser(),content_types=ContentType.TEXT,state=Checkout.addres)
async def back_loc(message:Message,state:FSMContext):

    if message.text == back:
        async with state.proxy() as data:
            imy = data['name']
            await message.answer(f"Ismingizni <i> {imy} </i> dan o'zgartirmoqchimisiz?",reply_markup=back_markup)
            await Checkout.name.set()
    else:
        # await message.answer('Lokatsiyangizni pastdagi tugma orqali yuboring!',reply_markup=back_loco)
        async with state.proxy() as data:
            data['addres'] = message.text
            await message.answer('Lokatsiyangizni pastdagi tugma orqali yuboring!',reply_markup=back_loco)
            await Checkout.next()

@dp.message_handler(IsUser(),text = back,state=Checkout.location)
async def again_address(message:Message,state:FSMContext):


    async with state.proxy() as data:
        old_address = data['addres']
        await message.answer(f"Manzilingizni <i>{old_address}</i> dan o'zgartirmoqchimisiz?")
        await Checkout.addres.set()


@dp.message_handler(IsUser(),content_types=ContentType.LOCATION,state=Checkout.location)
async def get_location(message:Message,state:FSMContext):
    lat = message.location.latitude
    long = message.location.longitude

    async with state.proxy() as data:
        data['location_latitude'] = lat
        data['location_longitude'] = long

    await message.answer('Telefon raqamingizni yuboring',reply_markup=contact_p)
    await Checkout.next()



@dp.message_handler(IsUser(),content_types=ContentType.CONTACT,state=Checkout.phone)
async def contact_procces(message:Message,state:FSMContext):

    phone = message.contact.phone_number
    first_name = message.contact.first_name

    async with state.proxy() as data:
        data['contact'] = phone
        data['first_name'] = first_name

    await confirm(message)

    await Checkout.next()

async def confirm(message):

    await message.answer("Hamma  narsa to'g'ri ekanligiga ishonch hosil qiling va buyurtmani tasdiqlang.",
                         reply_markup=confirm_markup())


@dp.message_handler(IsUser(),lambda message: message.text not in [share_contact],state=Checkout.phone)
async def contact_procces(message:Message):
    if message.text == back:
        pass
    else:
        await message.answer('Raqamingizni pastdagi tugma orqali yuboring!!')


@dp.message_handler(IsUser(), lambda message: message.text not in [confirm_message,back], state=Checkout.confirm)
async def process_confirm_invalid(message: Message):
    await message.reply('Quyidagilardan birini tanlang 👇!')

@dp.message_handler(IsUser(),text = back,state=Checkout.confirm)
async def procces_confirm_back(message:Message,state:FSMContext):

    await state.finish()
    await cartr(message,state)
    

@dp.message_handler(IsUser(),text=confirm_message,state=Checkout.confirm)
async def procces_confirm(message:Message,state:FSMContext):
    tg_id = message.from_user.id
    await message.answer('Buyurtmangiz tasdiqlandi! Tez orada uni qabul qilib oling 🚀',reply_markup=cart_bak)
    async with state.proxy() as data:
        name = data['name']
        addres = data['addres']
        location_lat = data['location_latitude']
        location_long = data['location_longitude']
        contact = data['contact']
        first_n = data['first_name']
        
    markup = InlineKeyboardMarkup()
    potverdjeniya = InlineKeyboardButton(text='✅ Tasdiqlash',callback_data='confirm')
    markup.insert(potverdjeniya)


    answer = ''
    total_price = 0
    total_name = ''

    async with state.proxy() as data:

        for title, price, count_in_cart in data['products'].values():

            tp = count_in_cart * price
            answer += f"<b>{title}</b> * {count_in_cart} dona. = {tp} so'm\n"
            total_price += tp
            total_name +=title + ','
            
        db.add_to_order(tg_id=tg_id,name=first_n,phone=contact,product=total_name)

        await bot.send_contact(5012333108,contact,first_name=first_n)
        await bot.send_location(5012333108,latitude=location_lat,longitude=location_long)
        await bot.send_message(5012333108,f"<b>{name}</b> ning buyurtmalari:\n\n{answer}\nManzil: {addres}\n\nBuyurtmaning umumiy narxi: {total_price} so'm",reply_markup=markup)


        db.delete_confirm_cart(tg_id=tg_id)
        await state.finish()


@dp.callback_query_handler(text = 'confirm')
async def adding_order(query: CallbackQuery):
    await query.answer('Buyurtmani tasdiqladingiz!')
    await query.message.delete_reply_markup()








