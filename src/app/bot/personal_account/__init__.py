from .personal_cabinet_callback import personal_cabinet_callbacks as __personal_cabinet_callbacks
from .personal_cabinet_states import personal_cabinet_handler

personal_cabinet_handlers = [
    *__personal_cabinet_callbacks,
    personal_cabinet_handler
]
