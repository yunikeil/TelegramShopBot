from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler

from core.telegram import get_array_global_fallbacks
from .admin_callbacks import get_create_catalog_callback, get_delete_catalog_callback, get_update_catalog_callback
from .admin_message import get_create_catalog_message, get_create_catalog_photo, get_update_catalog_message, get_ckip_catalog_photo


admin_catalog_handler = ConversationHandler(
    entry_points=[get_create_catalog_callback(), get_delete_catalog_callback(), get_update_catalog_callback()],
    states={
        "enter_create_catalogs_data": [get_create_catalog_message()],
        "enter_create_catalogs_photo": [get_create_catalog_photo(), get_ckip_catalog_photo()],
        "enter_delete_catalogs_data": [],
        "enter_update_catalogs_data": [get_update_catalog_message()],
    },
    fallbacks=get_array_global_fallbacks()
)

