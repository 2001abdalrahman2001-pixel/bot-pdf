from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
import os
import asyncio

TOKEN = "8730040425:AAFp8loKv8dQq8UWsSYPAqht8OuGjvzWm0Q"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = update.message.photo
    
    if not photos:
        return

    photo = photos[-1]
    file = await photo.get_file()

    file_path = "image.jpg"
    await file.download_to_drive(file_path)

    image = Image.open(file_path)
    pdf_path = "output.pdf"
    image.convert("RGB").save(pdf_path)

    await update.message.reply_document(document=open(pdf_path, "rb"))

    os.remove(file_path)
    os.remove(pdf_path)

# إنشاء التطبيق
application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# بدء التطبيق باستخدام webhook
async def start_webhook():
    await application.initialize()
    await application.start()
    await application.updater.start_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'localhost')}/{TOKEN}"
    )
    return application

# تشغيل البوت
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(start_webhook())

# ✅ WSGI app لـ Gunicorn
def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [b'Bot is running']
