from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_offset_limit_buttons(current_offset: int, current_limit: int, cart_count: int, return_to: str = "main"):   
    previous_offset = max(0, current_offset - current_limit)
    next_offset = max(0, current_offset + current_limit)
            
    is_first_page = current_offset == 0
    is_last_page = current_offset + current_limit >= cart_count
       
    return [
        [
            InlineKeyboardButton("⏪" if not is_first_page else "⏪❌", callback_data=f"shopping_cart:{0}:{10}:0;{return_to}" if not is_first_page else f"shopping_cart:-1:-1:0;{return_to}"),
            InlineKeyboardButton("◀️" if not is_first_page else "⬅️❌", callback_data=f"shopping_cart:{previous_offset}:{current_limit}:0;{return_to}" if not is_first_page else f"shopping_cart:-1:-1:0;{return_to}"),
            InlineKeyboardButton("🔄️", callback_data=f"shopping_cart:{current_offset}:{current_limit}:0;{return_to}"),
            InlineKeyboardButton("▶️" if not is_last_page else "❌➡️", callback_data=f"shopping_cart:{next_offset}:{current_limit}:0;{return_to}" if not is_last_page else f"shopping_cart:-1:-1:0;{return_to}"),
            InlineKeyboardButton("⏩" if not is_last_page else "❌⏩", callback_data=f"shopping_cart:{cart_count - cart_count % current_limit}:{current_limit}:0;{return_to}" if not is_last_page else f"shopping_cart:-1:-1:0;{return_to}")
        ],
        [
            InlineKeyboardButton("Вернуться ↩️", callback_data=return_to)
        ]
    ]


def get_shopping_cart_back_keyboard(cart_id: int, current_offset: int, current_limit: int, return_to: str = "main"):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Изменить количество", callback_data=f"update_shopping_cart:{cart_id}")
            ],
            [
                InlineKeyboardButton("Удалить из корзины", callback_data=f"delete_shopping_cart:{current_offset}:{current_limit}:{cart_id}")
            ],
            [
                InlineKeyboardButton("Вернуться ↩️", callback_data=f"shopping_cart:{current_offset}:{current_limit}:0;{return_to}")
            ]
        ]
    )
