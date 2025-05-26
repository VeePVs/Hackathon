from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from bot.manejador import start, handle_message

TOKEN = 'Token here'

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
