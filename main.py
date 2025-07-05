"""
Entry point del bot. Avvio, setup scheduler, dispatcher e handler menu.
"""

import logging
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ConversationHandler
)
from core.menu import get_main_menu, BACK_BTN
from core.auth import AuthDB, validate_pin
from config.settings import TELEGRAM_TOKEN, NOTIFY_PRESENZA_HOUR, NOTIFY_EXTRA_HOUR
from utils.logger import logger

auth_db = AuthDB()

# --- Handler di base --- #

async def start(update, context):
    user = update.effective_user
    if not auth_db.is_registered(user.id):
        await update.message.reply_text(
            "Benvenuto! Registrati inserendo /register.",
            reply_markup=get_main_menu()
        )
    else:
        await update.message.reply_text(
            "Benvenuto! Inserisci il PIN per accedere.",
            reply_markup=get_main_menu()
        )

async def register(update, context):
    await update.message.reply_text("Inizia registrazione.\nNome?")

async def fallback(update, context):
    await update.message.reply_text("Comando non riconosciuto.", reply_markup=get_main_menu())

# --- MAIN --- #

def main():
    logging.getLogger("httpx").setLevel(logging.WARNING)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(MessageHandler(filters.COMMAND, fallback))

    # TODO: ConversationHandler per login, menu, presenza, ecc.

    logger.info("Bot avviato.")
    app.run_polling()

if __name__ == "__main__":
    main()