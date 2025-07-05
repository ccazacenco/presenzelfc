# presenzelfc

Bot Telegram per la gestione presenze operai, pronto per deploy su Render con webhook.

## Setup

1. Copia `.env.example` in `.env` e inserisci i tuoi valori.
2. Installa i requirements:
   ```
   pip install -r requirements.txt
   ```
3. Avvia in locale (solo per test):
   ```
   python main.py
   ```
4. Deploy su Render come **Web Service**. Imposta le variabili ambiente, e carica (se serve) `config/credentials.json` come Secret File.

## Note webhook

- Il bot riceve messaggi solo tramite webhook (`/webhook`).  
- Devi impostare la variabile ambiente `WEBHOOK_URL` con l’URL pubblico Render (es: `https://presenzelfc.onrender.com`).  
- Non usare polling!

## Licenza

MIT