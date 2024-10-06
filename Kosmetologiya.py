from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from asyncio import run

# Botni va dispatcher'ni ishga tushirish
bot_token = "7844581324:AAHPqPjBbSKnpsxwojkGdHVuZGB_ZpNPdk4"  # Sizning bot tokeningiz
bot = Bot(token=bot_token)
dp = Dispatcher()

# Sizning Telegram ID'ingiz
admin_id = 6092871999

# Bot uchun ma'lumotlar
cosmetologists = ["Palonvchiyeva Palonchi", "Dildora Rixsibayeva"]
hair_types = {
    "Tuzatish": "30 daqiqa",
    "Qaytish": "45 daqiqa",
    "Dizayn": "60 daqiqa"
}
dates = ["1-Oktyabr", "2-Oktyabr", "3-Oktyabr"]

# Tanlangan kosmetolog, soch turi va sana
selected_cosmetologist = None
selected_hair_type = None
selected_date = None

# Botning vaqtinchalik ishlamayotganligi holati
bot_status_active = True  # Boshlanishida bot faol

# 1-Qadam: Start Buyrug'i
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("KOSMETOLOGIYA\nBotimizga xush kelibsiz!\nIltimos, kosmetologni tanlash uchun /select_cosmetologist ni bosing.")

# 2-Qadam: Kosmetologni Tanlash
@dp.message(Command("select_cosmetologist"))
async def select_cosmetologist(message: types.Message):
    if not bot_status_active:
        await message.answer("Bot vaqtinchalik ishlamayapti.")
        return
    
    keyboard_buttons = [f"/{cosmetologist.replace(' ', '_').lower()}" for cosmetologist in cosmetologists]
    await message.answer("Iltimos, kosmetologni tanlang:\n" + "\n".join(keyboard_buttons))

# Kosmetolog tanlanganda
@dp.message(lambda message: message.text in [f"/{c.replace(' ', '_').lower()}" for c in cosmetologists])
async def cosmetologist_selected(message: types.Message):
    global selected_cosmetologist
    selected_cosmetologist = message.text.replace("/", "").replace("_", " ").title()
    
    # Kosmetolog va soch turini bir vaqtda ko'rsatish
    hair_options = "\n".join([f"{hair_type} - {duration}" for hair_type, duration in hair_types.items()])
    await message.answer(f"{selected_cosmetologist} tanlandi. Iltimos, soch turini tanlang:\n{hair_options}\nSoch turini tanlash uchun /select_hair_type ni bosing.")

# 3-Qadam: Soch Turini Tanlash
@dp.message(Command("select_hair_type"))
async def select_hair_type(message: types.Message):
    if not bot_status_active:
        await message.answer("Bot vaqtinchalik ishlamayapti.")
        return

    keyboard_buttons = [f"/{hair_type.replace(' ', '_').lower()}" for hair_type in hair_types]
    await message.answer("Iltimos, soch turini tanlang:\n" + "\n".join(keyboard_buttons))

# Soch turi tanlanganda
@dp.message(lambda message: message.text.lower() in [f"/{h.replace(' ', '_').lower()}" for h in hair_types])
async def hair_type_selected(message: types.Message):
    global selected_hair_type
    selected_hair_type = message.text.replace("/", "").replace("_", " ").title()
    await message.answer(f"{selected_hair_type} tanlandi. Sanani tanlash uchun /select_date ni bosing.")

# 4-Qadam: Sanani Tanlash
@dp.message(Command("select_date"))
async def select_date(message: types.Message):
    if not bot_status_active:
        await message.answer("Bot vaqtinchalik ishlamayapti.")
        return

    keyboard_buttons = [f"/{date.replace('-', '_').lower()}" for date in dates]
    await message.answer("Iltimos, sanani tanlang:\n" + "\n".join(keyboard_buttons))

# Sana tanlanganda
@dp.message(lambda message: message.text.lower() in [f"/{d.replace('-', '_').lower()}" for d in dates])
async def date_selected(message: types.Message):
    global selected_date
    selected_date = message.text.replace("/", "").replace("_", "-").title()
    await message.answer(f"{selected_date} tanlandi.Tasdiqlash uchun 'Ha' yoki 'Yo'q' ni yozing.")

# 5-Qadam: Uchrashuvni Tasdiqlash
@dp.message(lambda message: message.text.lower() in ["ha", "yo'q"])
async def appointment_confirmation(message: types.Message):
    global selected_cosmetologist, selected_hair_type, selected_date
    
    if message.text.lower() == "ha":
        await message.answer(
            "Tabriklaymiz! Sizning uchrashuvingiz tasdiqlandi.\n"
            f"Tanlangan kosmetolog: {selected_cosmetologist}\n"
            f"Tanlangan soch turi: {selected_hair_type}\n"
            f"Tanlangan sana: {selected_date}\n"
            "Uchrashuvni bekor qilish uchun 'Bekor qilish' deb yozing."
        )
    elif message.text.lower() in ["yo'q", "yoq", "yok", "yokida", "yoqbo"]:
        await message.answer("Uchrashuv bekor qilindi. Iltimos, boshqa tanlov qiling.Tanlov qilish uchun /select_cosmetologist")
        selected_cosmetologist, selected_hair_type, selected_date = None, None, None  # Barcha tanlovlar bekor qilinadi
    else:
        await message.answer("Iltimos, 'Ha' yoki 'Yo'q' deb yozing.")

# Bekor qilish amali
@dp.message(lambda message: message.text.lower() == "bekor qilish")
async def cancel_appointment(message: types.Message):
    global selected_cosmetologist, selected_hair_type, selected_date
    selected_cosmetologist, selected_hair_type, selected_date = None, None, None  # Barcha tanlovlar bekor qilinadi
    await message.answer("Uchrashuv bekor qilindi. Iltimos, boshidan boshlang.")

# Bot vaqtinchalik ishlamayotganda - Faqat admin uchun
@dp.message(Command("status"))
async def bot_status(message: types.Message):
    if message.from_user.id == admin_id:
        global bot_status_active
        bot_status_active = not bot_status_active
        status_text = "Bot hozir ishlamoqda." if bot_status_active else "Bot hozir vaqtinchalik ishlamayapti."
        await message.answer(status_text)
    else:
        await message.answer("Siz bu amalni bajara olmaysiz.")

# Tanilmagan xabarlar uchun Echo funksiyasi
@dp.message()
async def echo(message: types.Message):
    await message.answer("Noto'g'ri buyruq. Iltimos, kerakli variantni tanlang.")

# Bot ishga tushganda xabar yuborish
async def startup_answer(bot: Bot):
    await bot.send_message(admin_id, text="Bot ishlamoqda /start")  # Bot ishga tushgani haqida ma'lumot yuboriladi

# Bot to'xtaganda xabar yuborish
async def shutdown_answer(bot: Bot):
    await bot.send_message(admin_id, text="Bot stop")  # Bot to'xtagani haqida ma'lumot yuboriladi

# Botni ishga tushirish
async def start():
    # Boshlanish va tugash xabarlarini ro'yxatdan o'tkazish
    dp.startup.register(startup_answer)
    dp.message.register(echo)
    dp.shutdown.register(shutdown_answer)

    # Polling orqali botni ishga tushirish
    await dp.start_polling(bot)

# Botni ishga tushirish
run(start())
