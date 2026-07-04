from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    resend_api_key: str
    email_from: str

    NOTION_CLIENT_ID: str
    NOTION_CLIENT_SECRET: str
    NOTION_REDIRECT_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()