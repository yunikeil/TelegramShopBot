from dotenv import load_dotenv
import os

# Загрузка переменных из .env файла

current_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(os.path.dirname(current_file_path) , ".env")

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
