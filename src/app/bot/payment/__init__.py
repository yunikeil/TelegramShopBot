from .payment_callback import payment_callbacks as __payment_callbacks


payment_state_handlers = [
    *__payment_callbacks,
]
