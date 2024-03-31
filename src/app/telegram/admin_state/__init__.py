from .admin_callbacks import admin_callbacks as __admin_callbacks
from .admin_states import admin_catalog_handler

admin_handlers = [
    *__admin_callbacks,
    admin_catalog_handler
]