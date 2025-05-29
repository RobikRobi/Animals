from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class EnvData(BaseSettings):
    DB_URL: str
    DB_URL_ASYNC: str
    SMTP_SERVER: str
    SMTP_PORT: int 
    EMAIL_LOGIN: str
    EMAIL_PASSWORD: str
    EMAIL_SENDER: str
    EMAIL_RECEIVER: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


class Config(BaseModel):
    env_data: EnvData = EnvData()
    
config = Config()
