from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes

from core.settings import config
from .__addons import about_us_text, about_us_inline_keyboard


def get_about_us_callback():
    pattern = "^about_us$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=about_us_text, reply_markup=about_us_inline_keyboard
        )

    return CallbackQueryHandler(callback, pattern)


def get_bot_version():
    pattern = "^bot_version$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer(
            text=f"Current version: {config.BOT_VERSION}", cache_time=10, show_alert=True
        )

    return CallbackQueryHandler(callback, pattern)


about_us_callbacks = [get_about_us_callback(), get_bot_version()]
