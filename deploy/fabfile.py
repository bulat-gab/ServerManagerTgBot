import logging

from fabric import Connection, task

from deploy_config import settings

logger = logging.getLogger(__name__)

def init_connection() -> Connection:
    c = Connection(
        host=settings.REMOTE_HOST,
        user="root",
        connect_kwargs={
            "key_filename": settings.SSH_KEY_PATH,
        }
    )
    return c
@task
def deploy(c):
    c = init_connection()    

    remote_dir = f"/root/{settings.REPO_NAME}"
    local_dir = settings.PROJECT_PATH_LOCAL

    result = c.run(f"if [ -d {remote_dir} ]; then echo 'exists'; else echo 'not found'; fi", hide=True)
    if result.stdout.strip() != "exists":
        logger.info(f"Cloning repository '{settings.REPO_NAME}'")
        c.run(f"git clone {settings.REPO_URL}")

    c.run(f"cd {remote_dir} && git fetch origin main && git reset --hard origin/main")
    c.put(f"{local_dir}\\.env", f"{remote_dir}/.env")
    c.run(f"cd {remote_dir} && bash ./install.sh")
    c.run(f"cd {remote_dir} && pm2 restart ecosystem.config.js || pm2 start ecosystem.config.js")


if __name__ == "__main__":
    c = init_connection()
    deploy(c)