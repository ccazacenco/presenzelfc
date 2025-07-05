"""
Configurazione principale del bot.
"""

import os
from dotenv import load_dotenv

# Carica variabili da .env nella root del progetto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS_JSON", "config/credentials.json")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
TEMP_DIR = os.path.join(DATA_DIR, 'temp')
TEMPLATES_DIR = os.path.join(DATA_DIR, 'templates')
LOG_FILE = os.path.abspath(os.path.join(DATA_DIR, "bot.log"))
SECRET_KEY_PATH = os.path.join(DATA_DIR, "fernet.key")

NOTIFY_PRESENZA_HOUR = 8
NOTIFY_EXTRA_HOUR = 19

DB_PATH = os.path.abspath(os.path.join(DATA_DIR, "presenze.sqlite3"))