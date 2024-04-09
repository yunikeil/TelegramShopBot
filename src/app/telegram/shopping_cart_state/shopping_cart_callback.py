from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, InputMedia
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import telegram
import sqlalchemy

from core.database import get_session
from core.settings import config
from app.services import (
    create_shopping_cart,
    get_shopping_cart_count,
    get_all_shopping_carts,
    get_shopping_cart_by_ids,
    delete_shopping_cart,
    update_shopping_cart,
    get_catalog_by_id,
)
from app.models import ShoppingCart
from .__addons import get_offset_limit_buttons, get_shopping_cart_back_keyboard


def get_add_to_shopping_cart_callback():
    pattern = r"^add_shopping_cart:\d+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, catalog_id = update.callback_query.data.split(":")

        cart: ShoppingCart | None = None

        async with get_session() as db_session:
            c_cart = await get_shopping_cart_by_ids(
                db_session, int(catalog_id), update.callback_query.from_user.id
            )

            if c_cart:
                await update.callback_query.answer("Товар уже был добавлен в корзину")
                return

            cart = await create_shopping_cart(
                db_session, int(catalog_id), update.callback_query.from_user.id, 1
            )

        await update.callback_query.answer("Товар добавлен в корзину")

    return CallbackQueryHandler(callback, pattern)


def get_shopping_cart_callback():
    pattern = r"^(shopping_cart|delete_shopping_cart):-?\d+:-?\d+:-?\d+;.+$"

    async def callback_delete(
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        base_callback_data, return_callback_data = update.callback_query.data.split(";")
        _, _, _, catalog_id = base_callback_data.split(":")

        cart: ShoppingCart | None = None

        async with get_session() as db_session:
            c_cart = await get_shopping_cart_by_ids(
                db_session, int(catalog_id), update.callback_query.from_user.id
            )

            if not c_cart:
                await update.callback_query.answer("Товар не был найден в корзине")
                await base_callback(update, context, True)

            cart = await delete_shopping_cart(
                db_session, int(catalog_id), update.callback_query.from_user.id
            )

        await update.callback_query.answer("Товар удалён из корзины")
        await base_callback(update, context, True)

    async def base_callback(
        update: Update, context: ContextTypes.DEFAULT_TYPE, is_answered: bool = False
    ):
        if not is_answered:
            await update.callback_query.answer()

        base_callback_data, return_callback_data = update.callback_query.data.split(";")
        _, offset, limit, _ = base_callback_data.split(":")

        if offset == "-1" or limit == "-1":
            return

        carts: list[ShoppingCart] | None = None

        async with get_session() as db_session:
            count_carts = await get_shopping_cart_count(
                db_session, int(update.callback_query.from_user.id)
            )
            carts = await get_all_shopping_carts(
                db_session,
                int(update.callback_query.from_user.id),
                int(offset),
                int(limit),
            )

        if not carts:
            text = "no carts no carts no carts"
        else:
            text = "carts in bd carts in bd carts in bd"

        try:  # После можно будет перекинуть в общие хендлеры
            await update.callback_query.edit_message_media(
                media=InputMedia("photo", config.CART_IMAGE_ID, caption=text, parse_mode="Markdown"),
                reply_markup=InlineKeyboardMarkup(
                    [
                        *[
                            catalog.to_button(
                                int(offset), int(limit), return_to=return_callback_data
                            )
                            for catalog in carts
                        ],
                        *get_offset_limit_buttons(
                            int(offset),
                            int(limit),
                            count_carts,
                            return_to=return_callback_data,
                        ),
                    ]
                ),
            )
        except telegram.error.BadRequest:
            pass

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if "delete" in update.callback_query.data:
            await callback_delete(update, context)
        else:
            await base_callback(update, context)

    return CallbackQueryHandler(callback, pattern)


def get_shopping_cart_solo_callback():
    # Отвечает за обработку единичных катологов
    pattern = r"^solo_shopping_cart:\d+:-?\d+:-?\d+;.+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        base_callback_data, return_callback_data = update.callback_query.data.split(";")
        _, cart_id, offset, limit = base_callback_data.split(":")

        if offset == "-1" or limit == "-1":
            return

        cart: ShoppingCart | None = None

        async with get_session() as db_session:
            cart = await get_shopping_cart_by_ids(
                db_session, int(cart_id), update.callback_query.from_user.id
            )

        if not cart:
            text = "cant fint this cart"
        else:
            text = cart.to_text()

        await update.callback_query.edit_message_media(
            media=InputMedia(
                media_type="photo",
                media=cart.catalog.file_unique_tg_id
                if cart.catalog.file_unique_tg_id
                else config.DEFAULT_SOLO_CATALOG_IMAGE_ID,
                caption=text,
                parse_mode="Markdown",
            ),
            reply_markup=get_shopping_cart_back_keyboard(
                cart_id, int(offset), int(limit), return_to=return_callback_data
            ),
        )

    return CallbackQueryHandler(callback, pattern)


def get_update_shopping_cart_count_mp_callback():
    pattern = r"^count_shopping_cart:[0-9]+:.+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        base_callback_data, return_callback_data = update.callback_query.data.split(";")
        _, offset, limit, cart_id, action = base_callback_data.split(":")

        async with get_session() as db_session:
            card = await get_shopping_cart_by_ids(
                db_session, int(cart_id), update.callback_query.from_user.id
            )
            if not card:
                await update.callback_query.answer("Нет товара в корзине")
                return

            count = card.count + 1 if action == "plus" else card.count - 1
            if count > len(card.catalog.products):
                await update.callback_query.answer("Нельзя выбрать больше, чем имеется.")
                return

            try:
                new_card = await update_shopping_cart(
                    db_session, int(cart_id), update.callback_query.from_user.id, count
                )
            except sqlalchemy.exc.IntegrityError:
                await update.callback_query.answer("Неверное количество...")
                return

        await update.callback_query.answer()
        await update.callback_query.edit_message_media(
            media=InputMedia(
                media_type="photo",
                media=new_card.catalog.file_unique_tg_id
                if new_card.catalog.file_unique_tg_id
                else config.DEFAULT_SOLO_CATALOG_IMAGE_ID,
                caption=new_card.to_text(),
                parse_mode="Markdown",
            ),
            reply_markup=get_shopping_cart_back_keyboard(
                cart_id, offset, limit, return_callback_data
            ),
        )

    return CallbackQueryHandler(callback, pattern)


def get_update_shopping_cart_count_callback():
    pattern = r"^update_shopping_cart:\d+:-?\d+:-?\d+;.+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.callback_query.answer()
        base_callback_data, return_callback_data = update.callback_query.data.split(";")
        _, offset, limit, cart_id = base_callback_data.split(":")

        context.user_data["update_card_id"] = int(cart_id)
        context.user_data["offset"] = offset
        context.user_data["limit"] = limit
        context.user_data["return_callback_data"] = return_callback_data

        await update.callback_query.edit_message_caption("Введите новое количество...")
        return "update_shopping_cart_count"

    return CallbackQueryHandler(callback, pattern)


shopping_cart_callbacks = [
    get_add_to_shopping_cart_callback(),
    get_shopping_cart_callback(),
    get_shopping_cart_solo_callback(),
    get_update_shopping_cart_count_mp_callback(),
]
