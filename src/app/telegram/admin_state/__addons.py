from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core.settings import config


def check_is_user_admin(tg_id: int):
    if tg_id in config.ADMIN_IDS:
        return True


admin_text = "Вы в админ-панельке, {user_name}"
admin_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Добавить товар", callback_data="create_catalog"),
        ],
        [
            InlineKeyboardButton("Удалить товаров", callback_data="delete_catalog"),
        ],
        [
            InlineKeyboardButton("Изменить товар", callback_data="update_catalog"),
        ],
        [
            InlineKeyboardButton("Вернуться ↩️", callback_data="main"),
        ],

    ]
)


after_get_create_catalog_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Добавить ещё товар", callback_data="create_catalog"),
        ],
        [
            InlineKeyboardButton("В админ панель ↩️", callback_data="admin"),
        ],
    ]
)

start_update_catalogs_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Обновить данные", callback_data="update_catalogs:start:pass"),
        ],
        [
            InlineKeyboardButton("В админ панель ↩️", callback_data="admin_back")
        ],
    ]
)

def get_next_update_catalogs_message_keyboard(category_id: int, is_last: bool = False):
    end_buttons = [
        InlineKeyboardButton("Обновить ещё товар", callback_data="update_catalogs:start"),
        InlineKeyboardButton("В админ панель ↩️", callback_data="admin_back")
    ]
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Обновить имя товара", callback_data=f"update_catalogs:name:{category_id}:pass")
            ],
            [
                InlineKeyboardButton("Обновить описание товара", callback_data=f"update_catalogs:description:{category_id}:pass")
            ],
            [
                InlineKeyboardButton("Обновить картинку товара", callback_data=f"update_catalogs:image:{category_id}:pass")
            ],
            [
                InlineKeyboardButton("Обновить количество товаров", callback_data=f"update_catalogs:count:{category_id}:pass")
            ],
            [
                *([InlineKeyboardButton("Перейти дальше", callback_data="update_catalogs:start:pass")]
                if not is_last else end_buttons)
            ],
        ]   
    )

def get_back_to_catalogs_message_keyaboard(catalog_id: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Перейти дальше", callback_data="update_catalogs:start:pass")
            ],
            [
                InlineKeyboardButton("К обновлению ↩️", callback_data=f"update_catalogs:start:{catalog_id}")
            ]
        ]
    )
