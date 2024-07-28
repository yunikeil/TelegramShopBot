import re


import sqlalchemy
from telegram import Update
from telegram.ext import (
    filters,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    ContextTypes,
)

from core.database import context_get_pg_session
from core.settings import config
from app.services import get_shopping_cart_by_ids, update_shopping_cart
from .__addons import get_shopping_cart_back_keyboard


def get_update_shopping_cart_count_message():
    pattern = filters.TEXT and filters.Regex(r"^[0-9]+$")

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        cart_id = context.user_data["update_card_id"]
        offset = context.user_data["offset"]
        limit = context.user_data["limit"]
        return_data = context.user_data["return_callback_data"]
        count = int(update.message.text)

        async with context_get_pg_session() as db_session:
            cart = await get_shopping_cart_by_ids(
                db_session, int(cart_id), update.message.from_user.id
            )

            if not cart:
                await update.message.reply_photo(
                    photo=cart.catalog.file_unique_tg_id
                    if cart.catalog.file_unique_tg_id
                    else settings.DEFAULT_SOLO_CATALOG_IMAGE_ID,
                    caption="```Ошибка Нет товара в корзине```\n" + cart.to_text(),
                    parse_mode="Markdown",
                    reply_markup=get_shopping_cart_back_keyboard(
                        cart_id, offset, limit, return_data
                    ),
                )

                return ConversationHandler.END

            if count > len(cart.catalog.products):
                await update.message.reply_photo(
                    photo=cart.catalog.file_unique_tg_id
                    if cart.catalog.file_unique_tg_id
                    else settings.DEFAULT_SOLO_CATALOG_IMAGE_ID,
                    caption="```Ошибка Нельзя выбрать больше, чем имеется.```\n" + cart.to_text(),
                    parse_mode="Markdown",
                    reply_markup=get_shopping_cart_back_keyboard(
                        cart_id, offset, limit, return_data
                    ),
                )
                return ConversationHandler.END

            try:
                new_cart = await update_shopping_cart(
                    db_session, cart_id, update.message.from_user.id, count
                )
            except sqlalchemy.exc.IntegrityError:
                await update.message.reply_photo(
                    photo=cart.catalog.file_unique_tg_id
                    if cart.catalog.file_unique_tg_id
                    else settings.DEFAULT_SOLO_CATALOG_IMAGE_ID,
                    caption="```Ошибка Неверное количество...```\n" + cart.to_text(),
                    parse_mode="Markdown",
                    reply_markup=get_shopping_cart_back_keyboard(
                        cart_id, offset, limit, return_data
                    ),
                )

                return ConversationHandler.END

        await update.message.reply_photo(
            photo=new_cart.catalog.file_unique_tg_id
            if new_cart.catalog.file_unique_tg_id
            else settings.DEFAULT_SOLO_CATALOG_IMAGE_ID,
            caption=new_cart.to_text(),
            parse_mode="Markdown",
            reply_markup=get_shopping_cart_back_keyboard(
                cart_id, offset, limit, return_data
            ),
        )
        return ConversationHandler.END

    return MessageHandler(pattern, callback)
