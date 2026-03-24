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

# ✅ إنشاء كائن WSGI لـ Gunicorn
# هذا الكائن يقوم بتشغيل البوت عند استدعائه
class BotWSGI:
    def __init__(self):
        self.app = application
        
    def __call__(self, environ, start_response):
        # تشغيل البوت في الخلفية إذا لم يكن يعمل
        if not hasattr(self, '_running'):
            self._running = True
            # بدء polling أو webhook حسب الإعداد
            asyncio.create_task(self.app.initialize())
            asyncio.create_task(self.app.start())
        
        # إرجاع استجابة بسيطة للـ health check
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Bot is running']

# الكائن المطلوب من Gunicorn
app = BotWSGI()
