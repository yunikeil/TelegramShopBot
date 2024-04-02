import re

from telegram import Update
from telegram.ext import filters, ConversationHandler, CommandHandler, MessageHandler, ContextTypes

from core.database import get_session
from app.services import update_shopping_cart
from .__addons import get_shopping_cart_back_keyboard


def get_update_shopping_cart_count_message():
    pattern = filters.TEXT and filters.Regex(r"^[0-9]+$")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        card_id = context.user_data["update_card_id"]
        offset = context.user_data["offset"]
        limit = context.user_data["limit"]
        return_data = context.user_data["return_callback_data"]
        count = int(update.message.text)
        
        async with get_session() as db_session:
            new_cart = await update_shopping_cart(db_session, card_id, update.message.from_user.id, count)

        await update.message.reply_text(text=new_cart.to_text(), parse_mode="Markdown", reply_markup=get_shopping_cart_back_keyboard(card_id, offset, limit, return_data))
        return ConversationHandler.END
        
    return MessageHandler(pattern, callback)