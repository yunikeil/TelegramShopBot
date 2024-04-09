from telegram import InlineKeyboardButton, InlineKeyboardMarkup



return_to_me_keyboard_message = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Вернуться ↩️", callback_data="personal_cabinet")
        ]
    ]
)
