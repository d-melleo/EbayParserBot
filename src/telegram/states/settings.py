from aiogram.dispatcher.filters.state import State, StatesGroup

# Category selection states
class SettingsStates(StatesGroup):
    settings = State()
    language = State()
    msg_send_items_at_once = State()