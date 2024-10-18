from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    BOT_TOKEN: str
    BOT_USERNAME: str = ""
    ALLOWED_USER_IDS: list[int] = [] # Telegram user ids that are allowed to use this bot.


settings = Settings()