from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from data.storage import Storage
from datetime import datetime, timedelta

storage = Storage()

TEXT, NAME, DATE, TIME = range(4)

async def add_medication_start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Enter Medication Name", callback_data='enter_name')],
        [InlineKeyboardButton("Cancel", callback_data='cancel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = await update.message.reply_text("Please choose an action:", reply_markup=reply_markup)
    context.user_data['bot_message_id'] = message.message_id
    context.user_data['name'] = ""
    context.user_data['selected_dates'] = []
    context.user_data['selected_times'] = []
    return TEXT

async def enter_medication_name(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text("Please enter the medication name:")
    return NAME

async def add_medication_name(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    await update.message.delete()
    await send_date_picker(update, context, edit=True)
    return DATE

async def send_date_picker(update: Update, context: CallbackContext, edit=False):
    today = datetime.now()
    keyboard = [
        [
            InlineKeyboardButton(
                f"{'✔ ' if (today + timedelta(days=i)).strftime('%Y-%m-%d') in context.user_data['selected_dates'] else ''}{(today + timedelta(days=i)).strftime('%Y-%m-%d')}",
                callback_data=(today + timedelta(days=i)).strftime('%Y-%m-%d')
            )
        ] for i in range(7)
    ]
    keyboard.append([InlineKeyboardButton("Done", callback_data='done')])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Medication Name: {context.user_data['name']}\nPlease choose the date(s):"
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data['bot_message_id'],
        text=text,
        reply_markup=reply_markup
    )

async def date_picker_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'done':
        await send_time_picker(update, context, edit=True)
        return TIME

    if query.data == 'cancel':
        await cancel(update, context)
        return ConversationHandler.END

    selected_date = query.data
    if selected_date in context.user_data['selected_dates']:
        context.user_data['selected_dates'].remove(selected_date)
    else:
        context.user_data['selected_dates'].append(selected_date)

    await send_date_picker(update, context, edit=True)
    return DATE

async def send_time_picker(update: Update, context: CallbackContext, edit=False):
    keyboard = [
        [
            InlineKeyboardButton(
                f"{'✔ ' if f'{hour:02d}:00' in context.user_data['selected_times'] else ''}{hour:02d}:00",
                callback_data=f"{hour:02d}:00"
            )
        ] for hour in range(24)
    ]
    keyboard.append([InlineKeyboardButton("Back", callback_data='back')])
    keyboard.append([InlineKeyboardButton("Done", callback_data='time_done')])
    keyboard.append([InlineKeyboardButton("Cancel", callback_data='cancel')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = f"Medication Name: {context.user_data['name']}\nSelected Dates: {', '.join(context.user_data['selected_dates'])}\nPlease choose the time(s):"
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=context.user_data['bot_message_id'],
        text=text,
        reply_markup=reply_markup
    )

async def time_picker_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'back':
        await send_date_picker(update, context, edit=True)
        return DATE

    if query.data == 'time_done':
        user = storage.get_user(update.effective_user.id)
        if user:
            for selected_date in context.user_data['selected_dates']:
                for selected_time in context.user_data['selected_times']:
                    date_time_str = f"{selected_date} {selected_time}"
                    date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                    storage.add_medication(user, context.user_data['name'], date_time)
            await query.message.edit_text(f"Medication {context.user_data['name']} added for selected dates and times successfully.")
        else:
            await query.message.edit_text("User not found.")
        return ConversationHandler.END

    if query.data == 'cancel':
        await cancel(update, context)
        return ConversationHandler.END

    selected_time = query.data
    if selected_time in context.user_data['selected_times']:
        context.user_data['selected_times'].remove(selected_time)
    else:
        context.user_data['selected_times'].append(selected_time)

    await send_time_picker(update, context, edit=True)
    return TIME

async def cancel(update: Update, context: CallbackContext):
    await update.callback_query.message.edit_text("Action canceled.")
    return ConversationHandler.END

add_medication_conv_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex('^(Добавить)$'), add_medication_start)],
    states={
        TEXT: [CallbackQueryHandler(enter_medication_name, pattern='^enter_name$')],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_medication_name)],
        DATE: [CallbackQueryHandler(date_picker_callback)],
        TIME: [CallbackQueryHandler(time_picker_callback)],
    },
    fallbacks=[CallbackQueryHandler(cancel, pattern='^cancel$')],
)
