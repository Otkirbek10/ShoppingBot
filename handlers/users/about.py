from aiogram.types import Message
from loader import dp


about = 'âšī¸ Biz haqimizda'

@dp.message_handler(text=about)
async def about_our(message:Message):
    await message.answer("<b>Damir Market</b>ning  yetkazib berish xizmatlaridan endi onlayn bot orqali foydalanishingiz mumkin\n\nProgrammist đ¨đģâđģ: <a href='https://t.me/alimov_06'>O'tkirbek Alimov</a>")