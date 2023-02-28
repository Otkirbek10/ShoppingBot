from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from loader import dp

@dp.message_handler(CommandHelp())
async def bot_help(message:types.Message):
        notes = "Botdan foydalanish uchun qo'llanma:\nBotda mahsulotlarni buyurtma qiling va uni rasmiylashtiring va tez orada buyurtmangizni qabul qilib oling\nSavol va takliflaringiz bo'lsa uni @Ahmadjon_Dokon5957 ga jo'nating "

        await message.answer("\n".join(notes))