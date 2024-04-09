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
            InlineKeyboardButton("Изменить товар", callback_data="update_catalog"),
        ],
        [
            InlineKeyboardButton("Удалить товаров", callback_data="delete_catalog"),
        ],
        [
            InlineKeyboardButton("Получить id photo", callback_data="get_photo_id")
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

after_get_photo_id_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Получить ещё фото", callback_data="get_photo_id"),
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

back_to_admin_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("В админ панель ↩️", callback_data="admin")
        ],
    ]
)

def get_next_update_catalogs_message_keyboard(category_id: int, is_finded: bool = True, is_last: bool = False):
    update_name_button = InlineKeyboardButton("Обновить имя товара", callback_data=f"update_catalogs:name:{category_id}:pass")
    update_description_button = InlineKeyboardButton("Обновить описание товара", callback_data=f"update_catalogs:description:{category_id}:pass")
    update_price_button = InlineKeyboardButton("Обновить стоимость товара", callback_data=f"update_catalogs:price:{category_id}:pass")
    update_count_button = InlineKeyboardButton("Обновить количество товаров", callback_data=f"update_catalogs:count:{category_id}:pass")
    update_image_button = InlineKeyboardButton("Обновить картинку товара", callback_data=f"update_catalogs:photo:{category_id}:pass")
    
    buttons = []
    if is_finded:
        buttons.extend([
            [update_name_button],
            [update_description_button],
            [update_price_button],
            [update_count_button],
            [update_image_button],
        ])
    
    if not is_last:
        buttons.append([InlineKeyboardButton("Перейти дальше", callback_data="update_catalogs:start:pass")])
    else:
        buttons.append([InlineKeyboardButton("Обновить другие товары", callback_data="update_catalog"),])
        
    buttons.append([InlineKeyboardButton("В админ панель ↩️", callback_data="admin_back")])
    
    return InlineKeyboardMarkup(buttons)


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


enter_delete_catalogs_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Удалить все выбранные", callback_data="delete_catalogs:all")
        ],
        [
            InlineKeyboardButton("Удалить выборочно ➡️", callback_data="delete_catalogs:start")
        ],
        [ 
            InlineKeyboardButton("В админ панель ↩️", callback_data="admin_back")
        ],
    ]
)


def get_delete_catalogs_data_message_keyboard(is_deleted: bool = False) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            *([[
                InlineKeyboardButton("Удалить данный лот", callback_data=f"delete_catalogs:solo")
            ]]if not is_deleted else []),
            [
                InlineKeyboardButton("Перейти дальше ➡️", callback_data="delete_catalogs:start")
            ],
            [
                InlineKeyboardButton("В админ панель ↩️", callback_data="admin_back")
            ],
        ]
    )

end_delete_catalogs_message_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Удалить ещё", callback_data="delete_catalog")
        ],
        [
            InlineKeyboardButton("В админ панель ↩️", callback_data="admin")
        ]
    ]
)