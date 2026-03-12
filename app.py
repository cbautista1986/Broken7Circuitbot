import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time
import os

# --- CONFIGURACIÓN ---
TOKEN = "8657723712:AAGlqOVc3MkMadApLfXhdLu1_KHpw4bqe54"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

genai.configure(api_key=IA_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot Broken7Circuit activo y listo."

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Respuesta de la IA
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        print(f"ERROR IA: {e}")
        bot.reply_to(message, "¡Ay, mi vida! Tuve un pequeño tropiezo técnico. ¿Me lo repites? 💖")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    
    # Nos aseguramos de que no haya restos de conexiones viejas
    bot.remove_webhook()
    time.sleep(1)
    
    print("Bot encendido y escuchando...")
    bot.polling(none_stop=True, interval=1, timeout=20)
