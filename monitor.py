from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters, CommandHandler
import json, os, datetime

ADMIN_ID = 6599925642  # ganti dengan ID kamu
USERS_FILE = "users.json"
LOG_FILE = "monitor_log.txt"

def save_user(user_id, username):
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            users = json.load(f)
    else:
        users = {}

    if str(user_id) not in users:
        users[str(user_id)] = username or "None"
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)
        print(f"[NEW USER] {username} ({user_id}) added.")
        return True
    return False

def log_message(username, user_id, text):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {username} ({user_id}): {text}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

async def monitor_private(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        user_id = update.effective_user.id
        username = update.effective_user.username or "None"
        text = update.message.text if update.message else "<no text>"

        is_new = save_user(user_id, username)
        log_message(username, user_id, text)
        print(f"[MONITOR] {username} ({user_id}): {text}")

        if is_new:
            try:
                await context.bot.send_message(
                    ADMIN_ID,
                    f"👤 *New user detected!*\n\nUsername: @{username}\nID: `{user_id}`",
                    parse_mode="Markdown",
                )
            except Exception as e:
                print(f"[WARN] Gagal kirim notifikasi admin: {e}")

async def user_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return  # tolak user non-admin

    if not os.path.exists(USERS_FILE):
        await update.message.reply_text("📂 Belum ada user yang tercatat.")
        return

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    if not users:
        await update.message.reply_text("📂 Belum ada user yang tercatat.")
        return

    lines = [f"📋 *Total users:* {len(users)}\n"]
    for uid, uname in users.items():
        lines.append(f"• @{uname} — `{uid}`")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")

def setup_monitor(app):
    app.add_handler(MessageHandler(filters.PRIVATE, monitor_private))
    app.add_handler(CommandHandler("userlist", user_list))
    
