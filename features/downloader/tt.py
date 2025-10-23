from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
import yt_dlp, os
from .utils import send_file, DOWNLOAD_DIR

def tiktok_handler():
    return CommandHandler("tiktok", tiktok_command)

async def tiktok_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Url invalid")
        return

    url = context.args[0]
    await update.message.reply_text("Downloading...")

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
            'format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = os.path.join(DOWNLOAD_DIR, f"{info['title']}.mp4")
        await send_file(update, file_path)
        await update.message.reply_text("Download successful!")
    except Exception as e:
        await update.message.reply_text(f"Download failed: {e}")
