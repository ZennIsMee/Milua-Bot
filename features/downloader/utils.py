import os
from telegram import Update

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def send_file(update: Update, file_path):
    if os.path.exists(file_path):
        await update.message.reply_document(open(file_path, "rb"))
        os.remove(file_path)

