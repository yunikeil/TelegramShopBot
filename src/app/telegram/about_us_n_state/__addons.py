from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from core.settings import config


about_us_text = "Мы магазин такой то такой, занимаемся долгое время тем то тем. \
Иммеем большой выбор товаров на любой вкус и цвет..."

about_us_inline_keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Связаться с администрацией",
                url=f"https://t.me/{config.ADMIN_ID}",
            ),
        ],
        [
            InlineKeyboardButton("Версия бота", callback_data="bot_version"),
        ],
        [
            InlineKeyboardButton("Вернуться ↩️", callback_data="main"),
        ],
    ]
)
