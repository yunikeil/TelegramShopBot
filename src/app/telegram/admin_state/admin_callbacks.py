from typing import cast

import telegram
from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler

from core.database import get_session
from app.services import get_catalog_by_id, delete_catalog
from .__addons import (
    admin_text,
    admin_keyboard,
    end_delete_catalogs_message_keyboard,
    back_to_admin_message_keyboard,
    check_is_user_admin,
    get_next_update_catalogs_message_keyboard,
    get_delete_catalogs_data_message_keyboard,
)


# Ниже обработчики из главной admin панели
def get_create_catalog_callback():
    pattern = "^create_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_caption(
            caption="Введите данные по задданному паттерну:\n- Name\n- Description\n- Price\n- Count",
            parse_mode="Markdown"
        )

        return "enter_create_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_delete_catalog_callback():
    pattern = "^delete_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_caption(caption="Введите id офферов для удаления...")

        return "enter_delete_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_update_catalog_callback():
    pattern = "^update_catalog$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_caption(
            caption="введите id каталогов на обновление, один в одной строке"
        )

        return "enter_update_catalogs_data"

    return CallbackQueryHandler(callback, pattern)


def get_update_catalogs_data_callback():
    pattern = r"^update_catalogs:.+:.+$"

    async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalogs_ids = context.user_data["catalogs_to_update"]        
        catalog_id = update.callback_query.data.split(":")[2]
        
        if catalog_id.isdigit():
            catalog_id = int(catalog_id)
        
        elif len(cast(list, context.user_data["catalogs_to_update"])) == 0:
            await update.callback_query.edit_message_caption("Больше нечего обновлять", reply_markup=back_to_admin_message_keyboard)
            return ConversationHandler.END

        elif catalog_id == "pass":
            catalog_id = int(cast(list, context.user_data["catalogs_to_update"]).pop(0))
                
        async with get_session() as db_session:
            catalog = await get_catalog_by_id(db_session, catalog_id)
        
        
        if not catalog:
            is_finded = False
            text_to_send = f"Не удалось найти каталог с id: `{catalog_id}`"
        else:
            is_finded = True
            text_to_send = f"{catalog.to_text()}\n*Осталось на обновление:* `{len(catalogs_ids)}`"
            
        await update.callback_query.edit_message_caption(
            caption=text_to_send,
            parse_mode="Markdown",
            reply_markup=get_next_update_catalogs_message_keyboard(
                catalog_id, is_finded=is_finded, is_last=len(catalogs_ids) == 0
            ),
        )
    
    async def name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "name"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_caption("Введите новоё имя...")
        return "update_calatogs_field"
    
    async def description_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "description"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_caption("Введите новоё описание...")
        return "update_calatogs_field"

    async def price_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "price"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_caption("Введите новую цену...")
        return "update_calatogs_field"
        
    async def count_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "count"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_caption("Введите новоё количество...")
        return "update_calatogs_field"
    
    async def photo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = update.callback_query.data.split(":")[2]
        context.user_data["now_update_filed"] = "count"
        context.user_data["current_catalog_id"] = catalog_id
        await update.callback_query.edit_message_caption("Прикрепите фотографию...\n/skip - для пропуска\n/clear - для удаления фото")
        return "update_catalogs_photo"

    async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        update_type = update.callback_query.data.split(":")[1]
        await update.callback_query.answer()
        match update_type:
            case "start":
                to_return = await start_callback(update, context)
            case "name":
                to_return = await name_callback(update, context)
            case "description":
                to_return = await description_callback(update, context)
            case "price":
                to_return = await price_callback(update, context)
            case "count":
                to_return = await count_callback(update, context)
            case "photo":
                to_return = await photo_callback(update, context)
            case _:
                to_return = None
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

        await update.callback_query.edit_message_caption(
            caption=admin_text.format(user_name=username), reply_markup=admin_keyboard
        )
        
        return to_return
    
    if need_only_callback:
        return callback
    
    return CallbackQueryHandler(callback, pattern)


def get_back_to_admin_back_callback():
    pattern = "^admin_back$"
    
    return CallbackQueryHandler(get_back_to_admin_callback(need_only_callback=True), pattern)


def get_delete_catalogs_data_callback():
    pattern = r"^delete_catalogs:.+$"

    async def start_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalogs_to_delete_ids = context.user_data["catalogs_to_delete"]
        
        if not catalogs_to_delete_ids:
            await update.callback_query.edit_message_caption("Больше нечего удалять", reply_markup=back_to_admin_message_keyboard)
            return ConversationHandler.END
        
        catalog_id = int(cast(list, catalogs_to_delete_ids).pop(0))
        context.user_data["solo_catalog_id_to_delete"] = catalog_id 
        
        async with get_session() as db_session:
            catalog_to_delete = await get_catalog_by_id(db_session, catalog_id)
        
        if not catalog_to_delete:
            await update.callback_query.edit_message_caption(text=f"Нет оффера с id {catalog_id}", reply_markup=get_delete_catalogs_data_message_keyboard(True))
        else:
            await update.callback_query.edit_message_caption(text=f"*Выставлено на удаление:*\n{catalog_to_delete.to_text()}\n*Осталось удалить:* {len(catalogs_to_delete_ids)}", parse_mode="Markdown", reply_markup=get_delete_catalogs_data_message_keyboard())

    async def delete_all_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalogs_to_delete_ids = context.user_data["catalogs_to_delete"]

        if not catalogs_to_delete_ids:
            await update.callback_query.edit_message_caption("Больше нечего удалять", reply_markup=back_to_admin_message_keyboard)
            return ConversationHandler.END

        deleted_catalogs = [] # можно написать и лучше, но мне лень
        # Да так то вообще многое можно переписать, но не за 5к, камон ахах
        async with get_session() as db_session:
            for catalog_id in catalogs_to_delete_ids:
                deleted_catalog = await delete_catalog(db_session, int(catalog_id))
                
                if deleted_catalog:
                    deleted_catalogs.append(deleted_catalog.id)
            
        await update.callback_query.edit_message_caption(f"Удалено {len(deleted_catalogs)} офферов", reply_markup=end_delete_catalogs_message_keyboard)
        return ConversationHandler.END
        
    async def delete_solo_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["solo_catalog_id_to_delete"])
        catalogs_to_delete_ids = context.user_data["catalogs_to_delete"]
        
        async with get_session() as db_session:
            deleted_catalog = await delete_catalog(db_session, catalog_id)

        await update.callback_query.edit_message_caption(f"*Удалено:*\n{deleted_catalog.to_text()}\n*Осталось удалить:* {len(catalogs_to_delete_ids)}", parse_mode="Markdown", reply_markup=get_delete_catalogs_data_message_keyboard(True))
        
    async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        type_deletion = update.callback_query.data.split(":")[1]
        await update.callback_query.answer()
                
        match type_deletion:
            case "start":
                to_return = await start_callback(update, context)
            case "all":
                to_return = await delete_all_callback(update, context)
            case "solo":
                to_return = await delete_solo_callback(update, context)
            case _:
                to_return = None
        
        return to_return
        
    return CallbackQueryHandler(base_callback, pattern)


admin_callbacks = [get_back_to_admin_callback()]
