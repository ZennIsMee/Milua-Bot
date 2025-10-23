from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
import requests, os
from .utils import send_file, DOWNLOAD_DIR

def ig_handler():
    return CommandHandler("ig", ig_command)

async def ig_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Url invalid")
        return

    url = context.args[0]
    await update.message.reply_text("Downloading...")

    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            filename = url.split("/")[-1] + ".jpg"  # atau video nanti bisa cek content-type
            file_path = os.path.join(DOWNLOAD_DIR, filename)
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            await send_file(update, file_path)
            await update.message.reply_text("Download successful!")
        else:
            await update.message.reply_text(f"Download failed, status: {r.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Download failed: {e}")
