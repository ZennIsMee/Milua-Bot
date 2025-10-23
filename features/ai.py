from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
import openai, os, httpx

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
DEESEEK_API_KEY = os.environ.get("DEESEEK_API_KEY")
DEESEEK_BASE = "https://api.deepseek.com/v1"
MAX_TOKENS = 60

openai.api_key = OPENAI_API_KEY

def ai_handler():
    return CommandHandler("ai", ai_command)

async def ai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Kirim pesan setelah /ai")
        return

    ai_list = ["openai", "deepseek"]
    for ai in ai_list:
        if ai == "openai":
            try:
                resp = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": text}],
                    max_tokens=MAX_TOKENS
                )
                reply_text = resp.choices[0].message['content'] + " (Replied by OpenAI)"
                await update.message.reply_text(reply_text)
                return
            except Exception as e:
                print("OpenAI error:", e)

        elif ai == "deepseek":
            payload = {
                "model": "deepseek-v3.2-exp",
                "messages": [{"role": "user", "content": text}],
                "max_tokens": MAX_TOKENS
            }
            headers = {"Authorization": f"Bearer {DEESEEK_API_KEY}", "Content-Type": "application/json"}
            try:
                async with httpx.AsyncClient(timeout=20.0) as client:
                    r = await client.post(f"{DEESEEK_BASE}/chat/completions", json=payload, headers=headers)
                    if r.status_code == 200:
                        data = r.json()
                        reply_text = data["choices"][0]["message"]["content"] + " (Replied by DeepSeek)"
                        await update.message.reply_text(reply_text)
                        return
            except Exception as e:
                print("DeepSeek error:", e)

    await update.message.reply_text("Maaf, AI tidak tersedia saat ini.")
