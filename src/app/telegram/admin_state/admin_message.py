import re

from telegram import Update
from telegram.ext import filters, ConversationHandler, CommandHandler, MessageHandler, ContextTypes

from core.database import get_session
from app.services import create_catalog, update_catalog
from .__addons import after_get_create_catalog_message_keyboard, start_update_catalogs_message_keyboard, enter_delete_catalogs_message_keyboard, after_get_photo_id_message_keyboard, get_back_to_catalogs_message_keyaboard


def get_photo_id_message():
    pattern = filters.PHOTO
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        file_id = update.message.photo[-1].file_id
                        
        await update.message.reply_photo(
            photo=file_id,
            caption=f"file\_id: `{file_id}`",
            parse_mode="Markdown",
            reply_markup=after_get_photo_id_message_keyboard
        )
        
        return ConversationHandler.END
    
    return MessageHandler(pattern, callback)


def get_enter_create_catalogs_message():
    pattern = filters.TEXT and filters.Regex(r".+\n.+\n[0-9]+\n[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        catalog_ids: list[int] = []
        
        if results := re.findall(r".+\n.+\n[0-9]+\n[0-9]+", user_message):
            async with get_session() as db_session:
                for result in results:
                    result = result.split("\n")
                    catalog = await create_catalog(
                        db_session, result[0], result[1], int(result[2]), int(result[3])
                    )
                    catalog_ids.append(catalog.id)
        
        context.user_data["catalog_create_need_photo"] = catalog_ids
        await update.message.reply_photo(photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE" , caption=f"added: {len(catalog_ids)} result(s), now add file, or use /skip")
        return "create_catalogs_photo"

    return MessageHandler(pattern, callback)


def get_create_catalogs_photo():
    pattern = filters.PHOTO
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        file_id = update.message.photo[-1].file_id
        catalog_ids = context.user_data["catalog_create_need_photo"]
        
        async with get_session() as db_session:
            for catalog_id in catalog_ids:
                new_catalog = await update_catalog(
                    db_session, catalog_id, file_id=file_id
                )
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Файл добавлен к {len(catalog_ids)} каталогу(ам)!",
            reply_markup=after_get_create_catalog_message_keyboard
        )
        return ConversationHandler.END

    return MessageHandler(pattern, callback)


def get_ckip_catalogs_photo():
    command = "skip"
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Файлы для офферов были пропущены!", 
            reply_markup=after_get_create_catalog_message_keyboard
        )
        return ConversationHandler.END

    return CommandHandler(command, callback)


def get_enter_update_catalogs_data_message():
    pattern = filters.TEXT and filters.Regex(r"[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = list(set(re.findall(r"[0-9]+", user_message)))
        results.sort()
        context.user_data["catalogs_to_update"] = results
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"to_update queue: {len(results)} catalog(s)",
            reply_markup=start_update_catalogs_message_keyboard
        )
        return "update_catalogs_data"
    
    return MessageHandler(pattern, callback)


def get_update_calatogs_text_field_message():
    pattern = filters.TEXT and filters.Regex(r"^(?!\/).+$")

    async def name_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        catalog_id = int(context.user_data["current_catalog_id"])
        
        async with get_session() as db_session:
            new_catalog = await update_catalog(db_session, catalog_id, name=update.message.text)
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Обновлено имя: {new_catalog.name}", 
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
    
    async def description_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])
        
        async with get_session() as db_session:
            new_catalog = await update_catalog(db_session, catalog_id, description=update.message.text)
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Обновлено описание: {new_catalog.description}",
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )

    async def price_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])
        
        async with get_session() as db_session:
            new_catalog = await update_catalog(db_session, catalog_id, price=update.message.text)
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Обновлена цена: {new_catalog.price}",
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
    
    async def count_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])
        
        if update.message.text.isdigit():
            count = int(update.message.text)
        else:
            count = None
        
        async with get_session() as db_session:
            new_catalog = await update_catalog(db_session, catalog_id, count=count)

        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Обновлено количество: {new_catalog.count}",
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
    
    async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        attr_update = context.user_data["now_update_filed"]
        match attr_update:
            case "name":
                await name_callback(update, context)
            case "description":
                await description_callback(update, context)
            case "price":
                await price_callback(update, context)
            case "count":
                await count_callback(update, context)
            case _:
                pass
        
        return "update_catalogs_data"
   
    return MessageHandler(pattern, base_callback)


def get_update_catalogs_photo_message():
    pattern = filters.PHOTO
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])
        file_id = update.message.photo[-1].file_id
        
        async with get_session() as db_session:
            new_catalog = await update_catalog(
                db_session, catalog_id, file_id=file_id,
            )
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Файл для оффера был добавлен!", 
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
        
        return "update_catalogs_data"
    
    return MessageHandler(pattern, callback)


def get_skip_update_catalogs_photo_command():
    command = "skip"
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])

        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Файл для оффера был пропущен!", 
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
        
        return "update_catalogs_data"

    return CommandHandler(command, callback)


def get_clear_update_catalogs_photo_command():
    command = "clear"
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        catalog_id = int(context.user_data["current_catalog_id"])

        async with get_session() as db_session:
            new_catalog = await update_catalog(
                db_session, catalog_id, file_id=None,
            )
        
        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"Файл для оффера был удалён!", 
            reply_markup=get_back_to_catalogs_message_keyaboard(catalog_id)
        )
        
        return "update_catalogs_data"

    return CommandHandler(command, callback)


def get_enter_delete_catalogs_data_message():
    pattern = filters.TEXT and filters.Regex(r"[0-9]+")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        results: list[str] = []
        
        if results := list(set(re.findall(r"[0-9]+", user_message))):
            results.sort()
            context.user_data["catalogs_to_delete"] = results        

        await update.message.reply_photo(
            photo="AgACAgIAAxkBAAIF3GYUE504AAE1OD3RUPVpQhrNSfjNvwACH98xG89PoEggb-K0TwaieQEAAwIAA3kAAzQE",
            caption=f"to_delete added: {len(results)} result(s)", 
            reply_markup=enter_delete_catalogs_message_keyboard
        )
        return "delete_catalogs_data"

    return MessageHandler(pattern, callback)
