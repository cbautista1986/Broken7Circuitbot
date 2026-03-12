import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os
import time

# --- CONFIGURACIÓN CON TU NUEVO TOKEN ---
TOKEN = "8657723712:AAE2pkZZL4F26nZtNjPtkYeqfL3qEtPPvNU"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

# Configurar Inteligencia Artificial
genai.configure(api_key=IA_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializar Bot y Servidor
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health():
    return "Broken7CircuitBot con nuevo token activo", 200

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Generamos la respuesta con Gemini
        chat_response = model.generate_content(message.text)
        if chat_response.text:
            bot.reply_to(message, chat_response.text)
    except Exception as e:
        print(f"DIAGNÓSTICO IA: {e}")
        bot.reply_to(message, "¡Ay, mi vida! Dame un segundito que me distraje. 💖")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Iniciar servidor web para Render
    threading.Thread(target=run_server, daemon=True).start()
    
    # --- LIMPIEZA INICIAL ---
    print("Limpiando conexiones viejas del nuevo token...")
    try:
        bot.remove_webhook()
        time.sleep(2)
    except:
        pass
        
    print("Broken7CircuitBot encendido y listo...")
    
    # Bucle principal con intervalo para evitar el error 409
    while True:
        try:
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            print(f"Reintentando conexión: {e}")
            time.sleep(10)
