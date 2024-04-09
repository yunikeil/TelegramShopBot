import re

from telegram import Update, LabeledPrice
from telegram.ext import filters, ConversationHandler, CommandHandler, MessageHandler, ContextTypes

from core.database import get_session
from core.settings import config

# sorry for hardcode xD
TEST_PAYMENT_PROVIDER_TOKEN =  "1744374395:TEST:479b29acbf507213f0d2"

def get_create_payment_summ_message():
    pattern = filters.TEXT and filters.Regex(r"^[0-9]+$")
    
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.message.chat_id
        title = "Пополнение баланса"
        description = "Пример пополнения счёта бота"
        payload = "Custom-Payload"
        currency = "RUB"
        price = int(update.message.text)
        prices = [LabeledPrice("Тестовое пополнение", price * 100)]
        
        if price < 10 or price > 100000:
            await update.message.reply_text("Неверная сумма пополнеия 10 <= summ <= 100000")
            return

        await context.bot.send_invoice(
            chat_id, title, description, payload, TEST_PAYMENT_PROVIDER_TOKEN, currency, prices
        )
        
        return ConversationHandler.END
    
    return MessageHandler(pattern, callback)