"""
Generazione report Excel/PDF e statistiche.
"""

import pandas as pd
from core.presenze import PresenzeDB
from config.settings import TEMP_DIR
import os

class ReportManager:
    def __init__(self, presenze_db: PresenzeDB):
        self.presenze_db = presenze_db

    def export_presenze_excel(self, telegram_id, out_path, mese=None, cantiere=None):
        """Esporta presenze in Excel per l'operaio (filtri opzionali)."""
        presenze = self.presenze_db.lista_presenze(telegram_id, limit=1000, mese=mese, cantiere=cantiere)
        df = pd.DataFrame(presenze, columns=["ID", "Data", "Cantiere", "Ore", "Note", "Straordinario"])
        df["Straordinario"] = df["Straordinario"].apply(lambda x: "Sì" if x else "")
        df.to_excel(out_path, index=False)

    def export_report_pdf(self, telegram_id, out_path, mese=None, cantiere=None):
        """Genera un report PDF mensile (richiede libreria reportlab)."""
        # TODO: implementa PDF (usa pandas + reportlab)
        pass