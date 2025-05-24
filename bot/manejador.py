from telegram import Update
from telegram.ext import ContextTypes
from .respuestas import responder_pregunta

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Hola {update.effective_user.first_name}, soy NeuCol_Bot y soy tu chatbot de confianza para saber la nomina y finanzas de NiloApp')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        pregunta = update.message.text.lower()
        respuesta = responder_pregunta(pregunta)
        await update.message.reply_text(respuesta)
    else:
        await update.message.reply_text("Por favor, repite el mensaje")