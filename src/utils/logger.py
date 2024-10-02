import sys
from loguru import logger


logger.remove()
logger.add(sink=sys.stdout, format="<light-white>{time:YYYY-MM-DD HH:mm:ss}</light-white>"
                                   " | <level>{level}</level>"
                                   " | <light-white><b>{message}</b></light-white>", colorize=True)
logger = logger.opt(colors=True)