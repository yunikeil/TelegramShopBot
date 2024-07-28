import socket
import urllib3
import sys

from telegram import Update
from telegram.ext import Application

from core.logging.helpers import create_logger
from core.logging.handlers import ErrorHandlerTG
from core.storage.minio_client import test_storage_connection
from core.database.session import test_pg_connection
from core.settings import config
from app.bot import handlers

logger = create_logger("telegram")


async def init_application(application: Application) -> None:
    logger.addHandler(ErrorHandlerTG())
    need_stop = False
    
    try:
        logger.info(await test_pg_connection())
        logger.info(await test_storage_connection())
    except urllib3.exceptions.MaxRetryError:
        logger.error("Unable to start bot, check the connection with MinIO")
        need_stop = True
    except socket.gaierror:
        logger.error("Unable to start bot, check the connection with PostgreSQL")
        need_stop = True
    except BaseException as ex:
        logger.exception(ex)
        need_stop = True
    
    if need_stop:
        await application.shutdown()
        sys.exit(1)


if __name__ == "__main__":
    builder = Application.builder()
    builder.token(config.TG_SHOP_TOKEN).post_init(init_application)

    application = builder.build()
    application.add_handlers(handlers)

    application.run_polling(allowed_updates=Update.ALL_TYPES)
