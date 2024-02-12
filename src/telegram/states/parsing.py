from aiogram.dispatcher.filters.state import State, StatesGroup

# Category selection states
class ParsingStates(StatesGroup):
    parsing = State()
    sending_captcha = State()