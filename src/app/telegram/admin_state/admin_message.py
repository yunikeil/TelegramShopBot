import re

from telegram import Update
from telegram.ext import filters, ConversationHandler, CommandHandler, MessageHandler, ContextTypes

from core.database import get_session
from app.services import create_catalog
from .__addons import after_get_create_catalog_message_keyboard


def get_create_catalog_message():
    pattern = filters.TEXT and filters.Regex(r".+\n.+\n[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        
        if results := re.findall(r".+\n.+\n[0-9]+", user_message):
            async with get_session() as db_session:
                for result in results:
                    result = result.split("\n")
                    await create_catalog(
                        db_session, result[0], result[1], int(result[2])
                    )

        await update.message.reply_text(f"added: {len(results)} result(s), now add file, or use /skip")
        return "enter_create_catalogs_photo"

    return MessageHandler(pattern, callback)


def get_create_catalog_photo():
    pattern = filters.PHOTO
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        file = await update.message.photo[-1].get_file()
        await update.message.reply_text(f"File received!", reply_markup=after_get_create_catalog_message_keyboard)
        return ConversationHandler.END

    return MessageHandler(pattern, callback)


def get_ckip_catalog_photo():
    command = "skip"
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f"File skipped!", reply_markup=after_get_create_catalog_message_keyboard)
        return ConversationHandler.END

    return CommandHandler(command, callback)


# TODO
def get_update_catalog_message():
    pattern = filters.TEXT and filters.Regex(r".+\n.+\n[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        
        if results := re.findall(r".+\n.+\n[0-9]+", user_message):
            async with get_session() as db_session:
                for result in results:
                    result = result.split("\n")
                    await create_catalog(
                        db_session, result[0], result[1], int(result[2])
                    )

        await update.message.reply_text(f"added: {len(results)} result(s)", reply_markup=after_get_create_catalog_message_keyboard)
        return ConversationHandler.END
    
    return MessageHandler(pattern, callback)

