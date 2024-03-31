from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes

from core.settings import config
from .__addons import main_text, get_main_keyboard


def get_main_command():
    names = ["main"]

    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:      
        await update.message.reply_text(
            text=main_text,
            reply_markup=get_main_keyboard(update.message.from_user.id in config.ADMIN_IDS),
        )

    return CommandHandler(command=names, callback=command)


main_commands = [get_main_command()]
