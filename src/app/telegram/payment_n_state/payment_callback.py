from telegram import LabeledPrice, ShippingOption, Update, InputMedia
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    filters,
)
from core.settings import config
from core.database import get_session
from app.services import get_user_by_tg_id, update_user
from .__addons import return_to_me_keyboard_message


async def precheckout_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.pre_checkout_query
    is_user_data_ok = False
    is_query_invoice_payload_ok = False
    if query.invoice_payload == "Custom-Payload":
        is_query_invoice_payload_ok = True
    
    async with get_session() as db_session:
        old_user = await get_user_by_tg_id(db_session, query.from_user.id)
        if old_user:
            is_user_data_ok = True

        if is_user_data_ok and is_query_invoice_payload_ok:
            user = await update_user(
                db_session,
                query.from_user.id,
                balance=old_user.balance + query.total_amount
            )
            await query.answer(ok=True)

            return
    
    await query.answer(ok=False, error_message="Что-то пошло не так, вероятно сообщение является устаревшим")


async def successful_payment_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_photo(config.DEFAULT_SOLO_CATALOG_IMAGE_ID, "Спасибо за пополнение средств!", reply_markup=return_to_me_keyboard_message)


payment_callbacks = [
    MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_callback),
    PreCheckoutQueryHandler(precheckout_callback)
]
