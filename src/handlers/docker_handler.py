from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.handlers import states
from src.utils import logger
from src import cli_service

docker_ps_mock = [
    "MajorBot Up 21 hours",
    "BlumBot Up 2 days",
    "CatsGangBot Up 10 days",
    "MoonbixBot Up 10 days",
    "NotpixelBot Up 10 days",
    "SnapsterBot Up 9 days",
    "DiamoreCoBot Up 10 days",
    "LostDogsBot Up 10 days",
    "OkxRacerBot Up 10 days",
]

async def docker_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display a list of available containers."""
    logger.info("docker_menu")

    query = update.callback_query

    running_containers = cli_service.docker_ps(stopped=False)
    stopped_containers = cli_service.docker_ps(stopped=True)


    keyboard = []
    for i, docker_container in enumerate(running_containers):
        cont_name = docker_container.split(":")[0]
        status = docker_container.split(":")[1]
        keyboard.append([InlineKeyboardButton(f"{i+1}. {docker_container}" + u" 🟢", callback_data=f"container_{cont_name}")])

    for i, docker_container in enumerate(stopped_containers):
        cont_name = docker_container.split(":")[0]
        status = docker_container.split(":")[1]
        keyboard.append([InlineKeyboardButton(f"{i+1}. {docker_container}" + u" 🔴", callback_data=f"container_{cont_name}")])

    keyboard.append([InlineKeyboardButton("« Back", callback_data="docker_back")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Select a container:", reply_markup=reply_markup)

    return states.DOCKER_MENU

async def container_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display options for the selected container."""
    query = update.callback_query
    await query.answer()

    container_name = query.data.split("_", 1)[1]
    context.user_data["selected_container"] = container_name

    logger.debug(f"Container menu: {container_name}")

    # Container-specific actions
    keyboard = [
        [InlineKeyboardButton("Start", callback_data="docker_start"),
         InlineKeyboardButton("Stop", callback_data="stop")],
        [InlineKeyboardButton("Restart", callback_data="restart"),
         InlineKeyboardButton("Logs", callback_data="logs")],
        [InlineKeyboardButton("« Back", callback_data="container_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Selected container: {container_name}", reply_markup=reply_markup)
    return states.CONTAINER_MENU

async def docker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def docker_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass