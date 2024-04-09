from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла

current_file_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
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

TG_LOG_TOKEN: str = os.getenv("TG_LOG_TOKEN")
TG_INFO_LOG_CHANNEL: int = int(os.getenv("TG_INFO_LOG_CHANNEL"))
TG_ERROR_LOG_CHANNEL: int = int(os.getenv("TG_ERROR_LOG_CHANNEL"))

MAIN_IMAGE_ID: str = os.getenv("MAIN_IMAGE_ID")
CATALOG_IMAGE_ID: str = os.getenv("CATALOG_IMAGE_ID")
CART_IMAGE_ID: str = os.getenv("CART_IMAGE_ID")
ADMIN_IMAGE_ID: str = os.getenv("ADMIN_IMAGE_ID")
ABOUT_IMAGE_ID: str = os.getenv("ABOUT_IMAGE_ID")
CABINET_IMAGE_ID: str = os.getenv("CABINET_IMAGE_ID")

DEFAULT_SOLO_CATALOG_IMAGE_ID: str = os.getenv("DEFAULT_SOLO_CATALOG_IMAGE_ID")