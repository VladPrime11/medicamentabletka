from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from data.storage import Storage

storage = Storage()


async def start_handler(update: Update, context: CallbackContext):
    user = storage.add_user(update.effective_user.username, update.effective_user.id)

    # Создание кнопки "Добавить"
    button_add = KeyboardButton("Добавить")
    reply_markup = ReplyKeyboardMarkup([[button_add]], resize_keyboard=True)

    await update.message.reply_text(
        f"Welcome {user.username} to the Medication Reminder Bot!",
        reply_markup=reply_markup
    )
