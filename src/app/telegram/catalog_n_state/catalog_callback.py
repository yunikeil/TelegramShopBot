import telegram
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import filters, CallbackQueryHandler, ContextTypes

from core.database import get_session
from app.services import get_all_catalogs, get_catalog_by_id, get_catalogs_count
from app.models import Catalog
from .__addons import get_offset_limit_buttons, get_catalog_back_keyboard


def get_catalog_callback():
    pattern = r"^catalog:-?\d+:-?\d+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        _, offset, limit = update.callback_query.data.split(":")
                
        if offset == '-1' or limit == '-1':
            return
                
        catalogs: list[Catalog] | None = None

        async with get_session() as db_session:
            count_catalogs = await get_catalogs_count(db_session) 
            catalogs = await get_all_catalogs(db_session, int(offset), int(limit))

        if not catalogs:
            text = "no offers no offers no offers"
        else:
            text = "offers in bd offers in bd offers in bd"

        try: # После можно будет перекинуть в общие хендлеры
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        *[catalog.to_button(int(offset), int(limit)) for catalog in catalogs],
                        *get_offset_limit_buttons(int(offset), int(limit), count_catalogs),
                    ]
                ),
            )
        except telegram.error.BadRequest:
            pass
        

    return CallbackQueryHandler(callback, pattern)


def get_catalog_solo_callback():
    # Отвечает за обработку единичных катологов
    pattern = r"^catalog:\d+:-?\d+:-?\d+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        _, catalog_id, offset, limit = update.callback_query.data.split(":")
        
        if offset == '-1' or limit == '-1':
            return

        catalog: Catalog | None = None

        async with get_session() as db_session:
            catalog = await get_catalog_by_id(db_session, int(catalog_id))

        if not catalog:
            text = "cant fint this catalog"
        else:
            text = catalog.to_text()
        
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=get_catalog_back_keyboard(catalog_id, int(offset), int(limit)))

    return CallbackQueryHandler(callback, pattern)


catalog_callbacks = [get_catalog_callback(), get_catalog_solo_callback()]
