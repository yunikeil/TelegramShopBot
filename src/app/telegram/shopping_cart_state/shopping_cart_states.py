from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from core.telegram import get_array_global_fallbacks
from .shopping_cart_callback import get_update_shopping_cart_count_callback
from .shopping_cart_message import get_update_shopping_cart_count_message

shopping_cart_handler = ConversationHandler(
    entry_points=[get_update_shopping_cart_count_callback()],
    states={"update_shopping_cart_count": [get_update_shopping_cart_count_message()],},
    fallbacks=[*get_array_global_fallbacks()],
)
