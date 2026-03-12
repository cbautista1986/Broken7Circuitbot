import telebot
import google.generativeai as genai
from flask import Flask
import threading
import time
import os

# --- CONFIGURACIÓN DE ACCESO ---
TOKEN = "8657723712:AAGlqOVc3MkMadApLfXhdLu1_KHpw4bqe54"
IA_KEY = "AIzaSyCgDozHxPy1VKTGVVC_pyf_OlNFYjh8ybw"

# --- CONFIGURACIÓN DE GEMINI ---
genai.configure(api_key=IA_KEY)

system_instruction_en = (
    "Your name is Broken7CircuitBot. Your personality is warm, affectionate, and deeply human. "
    "Treat users with care, use endearing terms like 'cariño' or 'corazón', and feel free to use humor. "
    "CRITICAL RULES: "
    "1. For technical inquiries: Be rigorous and use verified information. "
    "2. For casual talk: Be creative, charming, and fun. Use emojis. "
    "3. Always reply in the same language the user uses."
)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=system_instruction_en
)

# --- CONFIGURACIÓN DEL BOT Y SERVIDOR ---
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def index():
    return "Broken7CircuitBot is active and spreading love."

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    try:
        config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1024,
        )
        # Generamos la respuesta
        chat_response = model.generate_content(message.text, generation_config=config)
        
        if chat_response.text:
            bot.reply_to(message, chat_response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé pensando en blanco. ¿Me repites? 💖")
            
    except Exception as e:
        # Esto imprimirá el error real en los Logs de Render
        print(f"DIAGNÓSTICO TÉCNICO: {str(e)}")
        bot.reply_to(message, "¡Ay, corazón! Tuve un pequeño tropiezo técnico. ¿Me lo podrías repetir? 💖")

# --- EJECUCIÓN ---
def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    print("Bot encendido con nueva llave...")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=40)
        except Exception as e:
            print(f"Reconectando bot... {e}")
            time.sleep(10)
