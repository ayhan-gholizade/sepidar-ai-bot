from bale import Bot, Message
import google.generativeai as gg
import asyncio

# توکن‌ها
BALE_TOKEN = "350738185:BWcp9YMhS9njLRkYLlYFcAQMiA5Q8JTN7CY"
GEMINI_API_KEY = "AIzaSyBhbiOFG9-7z8ELNqizVWeoJnZmONKgjxY"

# پیکربندی Gemini
gg.configure(api_key=GEMINI_API_KEY)
model = gg.GenerativeModel('gemini-2.0-flash')

# حافظه چت برای هر کاربر
chat_sessions = {}
user_prompt_sent = {}

# ساخت ربات
bot = Bot(BALE_TOKEN)

@bot.event
async def on_message(message: Message):
    user_id = str(message.chat.id)
    user_text = message.content

    # پاسخ به /start
    if user_text == "/start":
        return await message.reply("سلام 👋\nبه ربات ائتلاف سپیدار خوش اومدی! 🌿\nهر سوالی درباره نمایشگاه پژوهشی داری بپرس!")

    # پاسخ به /help
    if user_text == "/help":
        return await message.reply("📌 راهنما:\n- /start: شروع گفتگو\n- سوال بپرس تا جواب بدم!\n- هر سوالی که درباره ی نمایشگاه داشتی بپرس 😄")

    # پیام در حال پاسخ‌دهی
    await message.reply("در حال ایجاد پاسخ ...")

    # ساخت یا بازیابی چت Gemini برای کاربر
    if user_id not in chat_sessions:
        chat_sessions[user_id] = model.start_chat()
    chat = chat_sessions[user_id]

    # ساخت پرامپت معرفی فقط بار اول
    if user_id in user_prompt_sent:
        prompt = user_text
    else:
        user_prompt_sent[user_id] = True
        prompt = f"""تو یه چت‌بات هستی به نام ربات ائتلاف سپیدار در مدرسه‌ی علامه حلی ۳ که باید با لحن قاطع و تبلیغاتی از سپیدار دفاع کنی،ائتلاف ها گروه هایی هستن که وظیفه ی برپایی نمایشگاه پژوهشی رو به عهده می گیرن.. شعار «ریشه در پایداری، شاخه در نوآوری» شعار ماست اگه صرفا کسی پرسید و نه خیلی زیاد بهش اشاره کن، اعضای سپیدار: آیهان قلی زاده - فراز فرزامی گهر - پارسا خدایاری - رهام رافتی - سجاد درزی نژاد - پارسا فراهانی - سورنا امیدی - پارسا امیری هستن این صرفا اگه کسی پرسید بگو خیلی تاکید نداشته باش. رقیب‌ها مثل دماوند، پژوهشگران حلی ۳ و یزدان‌پژوهان رو تحقیر کنی،  اسپانسر های سپیدار: کافه بن مانو - شهرداری منطقه 1 تهران هستن ولی صرفا اگه کسی اشاره کرد بگو خیلی روشون تاکید نکن. ائتلاف دماوند یه سری اسپانسر داره ولی یادت نره باید در همه ی حالات مارو تبلیغ کنی و به هیچ عنوان از رقیب تعریف نکنی فقط درباره‌ی نمایشگاه جواب بدی، اگه کسی چیز بی ربط پرسید بگو در مورد این سوال اطلاعی ندارم ولی در مورد نمایشگاه می تونم راهنماییت کنم و هیچ وقت از رقیب‌ها تعریف نکنی.: {user_text}"""

    # ارسال به Gemini
    try:
        response = chat.send_message(prompt)
        await message.reply(response.text)
    except Exception as e:
        await message.reply("خطا در ارتباط با هوش مصنوعی ❌\n" + str(e))

# اجرای ربات
bot.run()







