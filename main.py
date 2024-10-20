from telegram import Update
from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                              ContextTypes, ConversationHandler)

from src.config import settings
from src.utils import logger
from src import handlers
from src.handlers import docker_handlers
from src.handlers import states, start_command, docker_menu, go_back, container_menu, help_command, docker_lifecycle_handler, docker_logs_callback_handler

async def pm2_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass

async def pm2_process_menu(update: Update, context: ContextTypes.DEFAULT_TYPE)  -> int:
    pass

def main():
    token = settings.BOT_TOKEN
    application = Application.builder().token(token).build()

    application.add_handler(handlers.auth_handler)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            states.MAIN_MENU: [
                CallbackQueryHandler(docker_menu, pattern="^docker$"),
                CallbackQueryHandler(pm2_menu, pattern="^pm2$"),
            ],
            states.PM2_MENU: [
                CallbackQueryHandler(pm2_process_menu, pattern="^pm2process"),
                CallbackQueryHandler(go_back, pattern="^back$"),
            ],
            states.DOCKER_MENU: [
                CallbackQueryHandler(container_menu, pattern="^container_"),
                CallbackQueryHandler(go_back, pattern="^docker_back$"),
            ],
            states.CONTAINER_MENU: [
                CallbackQueryHandler(docker_lifecycle_handler, pattern="^docker_(start|stop|restart)$"),
                CallbackQueryHandler(docker_logs_callback_handler, pattern="^docker_logs$"),
                CallbackQueryHandler(go_back, pattern="^container_back$"),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
            CommandHandler("help", help_command),
            CallbackQueryHandler(help_command, pattern="^help"),
        ],
    )

    application.add_handler(conv_handler)

    logger.info("Bot started.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()