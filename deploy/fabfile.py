import logging
import os
from fabric import Connection, task

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


is_github_action = "GITHUB_ACTIONS" in os.environ
if not is_github_action:
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env.deploy'))

REMOTE_HOST = os.environ['REMOTE_HOST']
SSH_KEY_PATH = os.environ['SSH_KEY_PATH']
LOCAL_DIR = os.environ['LOCAL_DIR']
REPO_NAME = os.environ['REPO_NAME']
REPO_URL = os.environ['REPO_URL']

def init_connection() -> Connection:
    c = Connection(
        host=REMOTE_HOST,
        user="root",
        connect_kwargs={
            "key_filename": SSH_KEY_PATH,
        }
    )
    return c
@task
def deploy(c):
    c = init_connection()    

    remote_dir = f"/root/{REPO_NAME}"

    result = c.run(f"if [ -d {remote_dir} ]; then echo 'exists'; else echo 'not found'; fi", hide=True)
    if result.stdout.strip() != "exists":
        logger.info(f"Cloning repository '{REPO_NAME}'")
        c.run(f"git clone {REPO_URL}")

    c.run(f"cd {remote_dir} && git fetch origin main && git reset --hard origin/main")
    c.put(f"{LOCAL_DIR}\\.env", f"{remote_dir}/.env")
    c.run(f"cd {remote_dir} && bash ./install.sh")
    c.run(f"cd {remote_dir} && pm2 restart ecosystem.config.js || pm2 start ecosystem.config.js")
    logger.info("Deploy finished")

if __name__ == "__main__":
    c = init_connection()
    deploy(c)