"""
Gestione cantieri personali: CRUD (crea, modifica, elimina, lista).
"""

import sqlite3
from config.settings import DB_PATH
from utils.logger import logger

class CantieriDB:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cantieri (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            nome TEXT,
            indirizzo TEXT,
            note TEXT,
            UNIQUE(telegram_id, nome)
        )
        """)
        self.conn.commit()

    def lista_cantieri(self, telegram_id):
        cur = self.conn.cursor()
        cur.execute("SELECT nome FROM cantieri WHERE telegram_id = ?", (telegram_id,))
        return [row[0] for row in cur.fetchall()]

    def aggiungi_cantiere(self, telegram_id, nome, indirizzo, note):
        try:
            cur = self.conn.cursor()
            cur.execute("""
                INSERT INTO cantieri (telegram_id, nome, indirizzo, note) VALUES (?, ?, ?, ?)
            """, (telegram_id, nome, indirizzo, note))
            self.conn.commit()
            logger.info(f"Aggiunto cantiere {nome} per {telegram_id}")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"Cantiere duplicato {nome} per {telegram_id}")
            return False

    def elimina_cantiere(self, telegram_id, nome):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM cantieri WHERE telegram_id = ? AND nome = ?", (telegram_id, nome))
        self.conn.commit()

    def modifica_cantiere(self, telegram_id, nome_old, nome_new, indirizzo, note):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE cantieri SET nome = ?, indirizzo = ?, note = ? WHERE telegram_id = ? AND nome = ?
        """, (nome_new, indirizzo, note, telegram_id, nome_old))
        self.conn.commit()

    def get_cantiere(self, telegram_id, nome):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT nome, indirizzo, note FROM cantieri WHERE telegram_id = ? AND nome = ?
        """, (telegram_id, nome))
        return cur.fetchone()