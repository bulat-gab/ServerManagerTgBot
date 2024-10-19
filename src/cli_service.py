import json
import os
import subprocess
from typing import Union

from src.config import settings
from src.utils import logger

def run_command(command: str) -> tuple[bool, str]:
    logger.debug(f"Run command: {command}")
    result = subprocess.run(command, 
        text=True, 
        shell=True,
        capture_output=True)
    if result.stdout:
        logger.debug(f"Command executed: {result.stdout}")
        return True, result.stdout
    else:
        logger.warning(f"Command finished with error: {result.stderr}")
        return False, result.stderr
    

def docker_ps():
    result, response = run_command("docker ps --format '{{.Names}}:{{.Status}}'")

    if not result:
        return []
    
    return response