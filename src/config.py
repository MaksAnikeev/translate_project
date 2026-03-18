from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    TRANSLATE_API_URL: str
    TRANSLATE_API_TOKEN: str

    MAX_CHUNK_SIZE: int

    SOURCE_LANG = "ru"
    TARGET_LANG = "en"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str | None = None

    @property
    def RADIS_URL(self):
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}"
        else:
            return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    HEADERS = {
        "Authorization": f"Bearer {TRANSLATE_API_TOKEN}",  # ← если нужен
        "Content-Type": "application/json",
        "User-Agent": "AsyncFileTranslator/1.0",
    }

    REQUEST_PARAMS = {
        "source_lang": "ru",
        "target_lang": "en",
    }


    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")


settings = Settings()  # type: ignore
