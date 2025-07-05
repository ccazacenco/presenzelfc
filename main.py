import os
print("DEBUG: import os OK")
import threading
print("DEBUG: import threading OK")
from http.server import BaseHTTPRequestHandler, HTTPServer
print("DEBUG: import http.server OK")
from telegram.ext import ApplicationBuilder, CommandHandler
print("DEBUG: import telegram.ext OK")
from core.menu import get_main_menu
print("DEBUG: import core.menu OK")
from core.auth import AuthDB
print("DEBUG: import core.auth OK")
from config.settings import TELEGRAM_TOKEN
print("DEBUG: import config.settings OK")

auth_db = AuthDB()
print("DEBUG: auth_db istanziato")

async def start(update, context):
    await update.message.reply_text("Benvenuto! Bot presenze attivo.")

def main():
    print("DEBUG: main() chiamata")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    # ... altri handler

    port = int(os.environ.get("PORT", 8443))
    webhook_url = os.environ.get("WEBHOOK_URL")
    if not webhook_url:
        raise Exception("WEBHOOK_URL env var is required")

    print(f"DEBUG: Avvio bot su porta {port} e webhook_url {webhook_url}/webhook")

    app.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url=f"{webhook_url}/webhook"
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
    print("DEBUG: start_health_server() chiamata")
    server = HTTPServer(('0.0.0.0', 8080), HealthHandler)
    server.serve_forever()

if __name__ == "__main__":
    print("DEBUG: __main__")
    threading.Thread(target=start_health_server, daemon=True).start()
    main()
