from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes
import telegram

from core.database import get_session
from app.services import create_shopping_cart, get_shopping_cart_count, get_all_shopping_carts, get_shopping_cart_by_ids, delete_shopping_cart
from app.models import ShoppingCart
from .__addons import get_offset_limit_buttons, get_shopping_cart_back_keyboard


def get_add_to_shopping_cart_callback():
    pattern = r"^add_shopping_cart:\d+$"
        
    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, catalog_id = update.callback_query.data.split(":")
        
        cart: ShoppingCart | None = None
        
        async with get_session() as db_session:
            c_cart = await get_shopping_cart_by_ids(db_session, int(catalog_id), update.callback_query.from_user.id)
            
            if c_cart:
                await update.callback_query.answer("Товар уже был добавлен в корзину")
                return
            
            cart = await create_shopping_cart(db_session, int(catalog_id), update.callback_query.from_user.id, 1)
        
        await update.callback_query.answer("Товар добавлен в корзину")
    
    return CallbackQueryHandler(callback, pattern)


def get_shopping_cart_callback():
    pattern = r"^(shopping_cart|delete_shopping_cart):-?\d+:-?\d+:-?\d+$"

    async def callback_delete(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _, _, _, catalog_id = update.callback_query.data.split(":")
        
        cart: ShoppingCart | None = None
        
        async with get_session() as db_session:
            c_cart = await get_shopping_cart_by_ids(db_session, int(catalog_id), update.callback_query.from_user.id)
            
            if not c_cart:
                await update.callback_query.answer("Товар не был найден в корзине")
                await base_callback(update, context, True)
                
            cart = await delete_shopping_cart(db_session, int(catalog_id), update.callback_query.from_user.id)
                    
        await update.callback_query.answer("Товар удалён из корзины")
        await base_callback(update, context, True)
    
    async def base_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, is_answered: bool = False):
        if not is_answered:
            await update.callback_query.answer()
        
        _, offset, limit, _ = update.callback_query.data.split(":")
                
        if offset == '-1' or limit == '-1':
            return
                
        carts: list[ShoppingCart] | None = None

        async with get_session() as db_session:
            count_carts = await get_shopping_cart_count(db_session, int(update.callback_query.from_user.id)) 
            carts = await get_all_shopping_carts(db_session, int(update.callback_query.from_user.id), int(offset), int(limit))

        if not carts:
            text = "no carts no carts no carts"
        else:
            text = "carts in bd carts in bd carts in bd"
                
        try: # После можно будет перекинуть в общие хендлеры
            await update.callback_query.edit_message_text(
                text=text,
                reply_markup=InlineKeyboardMarkup(
                    [
                        *[catalog.to_button(int(offset), int(limit)) for catalog in carts],
                        *get_offset_limit_buttons(int(offset), int(limit), count_carts),
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
    pattern = r"^solo_shopping_cart:\d+:-?\d+:-?\d+$"

    async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.callback_query.answer()
        _, cart_id, offset, limit = update.callback_query.data.split(":")
        
        if offset == '-1' or limit == '-1':
            return

        cart: ShoppingCart | None = None

        async with get_session() as db_session:
            cart = await get_shopping_cart_by_ids(db_session, int(cart_id), update.callback_query.from_user.id)

        if not cart:
            text = "cant fint this cart"
        else:
            text = cart.to_text()
        
        await update.callback_query.edit_message_text(text, parse_mode="Markdown", reply_markup=get_shopping_cart_back_keyboard(cart_id, int(offset), int(limit)))

    return CallbackQueryHandler(callback, pattern)


shopping_cart_callbacks = [get_add_to_shopping_cart_callback(), get_shopping_cart_callback(), get_shopping_cart_solo_callback()]

