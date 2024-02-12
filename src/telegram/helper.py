import re
from aiogram import types
from aiogram.dispatcher import FSMContext


# Get message id and chat id
def get_message_details(callback_query: types.CallbackQuery or types.Message) -> dict:
    # Get the details if type is CallbackQuery
    try:
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
    # Get the details if type is Message
    except AttributeError:
        chat_id = callback_query.chat.id
        message_id = callback_query.message_id
        
    return {'chat_id': chat_id, 'message_id': message_id}

# Get user's bids input from callback
def get_bids(callback_query: types.CallbackQuery or types.Message) -> int:
    try: # If bid was selected from given options
        bids = int(callback_query.data.split('_')[1])
    except AttributeError: # If bid was manually given
        bids = int(callback_query.text)
    return bids

# Get user's price input from callback
def get_price(callback_query: types.CallbackQuery or types.Message) -> int:
    try: # If price was selected from given options
        price = int(callback_query.data.split('_')[1])
    except AttributeError: # If price was manually given
        price = int(callback_query.text)
    return price

# Get user's imput on sold menu
def get_sold(callback_query: types.CallbackQuery, markup) -> bool:
    # Get button label
    label = markup.language.sold_buttons[callback_query.data]
    # Process callback query for sold items
    if callback_query.data.split('_')[1] == "1":
        sold = True
    elif callback_query.data.split('_')[1] == "0":
        sold = False
    return sold, label

# Process confirmation
def sending_captcha(callback_query: types.CallbackQuery) -> bool:
    if callback_query.data == "confirm_send_yes":
        return True
    elif callback_query.data == "confirm_send_no":
        return False

# Return values of keys
async def get_state_data(state: FSMContext, *keys: str) -> list:
    if type(state) is FSMContext:
        try:
            data: dict = await state.get_data()
            values = list(map(lambda x: data[x], keys))
            return values
        except KeyError:
            return None

async def get_filters(state: FSMContext, markup) -> dict:
    data = await state.get_data()
    # Set filters
    filters = {
        "site": data['site'],
        "category": get_category_id(data['category'], markup),
        "bids": data['bids'],
        "price": data['price'],
        "sold": data['sold']
    }
    return filters

def get_category_id(category_label: str, markup) -> int:
    category_id = list(filter(lambda x: markup.language.ebay_buttons[x] == category_label, markup.language.ebay_buttons))
    return category_id[0]
