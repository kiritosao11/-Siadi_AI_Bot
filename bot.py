import openai
import telegram
import logging
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# توكن تلغرام (⚠️ استبدله بتوكن البوت الخاص بك)
TELEGRAM_TOKEN = "ضع_هنا_توكن_بوت_تلغرام"

# مفتاح OpenAI (⚠️ استبدله بـ API Key من https://platform.openai.com/)
OPENAI_API_KEY = "ضع_هنا_API_Key_الخاصة_بـ_OpenAI"

# إعداد واجهة OpenAI
openai.api_key = OPENAI_API_KEY

# إعداد السجلات
logging.basicConfig(level=logging.INFO)

# دالة التفاعل مع ChatGPT
async def generate_response(user_message: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # يمكنك استخدام "gpt-4" إذا كان متاحًا لك
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي وودود. أجب بشكل واضح ومفيد."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"حدث خطأ أثناء محاولة الرد: {e}"

# التعامل مع الرسائل النصية
async def handle_message(update: telegram.Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await generate_response(user_text)
    await update.message.reply_text(reply)

# تشغيل البوت
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("🤖 البوت يعمل الآن...")
    await app.run_polling()

# نقطة البدء
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
