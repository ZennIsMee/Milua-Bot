from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from pytube import YouTube
import os, asyncio
from .utils import send_file, DOWNLOAD_DIR

def ytmp_handler():
    return CommandHandler("ytmp", ytmp_command)

async def ytmp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Kirim link YouTube setelah /ytmp")
        return

    url = context.args[0]
    await update.message.reply_text("Sedang download YouTube...")

    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = os.path.join(DOWNLOAD_DIR, f"{yt.title}.mp4")
        stream.download(output_path=DOWNLOAD_DIR, filename=f"{yt.title}.mp4")
        await send_file(update, file_path)
        await update.message.reply_text("Selesai! (Replied by YTMP)")
    except Exception as e:
        await update.message.reply_text(f"Gagal download: {e}")
