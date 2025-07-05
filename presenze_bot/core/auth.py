"""
Autenticazione, registrazione e login operai.
"""

import re
import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from utils.security import encrypt, decrypt
from utils.logger import logger
from config.settings import DB_PATH

def validate_cf(cf: str) -> bool:
    return bool(re.match(r"^[A-Z0-9]{16}$", cf.upper()))

def validate_birthdate(date_str: str) -> bool:
    from datetime import datetime
    try:
        d = datetime.strptime(date_str, "%d/%m/%Y")
        return d < datetime.now() and d > datetime(1900, 1, 1)
    except Exception:
        return False

def validate_pin(pin: str) -> bool:
    return bool(re.match(r"^\d{4}$", pin))

def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^(\+39)?3\d{8,9}$", phone.replace(" ", "")))

class AuthDB:
    """Gestione utenti su SQLite."""
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()
    
    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS operai (
            telegram_id INTEGER PRIMARY KEY,
            nome TEXT,
            cognome TEXT,
            birthdate TEXT,
            cf TEXT UNIQUE,
            telefono TEXT,
            pin_enc TEXT
        )""")
        self.conn.commit()
    
    def is_registered(self, telegram_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM operai WHERE telegram_id = ?", (telegram_id,))
        return bool(cur.fetchone())

    def register(self, telegram_id, nome, cognome, birthdate, cf, telefono, pin):
        try:
            pin_enc = encrypt(pin)
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO operai (telegram_id, nome, cognome, birthdate, cf, telefono, pin_enc) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (telegram_id, nome, cognome, birthdate, cf, telefono, pin_enc)
            )
            self.conn.commit()
            logger.info(f"Registrazione operaio {telegram_id} ({cf})")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Tentata doppia registrazione {telegram_id}")
            return False

    def check_pin(self, telegram_id, pin) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT pin_enc FROM operai WHERE telegram_id = ?", (telegram_id,))
        row = cur.fetchone()
        if row:
            return decrypt(row[0]) == pin
        return False
    
    def get_anagrafica(self, telegram_id):
        cur = self.conn.cursor()
        cur.execute("SELECT nome, cognome, birthdate, cf, telefono FROM operai WHERE telegram_id = ?", (telegram_id,))
        return cur.fetchone()

    def update_pin(self, telegram_id, new_pin):
        pin_enc = encrypt(new_pin)
        cur = self.conn.cursor()
        cur.execute("UPDATE operai SET pin_enc = ? WHERE telegram_id = ?", (pin_enc, telegram_id))
        self.conn.commit()

    def find_by_anagrafica(self, nome, cognome, birthdate, cf, telefono):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT telegram_id FROM operai WHERE nome=? AND cognome=? AND birthdate=? AND cf=? AND telefono=?",
            (nome, cognome, birthdate, cf, telefono)
        )
        row = cur.fetchone()
        return row[0] if row else None