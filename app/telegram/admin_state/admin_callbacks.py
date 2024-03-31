from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from .__addons import check_is_user_admin, admin_text, admin_keyboard


# Ниже обработчики из главной admin панели 
def get_create_catalog_callback():
    pattern = '^create_catalog$'
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="Введите по три строки каталоги")
        
        return "enter_create_catalogs_data"
    
    return CallbackQueryHandler(callback, pattern)


def get_delete_catalog_callback():
    pattern = '^delete_catalog$'
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="delete_catalog")
        
        return "enter_delete_catalogs_data"
    
    return CallbackQueryHandler(callback, pattern)


def get_update_catalog_callback():
    pattern = '^update_catalog$'
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="update_catalog")
        
        return "enter_update_catalogs_data"
    
    return CallbackQueryHandler(callback, pattern)


# Ниже обработчик вернуться обратно из дополнительных admin панелей
def get_back_to_admin_callback():
    pattern = '^admin$'
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.name

        if not check_is_user_admin(user_id):
            return

        await update.callback_query.edit_message_text(
            text=admin_text.format(user_name=username), reply_markup=admin_keyboard
        )

    return CallbackQueryHandler(callback, pattern)



admin_callbacks = [get_back_to_admin_callback()]
