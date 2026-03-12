import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time
import os

# --- CONFIGURACIÓN DE ACCESO ---
# Asegúrate de que estos tokens sean los correctos
TOKEN = "8657723712:AAGlqOVc3MkMadApLfXhdLu1_KHpw4bqe54"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

# --- CONFIGURACIÓN DE GEMINI ---
genai.configure(api_key=IA_KEY)

system_instruction_en = (
    "Your name is Broken7CircuitBot. Your personality is warm, affectionate, and deeply human. "
    "Treat users with care, use endearing terms like 'cariño' or 'corazón', and feel free to use humor. "
    "CRITICAL RULES: "
    "1. For technical or research inquiries: Be rigorous and use verified information. "
    "2. For casual talk: Be creative, charming, and fun. Use emojis to express warmth. "
    "3. Always reply in the same language the user uses (usually Spanish)."
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
    return "Broken7CircuitBot is active and spreading love."

# --- LÓGICA DE MENSAJES ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        # Pequeña pausa de estabilidad
        time.sleep(0.5)
        
        config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1024,
        )
        
        chat_response = model.generate_content(message.text, generation_config=config)
        
        if chat_response and chat_response.text:
            bot.reply_to(message, chat_response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé pensando en las musarañas. ¿Me repites? 💖")
            
    except Exception as e:
        error_msg = str(e)
        print(f"DIAGNÓSTICO TÉCNICO: {error_msg}")
        
        if "403" in error_msg or "location" in error_msg.lower():
            bot.reply_to(message, "¡Ay, mi vida! Google tiene un bloqueo en nuestra zona. Estoy intentando saltarlo. 💖")
        else:
            bot.reply_to(message, "¡Ay, corazón! Tuve un pequeño tropiezo técnico. ¿Me lo podrías repetir? 💖")

# --- EJECUCIÓN ---
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Servidor web para Render
    threading.Thread(target=run_web, daemon=True).start()
    print("Broken7CircuitBot encendido...")
    
    # Bucle con manejo de Error 409 (Conflict)
    while True:
        try:
            # interval=2 y timeout=20 para evitar saturar la conexión
            bot.polling(none_stop=True, interval=2, timeout=20)
        except Exception as e:
            # Si hay conflicto, esperamos 10 segundos y seguimos
            print(f"Error de polling detectado: {e}")
            time.sleep(10)
