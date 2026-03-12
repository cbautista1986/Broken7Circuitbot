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

# Instrucciones en inglés para mejor precisión del modelo
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
        # Pequeña pausa para estabilidad
        time.sleep(0.5)
        
        # Configuración de la respuesta
        config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_output_tokens=1024,
        )
        
        # Intentar generar contenido
        chat_response = model.generate_content(message.text, generation_config=config)
        
        if chat_response and chat_response.text:
            bot.reply_to(message, chat_response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé pensando en las musarañas. ¿Me repites? 💖")
            
    except Exception as e:
        error_msg = str(e)
        # Imprime el error exacto en los logs de Render para diagnóstico
        print(f"DIAGNÓSTICO TÉCNICO: {error_msg}")
        
        # Respuesta amigable según el tipo de error
        if "403" in error_msg or "location" in error_msg.lower():
            bot.reply_to(message, "¡Ay, mi vida! Google tiene un bloqueo en nuestra zona. Estoy intentando saltarlo. 💖")
        else:
            bot.reply_to(message, "¡Ay, corazón! Tuve un pequeño tropiezo técnico. ¿Me lo podrías repetir? 💖")

# --- EJECUCIÓN ---
def run_web():
    # Render usa el puerto asignado por la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    # Hilo para el servidor web (mantiene vivo a Render)
    threading.Thread(target=run_web, daemon=True).start()
    print("Bot encendido y listo para la acción...")
    
    # Bucle principal del bot con reconexión automática
    while True:
        try:
            bot.polling(none_stop=True, interval=1, timeout=20)
        except Exception as e:
            print(f"Conflicto o error de conexión: {e}")
            time.sleep(5)
