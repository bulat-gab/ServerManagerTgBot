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
        logger.debug(f"Command executed: {result.stdout.replace("\n", " ")}")
        return True, result.stdout
    else:
        logger.warning(f"Command finished with error: {result.stderr.replace("\n", " ")}")
        return False, result.stderr
    

def docker_ps(stopped: bool = False):
    cmd = "docker ps --format '{{.Names}}:{{.Status}}'"
    if stopped:
        cmd += " --filter 'status=exited'"

    result, response = run_command(cmd)

    if not result:
        return []
    
    response = response.splitlines()
    return response