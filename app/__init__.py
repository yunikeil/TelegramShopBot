from .telegram.start_n_state import start_state_handlers
from .telegram.main_n_state import main_state_handlers

from .telegram.catalog_n_state import catalog_handlers
from .telegram.shopping_cart_n_state import shopping_cart_handlers
from .telegram.about_us_n_state import about_us_handlers
from .telegram.personal_cabinet_n_state import personal_cabinet_handlers

from .telegram.admin_state import admin_handlers


bot_handlers = [
    *start_state_handlers,
    *main_state_handlers,
    *catalog_handlers,
    *shopping_cart_handlers,
    *about_us_handlers,
    *personal_cabinet_handlers,
    *admin_handlers,
]
