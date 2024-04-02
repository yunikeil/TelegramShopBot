from telegram import Update
from telegram.ext import Application

from core.logging.helpers import create_logger
from core.settings import config
from core.database import init_models
from app import bot_handlers


tg_logger = create_logger("telegram")

"""
Товар 1
Ооооооооочень длинное описааание товара 1, но это не точно...
50
Товар 2
Ооооооооочень длинное описааание товара 2, но это не точно...
50
Товар 3
Ооооооооочень длинное описааание товара 3, но это не точно...
50
Товар 4
Ооооооооочень длинное описааание товара 4, но это не точно...
50
Товар 5
Ооооооооочень длинное описааание товара 5, но это не точно...
50
Товар 6
Ооооооооочень длинное описааание товара 6, но это не точно...
50
"""

async def init_application(application: Application) -> None:
    await init_models()
    
    ...
    

if __name__ == "__main__":
    builder = Application.builder()
    builder.token(config.TG_TOKEN).post_init(init_application)
    
    application = builder.build()
    application.add_handlers(bot_handlers)
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)
