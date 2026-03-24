import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from PIL import Image
import asyncio
import os

# ضع هنا التوكن مباشرة
TOKEN = "8730040425:AAFp8loKv8dQq8UWsSYPAqht8OuGjvzWm0Q"

# إعدادات اللوج
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# دالة start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبا! أرسل أي صورة لتحويلها إلى PDF.")

# دالة تحويل الصور إلى PDF
async def convert_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_file = await update.message.photo[-1].get_file()
        await photo_file.download_to_drive("temp.jpg")
        image = Image.open("temp.jpg")
        image.save("result.pdf", "PDF")
        await update.message.reply_document(document=open("result.pdf", "rb"))
    else:
        await update.message.reply_text("أرسل صورة فقط.")

# الوظيفة الرئيسية لتشغيل البوت
async def main():
    PORT = int(os.environ.get("PORT", 8443))  # Render يعطي البورت تلقائيًا

    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, convert_image))

    # تشغيل Webhook فقط
    url = os.environ.get("RENDER_EXTERNAL_URL")  # URL الافتراضي للبوت على Render
    webhook_url = f"{url}/webhook"
    await application.bot.set_webhook(webhook_url)
    logger.info(f"Webhook set to {webhook_url}")

    await application.updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook"
    )
    logger.info(f"Bot is running on port {PORT}")
    await application.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
