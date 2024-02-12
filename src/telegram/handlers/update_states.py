from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from src.telegram import helper
from src.telegram import states


###################### HELPER FUNCTION ######################
async def store_message(message: types.Message, state: FSMContext=None):
    
    # Get current state
    if not state: 
        state: FSMContext = Dispatcher.get_current().current_state()
    
    # Store current chat and message info
    await state.update_data(chat_id=message.chat.id, message_id=message.message_id)


######################### MAIN MENU #########################
async def main_menu(*args):
    
    # Update state to expect a site name
    await states.FilterStates.site.set()


################### EBAY CATEGORIES MENU ####################
async def ebay_menu(callback_query: types.CallbackQuery, state: FSMContext):

    # Update state to expect a category name
    await states.FilterStates.category.set()
    
    # Store website into the state's info dictionary 
    await state.update_data(site=callback_query.data.title())


######################### BIDS MENU #########################
async def bids_menu(callback_query: types.CallbackQuery, state: FSMContext, markup):
    
    # Update state to expect bids
    await states.FilterStates.bids.set()
    
    # Store category into the state's info dictionarys
    await state.update_data(category=markup.language.ebay_buttons[callback_query.data])


#################### CUSTOM BIDS MENU #######################
async def custom_bid(*args):

    # Update state to expect input for custom bid
    await states.FilterStates.custom_bid.set()


######################## PRICE MENU #########################
async def price_menu(callback_query: types.CallbackQuery, state: FSMContext):
    
    # Update state to expect price
    await states.FilterStates.price.set()
    
    # Store bids into the state's info dictionary
    await state.update_data(bids = helper.get_bids(callback_query))


#################### CUSTOM PRICE MENU ######################
async def custom_price(*args):
    
    # Update state to expect input for custom price
    await states.FilterStates.custom_price.set()


######################### SOLD MENU #########################
async def sold_menu(callback_query: types.CallbackQuery, state: FSMContext):
    
    # Update state to expect True or False if show sold items
    await states.FilterStates.sold.set()
    
    # Store price into the state's info dictionary
    await state.update_data(price = helper.get_price(callback_query))


####################### PREVIEW MENU #######################
async def summary_preview(callback_query: types.CallbackQuery, state: FSMContext, markup):
    
    # Update state to await for a confirmation from a user
    await states.FilterStates.confirm.set()

    # Process sold callback
    sold, sold_label = helper.get_sold(callback_query, markup)

    # Store sold into the state's info dictionary
    await state.update_data(sold=sold, sold_label=sold_label)


async def last_choice(filters: dict, sold_label: str, state: FSMContext, markup) -> FSMContext:
    # Finish whatever state was before
    await state.finish()
    # Update state to await for a confirmation from a user
    await states.FilterStates.confirm.set()
    # Get current state instance
    upd_state: FSMContext = Dispatcher.get_current().current_state()
    # Write filters into state's storage
    await state.update_data(
        site=filters['site'],
        category=markup.language.ebay_buttons[filters['category']],
        bids=filters['bids'],
        price=filters['price'],
        sold=filters['sold'],
        sold_label=sold_label
    )
    return upd_state


################### STARTED SEARCH MENU ####################
async def start_search(state):
    
    # Finish filter conversation
    await state.finish()
    
    # Start new state conversation for parsing
    await states.ParsingStates.parsing.set()


###################### CANCEL SEARCH ########################
async def cancellation(state: FSMContext):
    
    # Finish conversation
    await state.finish()


##################### CONFIRM SENDING #######################
async def sending_captcha(*args):

    # Update state to await confirmation from user whether to keep sending items in Telegram
    await states.ParsingStates.sending_captcha.set()


async def after_captcha(state: FSMContext, answer: bool) -> None:
    
    # Update state based on whether of not kepp sending items 
    if answer == True:
        await states.ParsingStates.parsing.set()
    elif answer == False:
        await state.finish()


######################## SETTINGS ###########################
async def settings(state: FSMContext):
    # Finish current conversation
    await state.finish()
    # Change state to settings  
    await states.SettingsStates.settings.set()

async def settings_close(state: FSMContext):
    # Finish conversation
    await state.finish()


async def language_menu(state: FSMContext):
    # Update state
    await states.SettingsStates.language.set()


################### SET NUM OF MSG AT ONCE ###################
async def msg_send_items_at_once(state: FSMContext):
    await states.SettingsStates.msg_send_items_at_once.set()


async def set_msg_send_items_at_once(state: FSMContext):
    pass