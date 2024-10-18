from telegram import Update
from telegram.ext import ContextTypes

from src.utils import telegram_utils

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = "This is a help message."
    
    await telegram_utils.send_message(update, context, text=help_message)