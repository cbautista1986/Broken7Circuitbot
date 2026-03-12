import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os
import time

# --- CONFIGURACIÓN ---
TOKEN = "8657723712:AAGlqOVc3MkMadApLfXhdLu1_KHpw4bqe54"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

# Inicializar IA
genai.configure(api_key=IA_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Inicializar Bot y Web
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def health_check():
    return "OK", 200

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        # Generar respuesta con Gemini
        response = model.generate_content(message.text)
        if response and response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé pensando. ¿Dime de nuevo? 💖")
    except Exception as e:
        print(f"Error en IA: {e}")
        bot.reply_to(message, "¡Ay, vida! Tuve un tropiezo técnico. Inténtalo otra vez. 💖")

def run_server():
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Iniciar servidor web en un hilo aparte
    threading.Thread(target=run_server, daemon=True).start()
    
    # Limpiar cualquier conexión vieja
    bot.remove_webhook()
    time.sleep(1)
    
    print("Broken7CircuitBot encendido...")
    # Iniciar escucha de mensajes
    bot.polling(none_stop=True, interval=1)
