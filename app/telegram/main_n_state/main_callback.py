from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from core.settings import config
from core.database import get_session
from app.services import get_user_by_tg_id
from .__addons import main_text, get_main_keyboard


def get_main_callback():
    pattern = "^main$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()

        await update.callback_query.edit_message_text(
            text=main_text,
            reply_markup=get_main_keyboard(update.callback_query.from_user.id in config.ADMIN_IDS),
        )

    return CallbackQueryHandler(callback, pattern)


main_callbacs = [get_main_callback()]
