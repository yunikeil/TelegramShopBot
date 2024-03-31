from telegram import Update
from telegram.ext import (
    filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
)


def get_array_global_fallbacks() -> tuple[
    CommandHandler, CommandHandler, MessageHandler, CallbackQueryHandler
]:
    all_commands = []
    stop_commads = ["stop", "cancel"]
    filter = filters.ALL
    pattern = '^.*$'
    
    async def any_command_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Неизвестная команда...\ntry /stop")
        
    async def stop_command_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Выполнение сценария остановленно...")
        return ConversationHandler.END
        
    async def message_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Неизвестный текстовый формат...\ntry /stop")
    
    async def callback_fallback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text("Неизвестное нажатие кнопки...\ntry /stop")
        

    return (
        CommandHandler(all_commands, any_command_fallback),
        CommandHandler(stop_commads, stop_command_fallback),
        MessageHandler(filter, message_fallback),
        CallbackQueryHandler(callback_fallback, pattern),
    )
