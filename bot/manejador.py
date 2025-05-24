from telegram import Update
from telegram.ext import ContextTypes
from .respuestas import responder_pregunta

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy NeuColBot. Pregúntame sobre tu facturación o nómina.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text.lower()
    respuesta = responder_pregunta(pregunta)
    await update.message.reply_text(respuesta)
