from http.server import BaseHTTPRequestHandler
import json
import urllib.request
import os
from urllib.parse import urlparse, parse_qs

TOKEN = os.environ.get("TELEGRAM_TOKEN")
# Ссылка на ваш сайт (пока оставим пустую, вставим потом)
WEB_APP_URL = "https://your-vercel-site.vercel.app" 

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        update = json.loads(post_data.decode('utf-8'))

        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            text = update["message"]["text"]

            if text == "/start":
                send_start_message(chat_id)
            else:
                # Здесь будет логика перевода в будущем
                send_message(chat_id, f"Вы написали: {text}")

        self.send_response(200)
        self.end_headers()
        return

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")
        return

def send_start_message(chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    reply_markup = {
        "inline_keyboard": [[
            {"text": "Открыть переводчик", "web_app": {"url": WEB_APP_URL}}
        ]]
    }
    data = json.dumps({
        "chat_id": chat_id, 
        "text": "Привет! Нажми на кнопку ниже, чтобы открыть приложение.",
        "reply_markup": reply_markup
    }).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": chat_id, "text": text}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    urllib.request.urlopen(req)
