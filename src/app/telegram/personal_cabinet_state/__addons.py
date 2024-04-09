from telegram import InlineKeyboardButton, InlineKeyboardMarkup


about_me_keyboard_message = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Пополнить баланс", callback_data="create_payment")
        ],
        [
            InlineKeyboardButton("Вернуться ↩️", callback_data="main")
        ]
    ]
)

