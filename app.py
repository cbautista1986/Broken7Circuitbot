# --- REEMPLAZA SOLO ESTA PARTE DEL CÓDIGO ---
def handle_messages(message):
    try:
        # Añadimos un pequeño retraso para no saturar
        time.sleep(1) 
        
        # Forzamos que la IA genere contenido de forma más simple
        chat_response = model.generate_content(
            message.text,
            generation_config={"temperature": 0.7, "max_output_tokens": 800}
        )
        
        if chat_response.text:
            bot.reply_to(message, chat_response.text)
        else:
            bot.reply_to(message, "Cariño, me quedé en blanco. ¿Me repites? 💖")
            
    except Exception as e:
        # Esto te dirá el error real en los Logs de Render
        print(f"DIAGNÓSTICO REAL: {str(e)}")
        bot.reply_to(message, "¡Ay, mi vida! Google se puso difícil. Reintenta en un segundo. 💖")
