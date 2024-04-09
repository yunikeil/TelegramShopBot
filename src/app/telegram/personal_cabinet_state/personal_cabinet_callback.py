from telegram import Update, InputMedia
from telegram.ext import CallbackQueryHandler, ContextTypes

from core.database import get_session
from core.settings import config
from app.services import get_user_by_tg_id
from .__addons import about_me_keyboard_message


def get_personal_cabinet_callback():
    pattern = '^personal_cabinet$'

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()

        async with get_session() as db_session:
            user = await get_user_by_tg_id(db_session, update.callback_query.from_user.id)
        
        if not user:
            return
        
        await query.edit_message_media(
            media=InputMedia("photo", config.CABINET_IMAGE_ID, caption=user.to_text(), parse_mode="Markdown"),
            reply_markup=about_me_keyboard_message)
    
    return CallbackQueryHandler(callback, pattern)


def get_payemnt_callback():
    pattern = r"^create_payment$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_caption(
            caption="Введите сумму, на которую хотите пополнить"
        )
        
        return "enter_purchase_summ"

    return CallbackQueryHandler(callback, pattern)


personal_cabinet_callbacks = [get_personal_cabinet_callback()]
