from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from PIL import Image
import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

TOKEN = "8658089098:AAFXd7PwODPgy5fHVNSzaPsvQWyLGIKxwmo"

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

# تشغيل البوت
def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Bot is running...")
    application.run_polling()

# خادم HTTP بسيط لـ health check
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_http():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    print(f"✅ HTTP server running on port {port}")
    server.serve_forever()

# تشغيل كل شيء معاً
if __name__ == "__main__":
    # تشغيل HTTP server في thread منفصل
    http_thread = threading.Thread(target=run_http, daemon=True)
    http_thread.start()
    
    # تشغيل البوت في thread الرئيسي
    run_bot()
