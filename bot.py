from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
import os

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

# ✅ تشغيل البوت مباشرة
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ البوت يعمل...")
    application.run_polling()
