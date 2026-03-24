import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image
import asyncio

TOKEN = "8658089098:AAFXd7PwODPgy5fHVNSzaPsvQWyLGIKxwmo"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أرسل صورة لتحويلها PDF")

async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
        await file.download_to_drive("img.jpg")

        img = Image.open("img.jpg")
        img.save("file.pdf", "PDF")

        await update.message.reply_document(open("file.pdf", "rb"))

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, convert))

    PORT = int(os.environ.get("PORT", 10000))
    URL = os.environ.get("RENDER_EXTERNAL_URL")

    # ضبط webhook
    await app.bot.set_webhook(f"{URL}/webhook")

    # تشغيل السيرفر
    await app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path="webhook"
    )

if __name__ == "__main__":
    asyncio.run(main())
