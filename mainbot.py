from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# ------------------------
# Inline menu
# ------------------------
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("YouTube", callback_data="ytmp")],
        [InlineKeyboardButton("TikTok", callback_data="tiktok")],
        [InlineKeyboardButton("Instagram", callback_data="ig")],
        [InlineKeyboardButton("AI Chat", callback_data="ai")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select menu:", reply_markup=reply_markup)

def menu_handler():
    return CommandHandler(["start", "menu"], menu)

# ------------------------
# Callback handler untuk tombol
# ------------------------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "ytmp":
        await query.edit_message_text("Type /ytmp <link> to download YouTube")
    elif data == "tiktok":
        await query.edit_message_text("Type /tiktok <link> to download TikTok")
    elif data == "ig":
        await query.edit_message_text("Type /ig <link> to download Instagram")
    elif data == "ai":
        await query.edit_message_text("Type /ai <pesan> untuk chat AI (sementara dummy)")

# ------------------------
# Dummy AI handler
# ------------------------
async def dummy_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("AI still on update.")

def ai_handler():
    return CommandHandler("ai", dummy_ai)

# ------------------------
# Downloader imports
# ------------------------
from features.downloader.yt import ytmp_handler
from features.downloader.tt import tiktok_handler
from features.downloader.ig import ig_handler

# ------------------------
# Build bot
# ------------------------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handler
app.add_handler(menu_handler())                  # /start & /menu
app.add_handler(CallbackQueryHandler(button_callback))  # tombol inline
app.add_handler(ai_handler())                    # /ai
app.add_handler(ytmp_handler())                  # /ytmp
app.add_handler(tiktok_handler())                # /tiktok
app.add_handler(ig_handler())                    # /ig

print("Bot jalan...")
app.run_polling()

