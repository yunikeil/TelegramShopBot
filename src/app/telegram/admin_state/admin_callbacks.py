from typing import cast

from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler

from core.database import get_session
from app.services import get_catalog_by_id, update_catalog
from .__addons import (
    admin_text,
    admin_keyboard,
    check_is_user_admin,
    get_next_update_catalogs_message_keyboard,
)


# Ниже обработчики из главной admin панели
def get_create_catalog_callback():
    pattern = "^create_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text="Введите по три строки каталоги"
        )

        return "enter_create_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_delete_catalog_callback():
    pattern = "^delete_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text="delete_catalog")

        return "enter_delete_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_update_catalog_callback():
    pattern = "^update_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text="введите id каталогов на обновление, один в одной строке"
        )

        return "enter_update_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_update_catalogs_data_callback():
    pattern = r"^update_catalogs:.+:.+$"

    async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        catalogs_ids = context.user_data["catalogs_to_update"]
        if not catalogs_ids:
            await update.callback_query.edit_message_text("not catalogs there")
            return ConversationHandler.END
        
        catalog_id = update.callback_query.data.split(":")[2]
        
        if catalog_id.isdigit():
            catalog_id = int(catalog_id)
                        
        elif catalog_id == "pass":
            catalog_id = int(cast(list, context.user_data["catalogs_to_update"]).pop(0))
            
        async with get_session() as db_session:
            catalog = await get_catalog_by_id(db_session, catalog_id)
        
        await update.callback_query.edit_message_text(
            text=f"{catalog.to_text()}\n*Осталось на обновление:* `{len(catalogs_ids)}`",
            parse_mode="Markdown",
            reply_markup=get_next_update_catalogs_message_keyboard(catalog_id, is_last=len(catalogs_ids) == 0),
        )
    
    async def name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "name"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_text("Введите новоё имя...")
        return "update_calatogs_field"
        
    async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        update_type = update.callback_query.data.split(":")[1]
        match update_type:
            case "start":
                to_return = await start_callback(update, context)
            case "name":
                to_return = await name_callback(update, context)
            case _:
                to_return = None
                await update.callback_query.answer()
                print(update_type)
        
        return to_return

    return CallbackQueryHandler(base_callback, pattern)


# Ниже обработчик вернуться обратно из дополнительных admin панелей
def get_back_to_admin_callback(need_only_callback: bool = False):
    pattern = "^admin$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if update.callback_query.data == "admin_back":
            to_return = ConversationHandler.END
        else:
            to_return = None
        
        await update.callback_query.answer()
        user_id = update.callback_query.from_user.id
        username = update.callback_query.from_user.name

        if not check_is_user_admin(user_id):
            return to_return

        await update.callback_query.edit_message_text(
            text=admin_text.format(user_name=username), reply_markup=admin_keyboard
        )
        
        return to_return
    
    if need_only_callback:
        return callback
    
    return CallbackQueryHandler(callback, pattern)

def get_back_to_admin_back_callback():
    pattern = "^admin_back$"
    
    return CallbackQueryHandler(get_back_to_admin_callback(need_only_callback=True), pattern)

admin_callbacks = [get_back_to_admin_callback()]
