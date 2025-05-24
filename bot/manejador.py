from telegram import Update
from telegram.ext import ContextTypes
from .respuestas import responder_pregunta

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f'Hola {update.effective_user.first_name}, soy NeuCol_Bot y soy tu chatbot de confianza para saber la nómina y finanzas de NiloApp'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        pregunta = update.message.text.lower()
        resultado = responder_pregunta(pregunta)

        if isinstance(resultado, tuple):
            ruta_imagen, texto = resultado
            with open(ruta_imagen, 'rb') as photo:
                await update.message.reply_photo(photo=photo, caption=texto)
        else:
            await update.message.reply_text(resultado)
    else:
        await update.message.reply_text("Por favor, repite el mensaje.")
