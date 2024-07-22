from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, CallbackQueryHandler
from utils.config import TOKEN
from bot.handlers.start_handler import start_handler
from bot.handlers.add_medication_handler import add_medication_conv_handler

def start_bot():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(add_medication_conv_handler)

    application.run_polling()
