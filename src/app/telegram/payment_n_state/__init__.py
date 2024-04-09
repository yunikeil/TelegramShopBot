from .payment_callback import payment_callbacks as __payment_callbacks
from .payment_command import payment_commands as __payment_commands


payment_state_handlers = [
    *__payment_callbacks,
    *__payment_commands,
]
