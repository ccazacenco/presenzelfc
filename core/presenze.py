"""
Gestione presenze giornaliere: inserimento, modifica, visualizzazione.
"""

import sqlite3
from datetime import date
from config.settings import DB_PATH
from utils.logger import logger

class PresenzeDB:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS presenze (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER,
            data DATE,
            cantiere TEXT,
            ore REAL,
            note TEXT,
            straordinario INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def registra_presenza(self, telegram_id, data, cantiere, ore, note, straordinario=0):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO presenze (telegram_id, data, cantiere, ore, note, straordinario)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (telegram_id, data, cantiere, ore, note, straordinario))
        self.conn.commit()
        logger.info(f"Reg pres: {telegram_id} {data} {cantiere} {ore}")

    def lista_presenze(self, telegram_id, limit=50, mese=None, cantiere=None):
        cur = self.conn.cursor()
        query = "SELECT id, data, cantiere, ore, note, straordinario FROM presenze WHERE telegram_id = ?"
        params = [telegram_id]
        if mese:
            query += " AND strftime('%Y-%m', data) = ?"
            params.append(mese)
        if cantiere:
            query += " AND cantiere = ?"
            params.append(cantiere)
        query += " ORDER BY data DESC LIMIT ?"
        params.append(limit)
        cur.execute(query, tuple(params))
        return cur.fetchall()

    def get_presenza(self, presenza_id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM presenze WHERE id = ?", (presenza_id,))
        return cur.fetchone()

    def update_presenza(self, presenza_id, data, cantiere, ore, note, straordinario):
        cur = self.conn.cursor()
        cur.execute("""
            UPDATE presenze SET data=?, cantiere=?, ore=?, note=?, straordinario=?
            WHERE id=?
        """, (data, cantiere, ore, note, straordinario, presenza_id))
        self.conn.commit()

    def delete_presenza(self, presenza_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM presenze WHERE id=?", (presenza_id,))
        self.conn.commit()

    def statistiche(self, telegram_id, mese=None, cantiere=None):
        presenze = self.lista_presenze(telegram_id, limit=1000, mese=mese, cantiere=cantiere)
        tot_ore = sum(p[3] for p in presenze)
        straord = sum(p[3] for p in presenze if p[5])
        return {"tot_ore": tot_ore, "straordinari": straord, "n_giorni": len(presenze)}