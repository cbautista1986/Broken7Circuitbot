import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os
import time

# --- CONFIGURACIÓN DIRECTA (Temporalmente) ---
TOKEN = "8657723712:AAE2pkZZL4F26nZtNjPtkYeqfL3qEtPPvNU"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

genai.configure(api_key=IA_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health():
    return "Bot Broken7Circuit en línea", 200

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Respuesta de la IA
        response = model.generate_content(message.text)
        if response.text:
            bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error en Gemini: {e}")
        bot.reply_to(message, "¡Ay, mi vida! Me distraje un segundo. ¿Qué decías? 💖")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # 1. Arrancar el servidor web para Render
    threading.Thread(target=run_server, daemon=True).start()
    
    # 2. LIMPIEZA AGRESIVA: Matamos cualquier conexión previa
    print("Limpiando conexiones anteriores...")
    try:
        bot.remove_webhook()
        # Esperamos un poco más para que Telegram se entere
        time.sleep(3) 
    except:
        pass
        
    print("Broken7CircuitBot encendido y escuchando...")
    
    # 3. Bucle con intervalo de 3 segundos para que no choque con versiones viejas
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            # Si hay conflicto, esperamos 15 segundos antes de reintentar
            print(f"Conflicto o error: {e}")
            time.sleep(15)
