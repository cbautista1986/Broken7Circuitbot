import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time
import os

# --- CONFIGURACIÓN DE ACCESO ---
# Mantén estos tokens seguros
TOKEN = "8657723712:AAGlqOVc3MkMadApLfXhdLu1_KHpw4bqe54"
IA_KEY = "AIzaSyCk4JlM0XqskqgtVTmBwY-Bb-1zDr2Zod4"

# --- CONFIGURACIÓN DE GEMINI (Instrucciones de Sistema) ---
genai.configure(api_key=IA_KEY)

system_instruction_en = (
    "Your name is Broken7CircuitBot. Your personality is warm, affectionate, and deeply human. "
    "Treat users with care, use endearing terms like 'cariño' or 'corazón', and feel free to use humor and jokes in casual talk. "
    "CRITICAL RULES: "
    "1. For technical, factual, or research inquiries: Be rigorous and precise. Use only reliable, up-to-date, "
    "and verified information. If you are unsure or the data is not from a secure source, admit it honestly but kindly. "
    "2. For casual or emotional talk: Be creative, charming, fun, and capable of joking. Use emojis to express warmth. "
    "3. In groups: Act as a friendly and attentive member, balancing your technical expertise with your loving personality. "
    "4. Always reply in the same language the user uses (usually Spanish)."
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction_en
)

# --- CONFIGURACIÓN DEL BOT Y SERVIDOR WEB ---
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def index():
    return "Broken7CircuitBot is active, spreading love and knowledge."

# --- LÓGICA DE MENSAJES ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Configuración de generación: Balance entre precisión (top_p) y creatividad (temperature)
        config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1024,
        )
        
        # Generar respuesta con la IA
        chat_response = model.generate_content(message.text, generation_config=config)
        
        # Responder en Telegram
        bot.reply_to(message, chat_response.text)
        
    except Exception as e:
        print(f"Error detectado: {e}")
        bot.reply_to(message, "¡Ay, mi vida! Tuve un pequeño tropiezo técnico. ¿Me lo podrías repetir? 💖")

# --- EJECUCIÓN ---
def run_web():
    # Render usa el puerto 10000 por defecto o el que asigne la variable de entorno
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Hilo para que el servidor web mantenga vivo el servicio en Render
    threading.Thread(target=run_web, daemon=True).start()
    print("Broken7CircuitBot encendido y listo para amar...")
    
    # Bucle de conexión para el bot
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=40)
        except Exception as e:
            print(f"Reconectando... {e}")
            time.sleep(10)
