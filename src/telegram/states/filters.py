from aiogram.dispatcher.filters.state import State, StatesGroup

# Category selection states
class FilterStates(StatesGroup):
    site = State()
    category = State()
    bids = State()
    custom_bid = State()
    price = State()
    custom_price = State()
    sold = State()
    confirm = State()