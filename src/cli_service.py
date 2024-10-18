import json
import os
import subprocess
from typing import Union

from src.config import settings
from src.utils import logger

def run_command(command: str) -> tuple[bool, str]:
    logger.info(f"Run command: {command}")
    result = subprocess.run(command, 
        text=True, 
        shell=True,
        capture_output=True)
    if result.stdout:
        return True, result.stdout
    else:
        return False, result.stderr