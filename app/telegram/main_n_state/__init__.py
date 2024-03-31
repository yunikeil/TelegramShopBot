from .main_command import main_commands as __main_commands
from .main_callback import main_callbacs as __main_callbacs

main_state_handlers = [
    *__main_commands,
    *__main_callbacs,
]
