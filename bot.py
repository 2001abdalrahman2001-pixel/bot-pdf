from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
import os

TOKEN = "8629476476:AAFZhdoIs4_ak__SM5cFr02mlzKPsovZA48"

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photos = update.message.photo
    
    if not photos:
        return

    # أخذ أعلى جودة للصورة
    photo = photos[-1]
    file = await photo.get_file()

    file_path = "image.jpg"
    await file.download_to_drive(file_path)

    # تحويل الصورة إلى PDF
    image = Image.open(file_path)
    pdf_path = "output.pdf"
    image.convert("RGB").save(pdf_path)

    # إرسال PDF للمستخدم
    await update.message.reply_document(document=open(pdf_path, "rb"))

    # حذف الملفات المؤقتة
    os.remove(file_path)
    os.remove(pdf_path)

# ✅ إنشاء التطبيق مباشرة (بدون دالة main)
application = Application.builder().token(TOKEN).build()
application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

# ✅ هذا السطر مهم جداً - يعرض التطبيق لـ Render/Anywhere بدون polling
app = application
