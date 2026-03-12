import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os
import time

# --- CONFIGURACIÓN DESDE RENDER ---
TOKEN = os.environ.get("TELEGRAM_KEY") 
IA_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=IA_KEY)
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health():
    return "Bot Broken7Circuit en línea", 200

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(message.text)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Me quedé pensando... ¿qué me decías? 💖")
    except Exception as e:
        print(f"ERROR IA: {e}")
        bot.reply_to(message, "¡Ay, mi vida! Tuve un pequeño hipo técnico. ¿Me repites? 💖")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Iniciar servidor web
    threading.Thread(target=run_server, daemon=True).start()
    
    # Limpiar cualquier conexión vieja de Telegram para evitar el Error 409
    print("Limpiando sesión...")
    bot.remove_webhook()
    time.sleep(2)
    
    print("Broken7CircuitBot encendido...")
    # Bucle infinito para recibir mensajes
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
