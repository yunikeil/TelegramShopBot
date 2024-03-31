from telegram import InlineKeyboardButton, InlineKeyboardMarkup


main_text = "Добро пожаловать в главное меню бота! Выберите интересующий вас раздел"


def get_main_keyboard(is_admin: bool):
    keyboard = [
        [
            InlineKeyboardButton("Каталог товаров", callback_data="catalog:0:10"),
        ],
        [
            InlineKeyboardButton("Корзина товаров", callback_data="shopping_cart:0:10:0"),
        ],
        [
            InlineKeyboardButton("О нас", callback_data="about_us"),
            InlineKeyboardButton("Личный кабинет", callback_data="personal_cabinet"),
        ],
    ]
    if is_admin:
        keyboard.insert(
            2,
            [
                InlineKeyboardButton(
                    "Панель админа", callback_data=f"admin"
                )
            ],
        )

    return InlineKeyboardMarkup(keyboard)
