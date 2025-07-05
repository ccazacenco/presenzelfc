# Presenze Operai Telegram Bot

Bot Telegram per la gestione delle presenze degli operai, integrato con Google Drive e notifiche.

## Struttura progetto

```
presenze_bot/
├── core/         # Logica principale (menu, auth, presenze, report)
├── utils/        # Utility (gdrive, logger, security)
├── data/         # Dati, template, file temporanei
├── config/       # Configurazione e settings
├── main.py       # Entry point
├── requirements.txt
└── README.md
```

## Setup iniziale

1. **Crea file `.env` nella root** con:
   ```
   TELEGRAM_TOKEN=...
   GOOGLE_CREDENTIALS_JSON=...
   ADMIN_CHAT_ID=...
   ```
2. **Copia il file di credenziali Google Drive** in `config/credentials.json`.

3. **Installa i requirements**:
   ```
   pip install -r requirements.txt
   ```

4. **Avvia il bot**:
   ```
   python main.py
   ```

## Google Drive

- Il bot usa gspread e Google API per backup presenze/cantieri su Drive.
- Ogni operaio ha una cartella personale su Drive (basata su CF).
- I file Excel/PDF vengono salvati e scaricati automaticamente.

## Deploy

- Puoi usare un server Linux con Python 3.10+.
- Consigliato: systemd service o supervisord per l'esecuzione continua.
- Per notifiche scheduler (APScheduler) il bot deve restare sempre attivo.

## Sicurezza

- Dati sensibili (PIN, CF, telefono) sono criptati con Fernet.
- Logging dettagliato in `data/bot.log`.

## TODO

- Implementare tutti gli handler conversazionali
- Gestione completa backup, report, notifiche
- Test automatici (pytest)