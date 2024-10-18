from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.handlers import states
from src.utils import telegram_utils

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation and asks the user about their preferred command type."""

    title = "<b>Server Manager Bot</b>"
    keyboard = [
        [InlineKeyboardButton('Docker', callback_data='docker')],
        [InlineKeyboardButton('PM2 (Not Implemented Yet)', callback_data='pm2')],
        [InlineKeyboardButton('Help', callback_data='help')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(title, parse_mode='HTML', reply_markup=reply_markup)
    else:
        await update.message.reply_text(title, parse_mode='HTML', reply_markup=reply_markup)

    return states.MAIN_MENU