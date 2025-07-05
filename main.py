import os
from telegram.ext import ApplicationBuilder, CommandHandler
from core.menu import get_main_menu
from core.auth import AuthDB
from config.settings import TELEGRAM_TOKEN

auth_db = AuthDB()

async def start(update, context):
    await update.message.reply_text("Benvenuto! Bot presenze attivo.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # aggiungi qui altri handler

    # --- WEBHOOK PART (Render style) ---
    port = int(os.environ.get("PORT", 8443))
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        raise Exception("WEBHOOK_URL env var is required")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{webhook_url}/webhook",
        webhook_path="/webhook",
    )

if __name__ == "__main__":
    main()