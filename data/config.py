from environs import Env

#Environs kutubxonasidan foydalanish

env = Env()
env.read_env()

#.env fayli ichidan quyidagi ma'lumotlarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = [5012333108,1347430214]  # Adminlar ro'yxati
 