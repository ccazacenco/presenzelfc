"""
Gestione menu principale e navigazione reply keyboard.
"""

from telegram import ReplyKeyboardMarkup

MAIN_MENU = [
    ["📝 Registra presenza", "👤 Dati personali"],
    ["🏗️ I miei cantieri", "📅 Visualizza presenze"],
    ["📤 Scarica report"]
]
BACK_BTN = "🔙 Torna indietro"
CANCEL_BTN = "❌ Annulla"

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Restituisce il markup del menu principale con pulsante indietro.
    """
    kb = [row[:] for row in MAIN_MENU]
    for row in kb:
        if BACK_BTN not in row:
            row.append(BACK_BTN)
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)