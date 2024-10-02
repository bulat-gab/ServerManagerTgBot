import subprocess
from typing import Union
from telegram import (ForceReply, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update,
                          InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                              ContextTypes, ConversationHandler, MessageHandler, filters)

import os

from src.config import settings
from src.utils import logger
from src.utils import file_utils

def run_command(command: Union[str, list[str]]):
    result = subprocess.run(command, 
        text=True, 
        shell=True,
        capture_output=True)
    if result.stdout:
        return result.stdout
    else:
        return result.stderr

async def docker_ps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # response = run_command(["docker", "ps", "--format", "{{.Names}}: ({{.Status}})"])
    response = run_command("docker ps --format '{{.Names}}: ({{.Status}})'")

    await send_message(update, context, response)

async def docker_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        split = update.message.text.split(" ")
        arguments_list = split[1:]

        arg_str = " ".join(arguments_list[1:])

    except Exception:
        logger.warning(f"Invalid input: {update.message.text}")
        return

    response = run_command(f"docker {arg_str}")
    # response = run_command(["docker", "logs", *arguments_list])
    await send_message(update, context, response)

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE, text: str) -> int:
    """Send a message with the help of the bot."""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
        await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
        await update.callback_query.answer()
    elif update.message:
        await update.message.reply_text(text)
    
    file_utils.append(text) # FOR DEBUG ONLY

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await send_message(update, context, update.message.text)

def main():
    token = settings.BOT_TOKEN
    application = Application.builder().token(token).build()


    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("docker_ps", docker_ps))
    application.add_handler(CommandHandler("docker", docker_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C

    logger.info("Bot started.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    # application.add_handler(CommandHandler("docker_ps", docker_ps))

if __name__ == "__main__":
    main()