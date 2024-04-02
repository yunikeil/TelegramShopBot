from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)

from core.telegram import get_array_global_fallbacks
from .admin_callbacks import (
    get_create_catalog_callback,
    get_delete_catalog_callback,
    get_update_catalog_callback,
    get_update_catalogs_data_callback,
    get_back_to_admin_back_callback,
    get_delete_catalogs_data_callback,
)
from .admin_message import (
    get_enter_create_catalogs_message,
    get_create_catalogs_photo,
    get_enter_update_catalogs_data_message,
    get_ckip_catalogs_photo,
    get_update_calatogs_text_field_message,
    get_enter_delete_catalogs_data_message,
    get_update_catalogs_photo_message,
    get_skip_update_catalogs_photo_command,
    get_clear_update_catalogs_photo_command,
)


admin_catalog_handler = ConversationHandler(
    entry_points=[
        get_create_catalog_callback(),
        get_update_catalog_callback(),
        get_delete_catalog_callback(),
    ],
    states={
        "enter_create_catalogs_data": [get_enter_create_catalogs_message()],
        "create_catalogs_photo": [get_create_catalogs_photo(), get_ckip_catalogs_photo()],
        "enter_update_catalogs_data": [get_enter_update_catalogs_data_message()],
        "update_catalogs_data": [get_update_catalogs_data_callback()],
        "update_calatogs_field": [get_update_calatogs_text_field_message()], # need fix cala...
        "update_catalogs_photo": [get_update_catalogs_photo_message(), get_skip_update_catalogs_photo_command(), get_clear_update_catalogs_photo_command()],
        "enter_delete_catalogs_data": [get_enter_delete_catalogs_data_message()],
        "delete_catalogs_data": [get_delete_catalogs_data_callback()],
    },
    fallbacks=[get_back_to_admin_back_callback(), get_update_catalog_callback(), *get_array_global_fallbacks()],
)
