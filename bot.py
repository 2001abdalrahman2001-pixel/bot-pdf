import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters
from PIL import Image
import os

TOKEN = os.getenv("BOT_TOKEN")

user_images = {}
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📸 أرسل الصور وسأحولها إلى PDF\n\nعند الانتهاء اضغط /done")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    photo = update.message.photo[-1]
    file = await photo.get_file()
    os.makedirs(f"images/{user_id}", exist_ok=True)
    file_path = f"images/{user_id}/{len(os.listdir(f'images/{user_id}'))}.jpg"
    await file.download_to_drive(file_path)
    user_images.setdefault(user_id, []).append(file_path)
    await update.message.reply_text("✅ تم حفظ الصورة")

async def done(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_images or not user_images[user_id]:
        await update.message.reply_text("❌ لم ترسل أي صور")
        return
    images = []
    for path in user_images[user_id]:
        img = Image.open(path).convert("RGB")
        images.append(img)
    pdf_path = f"{user_id}.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    await update.message.reply_document(open(pdf_path, "rb"))
    for path in user_images[user_id]:
        os.remove(path)
    os.rmdir(f"images/{user_id}")
    os.remove(pdf_path)
    user_images[user_id] = []

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("done", done))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
