from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src import handlers

async def go_back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Handle the Back button."""
    query = update.callback_query
    await query.answer()

    # If the user clicks "Back" while on the container menu, show the Docker menu
    action = query.data
    if action == "docker_back":
        return await handlers.start_handler(update, context)
    elif action == "container_back":
        context.user_data.pop("selected_container", None)
        return await handlers.docker_menu(update, context)
    else:
        return await handlers.start_handler(update, context)