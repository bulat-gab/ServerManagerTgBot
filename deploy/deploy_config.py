from pydantic_settings import BaseSettings, SettingsConfigDict


class DeploySettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.deploy", env_ignore_empty=True)

    REMOTE_HOST: str
    SSH_KEY_PATH: str
    PROJECT_PATH_LOCAL: str
    REPO_NAME: str = "ServerManagerTgBot"
    REPO_URL: str = "git@github.com:bulat-gab/ServerManagerTgBot.git"
    PM2_BOT_NAME: str = "server_bot"


settings = DeploySettings()