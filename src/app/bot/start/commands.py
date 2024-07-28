from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, ContextTypes

from core.database import provide_pg_session
from app.services import get_user_by_tg_id, create_user


from telegram import ReplyKeyboardMarkup



text_user_not_finded = \
"""
Добро пожаловать! Это тестовая версия.
Для начала работы используйте /main.
Тут возможно будет описание его возможностей.
"""

text_user_finded = \
"""
С возвращением! Это тестовая версия.
Для начала работы используйте /main.
Тут возможно будет описание его возможностей.
"""

main_command_keyboard = ReplyKeyboardMarkup(keyboard=[["/main"]], resize_keyboard=True, one_time_keyboard=False) 



def get_start_command():
    names = ["start", "help"]

    @provide_pg_session
    async def command(update: Update, context: ContextTypes.DEFAULT_TYPE, db_session) -> None:
        user_id =  update.message.from_user.id
        user = await get_user_by_tg_id(db_session, user_id)
        
        if user:
            text_to_send = text_user_finded
        else:
            text_to_send = text_user_not_finded
            user = await create_user(db_session, user_id)
            
        await update.message.reply_text(text=text_to_send, reply_markup=main_command_keyboard)
        
    return CommandHandler(command=names, callback=command)


handlers = [get_start_command()]
