from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes

from core.database import get_session
from app.services import get_user_by_tg_id, create_user
from .__addons import text_user_finded, text_user_not_finded, main_command_keyboard


def get_start_command():
    names = ["start", "help"]

    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_id =  update.message.from_user.id

        async with get_session() as db_session:
            user = await get_user_by_tg_id(db_session, user_id)
            
            if user:
                text_to_send = text_user_finded
            else:
                text_to_send = text_user_not_finded
                user = await create_user(db_session, user_id)
            
        await update.message.reply_text(text=text_to_send, reply_markup=main_command_keyboard)
        
    return CommandHandler(command=names, callback=command)


start_state_commands = [get_start_command()]
