import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
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
    # Qui puoi aggiungere altri handler

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

# --- HEALTH CHECK SERVER ---
def start_health_server():
    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/healthz":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"ok")
            else:
                self.send_response(404)
                self.end_headers()
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    # Avvia il mini-server health check in background
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
