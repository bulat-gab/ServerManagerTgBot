from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from src.handlers import states
from src.utils import logger, telegram_utils
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
        keyboard.append([InlineKeyboardButton(f"{i+1}. {cont_name}. {status}" + u" 🟢", callback_data=f"container_{cont_name}")])

    for i, docker_container in enumerate(stopped_containers):
        cont_name = docker_container.split(":")[0]
        status = docker_container.split(":")[1]
        keyboard.append([InlineKeyboardButton(f"{i+1}. {cont_name}. {status}" + u" 🔴", callback_data=f"container_{cont_name}")])

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
         InlineKeyboardButton("Stop", callback_data="docker_stop")],
        [InlineKeyboardButton("Restart", callback_data="docker_restart"),
         InlineKeyboardButton("Logs", callback_data="docker_logs")],
        [InlineKeyboardButton("« Back", callback_data="container_back")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Selected container: {container_name}", reply_markup=reply_markup)
    return states.CONTAINER_MENU

async def handler_docker_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    action = update.callback_query.data

    container_name = context.user_data.get("selected_container")
    if not container_name:
        return

    cmd = f"docker {action} {container_name}"
    if action == "logs":
        cmd += " -n 15" # TODO: adjust the logs length

    result, output = cli_service.run_command(cmd)
    await telegram_utils.send_message(update, context, output)
    return


# async def docker_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     container_name = context.user_data.get("selected_container")
#     if not container_name:
#         return
    
#     result, output = cli_service.run_command(f"docker start {container_name}")
#     await telegram_utils.send_message(update, context, output)
#     return

# async def docker_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     container_name = context.user_data.get("selected_container")
#     if not container_name:
#         return
    
#     result, output = cli_service.run_command(f"docker stop {container_name}")
#     await telegram_utils.send_message(update, context, output)
#     return

# async def docker_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     container_name = context.user_data.get("selected_container")
#     if not container_name:
#         return
    
#     result, output = cli_service.run_command(f"docker restart {container_name}")
#     await telegram_utils.send_message(update, context, output)
#     return

# async def docker_logs(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     container_name = context.user_data.get("selected_container")
#     if not container_name:
#         return
    
#     result, output = cli_service.run_command(f"docker logs -n 15 {container_name}")
#     await telegram_utils.send_message(update, context, output)
#     return