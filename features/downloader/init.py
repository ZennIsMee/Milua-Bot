import os
import asyncio
from telegram import Update

DOWNLOAD_DIR = "downloads"

# pastikan folder downloads ada
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Helper: kirim file ke user & hapus setelah dikirim
async def send_file(update: Update, file_path):
    if os.path.exists(file_path):
        await update.message.reply_document(open(file_path, "rb"))
        os.remove(file_path)
        
