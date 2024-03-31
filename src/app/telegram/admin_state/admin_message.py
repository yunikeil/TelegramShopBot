import re

from telegram import Update
from telegram.ext import filters, ConversationHandler, MessageHandler, ContextTypes

from core.database import get_session
from app.services import create_catalog
from .__addons import after_get_create_catalog_message_keyboard


def get_create_catalog_message():
    pattern = filters.TEXT and filters.Regex(r"\w+\n\w+\n[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        
        if results := re.findall(r"\w+\n\w+\n[0-9]+", user_message):
            async with get_session() as db_session:
                for result in results:
                    result = result.split("\n")
                    await create_catalog(
                        db_session, result[0], result[1], int(result[2])
                    )

        await update.message.reply_text(f"added: {len(results)} result(s)", reply_markup=after_get_create_catalog_message_keyboard)
        return ConversationHandler.END

    return MessageHandler(pattern, callback)


# TODO
def get_update_catalog_message():
    pattern = filters.TEXT and filters.Regex(r"\w+\n\w+\n[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        
        if results := re.findall(r"\w+\n\w+\n[0-9]+", user_message):
            async with get_session() as db_session:
                for result in results:
                    result = result.split("\n")
                    await create_catalog(
                        db_session, result[0], result[1], int(result[2])
                    )

        await update.message.reply_text(f"added: {len(results)} result(s)", reply_markup=after_get_create_catalog_message_keyboard)
        return ConversationHandler.END
    
    return MessageHandler(pattern, callback)

