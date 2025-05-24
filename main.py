from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.manejador import start, handle_message

TOKEN = '8182404121:AAH50htGMGB_-SmA-Mjhh54CPiSsz3zGUZI'

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
