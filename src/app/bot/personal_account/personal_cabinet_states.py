from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from core.telegram import get_array_global_fallbacks
from .personal_cabinet_callback import get_payemnt_callback
from .personal_cabinet_message import get_create_payment_summ_message


personal_cabinet_handler = ConversationHandler(
    entry_points=[
        get_payemnt_callback()
    ],
    states={
        "enter_purchase_summ": [get_create_payment_summ_message()]
    },
    fallbacks=[*get_array_global_fallbacks()],
)
