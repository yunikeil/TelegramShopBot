from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла

current_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
root_path = os.path.dirname(os.path.dirname(current_file_path))
env_path = os.path.join(root_path, ".env")

load_dotenv(dotenv_path=env_path, override=True)

# MAIN

DEBUG: bool = os.getenv("DEBUG").lower() == "true"
DROP_TABLES: bool = os.getenv("DROP_TABLES").lower() == "true"
ECHO_SQL: bool = os.getenv("ECHO_SQL").lower() == "true"

BOT_VERSION: str = os.getenv("BOT_VERSION")
ADMIN_ID: str = os.getenv("ADMIN_ID")
ADMIN_IDS: list[int] = [int(id) for id in os.getenv("ADMIN_IDS").split(",")]

DATABASE_URL: str = os.getenv("DATABASE_URL")
REDIS_URL: str = os.getenv("REDIS_URL")
TG_TOKEN: str = os.getenv("TG_TOKEN")

TG_LOG_TOKEN: str = os.getenv("FILES_DELETE_MODE")
TG_INFO_LOG_CHANNEL: int = int(os.getenv("FILES_DELETE_MODE"))
TG_ERROR_LOG_CHANNEL: int = int(os.getenv("FILES_DELETE_MODE"))

FILES_DELETE_MODE: str = os.getenv("FILES_DELETE_MODE")
DATA_PATH: str = os.path.join(root_path, "data")
DEFERRED_HOUR_TO_DELETE: int = int(os.getenv("DEFERRED_HOUR_TO_DELETE"))
