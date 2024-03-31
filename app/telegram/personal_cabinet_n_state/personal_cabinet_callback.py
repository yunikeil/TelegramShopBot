from telegram import Update
from telegram.ext import CallbackQueryHandler, ContextTypes


def get_personal_cabinet_callback():
    pattern = '^personal_cabinet$'

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Parses the CallbackQuery and updates the message text."""
        query = update.callback_query

        # CallbackQueries need to be answered, even if no notification to the user is needed
        # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
        await query.answer()

        await query.edit_message_text(text=f"Selected option: {query.data}")
    
    return CallbackQueryHandler(callback, pattern)


personal_cabinet_callbacks = [get_personal_cabinet_callback()]
