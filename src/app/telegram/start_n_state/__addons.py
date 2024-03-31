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
