from telegram import (ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                          InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                              ContextTypes, ConversationHandler, MessageHandler, filters)

from src.config import settings


async def restrict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="You are not authorized to use this bot."
    )

auth_handler = MessageHandler(~filters.User(settings.ALLOWED_USER_IDS), restrict)