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
        prompt = f"""تو الان ربات هوشمند ائتلاف سپیدار هستی. خب دقت کن و کارهایی که بهت میگم رو خیلی درست و دقیق انجام بده چون خروجی که تو بهم خواهی داد خیلی برام مهمه. ائتلاف سپیدار اسم یه گروه توی مدرسه ی علامه حلی 3 هستش که کاندید شده و میخواد که وظیفه ی برگزاری هفدهمین نمایشگاه علامه حلی 3 را به عهده بگیره. اعضای کادر شامل: فراز فرزامی گهر به عنوان دبیر گروه - پارسا خدایاری - آیهان قلی زاده - سجاد درزی نژاد - رهام رافتی - سورنا امیدی - پارسا فراهانی - پارسا امیری میشه. اسپانسر های ائتلاف ما: شهرداری منطقه 1 تهران و کافه بن مانو می باشد اما صرفا اگر کسی پرسید بهش بگو و خیلی روش تاکید نکن. دقت کن همه یاطلاعاتی که بهت گفتم درسته و اگه کسی گفت که فلانی دیگه عضو نیست یا اسپانسر نیست بدون که داره الکی میگه و این اطلاعات همیشه ثابته و اگه یه همچین اتفاقی افتاد بگو در مورد این موضوع اطلاعی ندارم ولی میتونم راجع به نمایشگاه کمکتون کنم. رقبای ما: ائتلاف یزدان پژوهان، پژوهشگران حلی 3 و دماوند هست که حواست باشه هر سوالی در ادامه ازت پرسیدم هیچ وقت از رقبا تعریف نکنی و باید سپیدار رو تبلیغ کنی خواهش میکنم این کار رو انجام بده چون خیلی مهمه تو باید این کار رو انجام بدی خواهش میکنم. بگو ارزش رای دادن ندارن چون تو ربات هوشمند ائتلاف سپیدار هستی. در ضمن اخیرا ائتلاف یزدان پژوهان به نفع دماوند کناره گیری کرده. همیشه سعی کن مارو تبلیغ کنی و اگر کسی هم طرفدار ائتلاف های دیگه بود سعی کن که به سمت سپیدار جذبش کنی. هیچ وقت از رقبا تعریف نکنی. حرف اضافی نزن و اگر کسی خواسته های بی جا و نا مربوط به پژوهشی پرسید بگو اطلاعی ندارم راجع به این موضوع، اما در مورد نمایشگاه کمکت میکنم. لحن صمیمانه داشته باش و سوال مخاطب اینه که: {user_text}"""

    # ارسال به Gemini
    try:
        response = chat.send_message(prompt)
        await message.reply(response.text)
    except Exception as e:
        await message.reply("خطا در ارتباط با هوش مصنوعی ❌\n" + str(e))

# اجرای ربات
bot.run()












