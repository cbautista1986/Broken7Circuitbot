import telebot
import google.generativeai as genai
from flask import Flask
import threading
import os
import time

# --- CONFIGURACIÓN SEGURA Y DEFINITIVA ---
# Estos nombres deben coincidir con lo que pusiste en Render
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
        # Aquí la IA procesa tu mensaje
        model_flash = genai.GenerativeModel('gemini-1.5-flash')
        chat_response = model_flash.generate_content(message.text)
        
        if chat_response and chat_response.text:
            bot.reply_to(message, chat_response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé en blanco. ¿Qué me decías? 💖")
            
    except Exception as e:
        print(f"DIAGNÓSTICO TÉCNICO IA: {str(e)}")
        bot.reply_to(message, "¡Ay, mi vida! Tuve un pequeño hipo técnico. ¿Me repites? 💖")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # 1. Arrancar el servidor web para Render
    threading.Thread(target=run_server, daemon=True).start()
    
    # 2. LIMPIEZA: Cerramos cualquier sesión vieja
    print("Limpiando conexiones anteriores...")
    try:
        bot.remove_webhook()
        time.sleep(3) 
    except:
        pass
        
    print("Broken7CircuitBot encendido y escuchando...")
    
    # 3. Bucle para recibir mensajes
    while True:
        try:
            bot.polling(none_stop=True, interval=3, timeout=20)
        except Exception as e:
            print(f"Conflicto o error: {e}")
            time.sleep(15)
