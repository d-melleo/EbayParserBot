from aiogram.dispatcher import FSMContext
from src.telegram import helper
from utils.loader import bot


#################### DELETE FROM STATE #####################
async def del_from_state(state: FSMContext):
    try:
        await bot.delete_message(
            *await helper.get_state_data(state, 'chat_id'),
            *await helper.get_state_data(state, 'message_id')
        )
    except TypeError:
        return