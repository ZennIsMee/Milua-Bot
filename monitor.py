from pyrogram import Client, filters
import json
import os
import datetime

# 🔧 Ganti dengan ID kamu
ADMIN_ID = 6599925642

USERS_FILE = "users.json"
LOG_FILE = "monitor_log.txt"

def save_user(user_id, username):
    """Simpan user baru ke file users.json"""
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
        return True  # user baru
    return False

def log_message(username, user_id, text):
    """Tulis aktivitas chat ke monitor_log.txt"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] {username} ({user_id}): {text}\n"

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_line)

def load_users():
    """Ambil semua data user dari users.json"""
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def setup_monitor(app: Client):
    """Aktifkan fitur monitoring pesan private"""
    @app.on_message(filters.private)
    async def monitor_private(client, message):
        if m
