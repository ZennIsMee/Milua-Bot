from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ContextTypes, filters
import json, os

ADMIN_ID = 6599925642  # ganti ke id kamu

DATA_FILE = "user_data.json"

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f)

# simpan user baru
async def monitor_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    users = load_users()
    user_id = str(user.id)

    if user_id not in users:
        users.append(user_id)
        save_users(users)

        # kirim notifikasi ke admin
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 Pengguna baru chat bot!\n\n👤 {user.first_name} (`{user_id}`)",
            parse_mode="Markdown"
        )

# command /userlist
async def user_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # hanya admin
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("Kamu tidak punya akses ke command ini.")

    users = load_users()
    if not users:
        await update.message.reply_text("Belum ada user yang terdaftar.")
    else:
        text = "📋 *Daftar User:*\n" + "\n".join(f"- `{u}`" for u in users)
        await update.message.reply_text(text, parse_mode="Markdown")

# fungsi setup
def setup_monitor(app):
    app.add_handler(MessageHandler(filters.ChatType.PRIVATE, monitor_private))
    app.add_handler(CommandHandler("userlist", user_list, filters=filters.ChatType.PRIVATE))
