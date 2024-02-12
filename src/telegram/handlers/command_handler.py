import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext, Dispatcher
from src.ebay import ebay
from src.ebay import helper as task_helper
from src.queues import confirmation_queue
from src.telegram import handlers
from src.telegram import helper
from src.telegram import states
from src.user import userdata
from utils.mongo import CLIENT


class CommandHandler:
    def __init__(self, dp: Dispatcher):
        self.markup: handlers.markup_handler.MarkupHandler = None
        self.text: handlers.text_handler.TextHandler = None
        self.user: userdata.UserData = None
        
        ##################### REGISTER HANDLERS #####################
        # Start
        dp.register_callback_query_handler(self.on_start, state=None)
        dp.register_message_handler(self.on_start, commands=["start"], state=None)
        # Main Menu
        dp.register_callback_query_handler(self.main_menu, lambda x: x.data == "main_menu", state="*")
        # Ebay Menu
        dp.register_callback_query_handler(self.ebay_menu, lambda x: x.data in list(filter(lambda x: x != "last_choice", self.text.language.website_buttons)), state="*")
        # Bids
        dp.register_callback_query_handler(self.bids_menu, lambda x: x.data in self.text.language.ebay_buttons, state="*")
        dp.register_callback_query_handler(self.custom_bid, lambda x: x.data == "bid_custom", state=states.FilterStates.bids)
        dp.register_message_handler(self.invalid_custom_bid, content_types=types.ContentTypes.TEXT, regexp='\D+', state=states.FilterStates.custom_bid)
        # Price
        dp.register_callback_query_handler(self.price_menu, lambda x: x.data in list(filter(lambda x: x != "bid_custom", self.text.language.bids_buttons)), state=states.FilterStates.bids)
        dp.register_message_handler(self.price_menu, content_types=types.ContentTypes.TEXT, regexp='^[0-9]+$', state=states.FilterStates.custom_bid)
        dp.register_callback_query_handler(self.custom_price, lambda x: x.data == "price_custom", state=states.FilterStates.price)
        dp.register_message_handler(self.invalid_custom_price, content_types=types.ContentTypes.TEXT, regexp='\D+', state=states.FilterStates.custom_price)
        # Sold
        dp.register_callback_query_handler(self.sold_menu, lambda x: x.data in list(filter(lambda x: x != "price_custom", self.text.language.price_buttons)), state=states.FilterStates.price)
        dp.register_message_handler(self.sold_menu, content_types=types.ContentTypes.TEXT, regexp='^[0-9]+$', state=states.FilterStates.custom_price)
        # Category summary
        dp.register_callback_query_handler(self.summary_preview, lambda x: x.data in self.text.language.sold_buttons, state=states.FilterStates.sold)
        # Last choice
        dp.register_callback_query_handler(self.last_choice, lambda x: x.data == "last_choice", state="*")
        # Start parsing
        dp.register_callback_query_handler(self.start_search, lambda x: x.data == "confirm_yes", state=states.FilterStates.confirm)
        # Cancel
        dp.register_message_handler(self.cancellation, lambda callback_query: callback_query.text == self.text.language.vocabulary["cancel"], state="*")
        dp.register_message_handler(self.cancellation, commands=["stop"], state="*")
        dp.register_callback_query_handler(self.cancellation, lambda x: x.data == "confirm_no", state="*")
        # Captcha
        dp.register_callback_query_handler(self.after_captcha, lambda x: x.data in self.text.language.captcha_buttons, state=states.ParsingStates.sending_captcha)
        # Settings
        dp.register_message_handler(self.settings_menu, commands=["settings"], state="*")
        dp.register_callback_query_handler(self.msg_send_items_at_once, lambda x: x.data == "msg_send_items_at_once", state=states.SettingsStates.settings)
        dp.register_callback_query_handler(self.set_msg_send_items_at_once, lambda x: x.data in self.text.language.msg_at_once_buttons, state=states.SettingsStates.msg_send_items_at_once)
        dp.register_callback_query_handler(self.language_menu, lambda x: x.data == "language_menu", state=states.SettingsStates.settings)
        dp.register_callback_query_handler(self.select_language, lambda x: x.data in self.text.language.language_buttons, state=states.SettingsStates.language)
        
        
    ########################### START ###########################
    # @dp.callback_query_handler(state=None)
    # @dp.message_handler(commands=["start"], state=None)
    async def on_start(self, callback_query: types.Message):
        self.user = userdata.UserData(CLIENT, callback_query)
        self.markup = handlers.markup_handler.MarkupHandler(self.user)
        self.text = handlers.text_handler.TextHandler(self.user.language)
        await self.on_restart(callback_query)
        
        
    async def on_restart(self, callback_query: types.CallbackQuery or types.Message):
        # types.CallbackQuery
        try:
            command = callback_query.data
        # types.Message
        except AttributeError: # 'CallbackQuery' object has no attribute 'text'
            command = callback_query.text
        
        # In case if the bot was restarted, the user should be able to use buttons on the main menu without prior using a /start command
        if command == "/start": await self.main_menu(callback_query)
        if command == "ebay": await self.ebay_menu(callback_query, state=Dispatcher.get_current().current_state())
        if command == "confirm_no": await self.cancellation(callback_query, Dispatcher.get_current().current_state(), command)
        if command == "last_choice": await self.last_choice(callback_query, state=Dispatcher.get_current().current_state())
        
        
    ######################### MAIN MENU #########################
    # @dp.callback_query_handler(lambda x: x.data == "main_menu", state="*")
    async def main_menu(self, callback_query: types.CallbackQuery or types.Message):
        await handlers.update_states.main_menu()
        message = await handlers.send_message.main_menu(callback_query, self.text, self.markup)
        await handlers.update_states.store_message(message)
        
        
    ################### EBAY CATEGORIES MENU ####################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_mainMenu.keys(), state="*")
    async def ebay_menu(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        await handlers.update_states.ebay_menu(callback_query, state)
        message = await handlers.send_message.ebay_menu(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ######################### BIDS MENU #########################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_ebayMenu.keys(), state="*")
    async def bids_menu(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.bids_menu(callback_query, state, self.markup)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.bids_menu(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    #################### CUSTOM BIDS MENU #######################
    # @dp.callback_query_handler(lambda x: x.data == "bid_custom", state=FilterStates.bids)
    async def custom_bid(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.custom_bid(callback_query, state)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.custom_bid(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ################## INVALID CUSTOM BIDS MENU #################
    # @dp.message_handler(content_types=types.ContentTypes.TEXT, regexp='\D+', state=FilterStates.custom_bid)
    async def invalid_custom_bid(self, message: types.Message, state: FSMContext):
        await handlers.send_message.invalid_custom_bid(message, state, self.text, self.markup)
        
        
    ######################## PRICE MENU #########################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_bidsMenu.keys(), state=FilterStates.bids)
    # @dp.message_handler(content_types=types.ContentTypes.TEXT, regexp='^[0-9]+$', state=FilterStates.custom_bid)
    async def price_menu(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.price_menu(callback_query, state)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.price_menu(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    #################### CUSTOM PRICE MENU ######################
    # @dp.callback_query_handler(lambda x: x.data == "price_custom", state=FilterStates.price)
    async def custom_price(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.custom_price(callback_query, state)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.custom_price(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ################ INVALID CUSTOM PRICE MENU ##################
    # @dp.message_handler(content_types=types.ContentTypes.TEXT, regexp='\D+', state=FilterStates.custom_price)
    async def invalid_custom_price(self, message: types.Message, state: FSMContext):
        await handlers.send_message.invalid_custom_price(message, state, self.text, self.markup)
        
        
    ######################### SOLD MENU #########################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_priceMenu.keys(), state=FilterStates.price)
    # @dp.message_handler(content_types=types.ContentTypes.TEXT, regexp='^[0-9]+$', state=FilterStates.custom_price)
    async def sold_menu(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.sold_menu(callback_query, state)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.sold_menu(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ####################### PREVIEW MENU #######################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_soldMenu.keys(), state=FilterStates.sold)
    async def summary_preview(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.update_states.summary_preview(callback_query, state, self.markup)
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.summary_preview(callback_query, state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ####################### LAAST CHOICE #######################
    # dp.callback_query_handler(lambda x: x.data in list(filter(lambda x: x != "last_choice", self.text.language.website_buttons)), state="*")
    async def last_choice(self, callback_query: types.CallbackQuery, state: FSMContext):
        upd_state = await handlers.update_states.last_choice(
            filters = self.user.last_choice,
            sold_label = (lambda x: self.markup.language.sold_buttons['sold_1'] if x else self.markup.language.sold_buttons['sold_0'])(self.user.last_choice['sold']),
            state = state,
            markup=self.markup)
        
        message = await handlers.send_message.summary_preview(callback_query, upd_state, self.text, self.markup)
        await handlers.update_states.store_message(message, state)
        
        
    ################### STARTED SEARCH MENU ####################
    # @dp.callback_query_handler(lambda x: x.data == "confirm_yes", state=FilterStates.confirm)
    async def start_search(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        message = await handlers.send_message.start_search(callback_query, state, self.text, self.markup)
        await handlers.send_message.cancel_button(message, self.text, self.markup)
        
        # Pass conversation's information to filters
        filters: dict = await helper.get_filters(state, self.markup)
        # Update states
        await handlers.update_states.start_search(state)
        # Update last choice
        self.user.update_last_choice(filters)
        # Start parsing category
        await ebay.run_ebay(callback_query, filters, state, self.user, self.text, self.markup)
        # Send main menu once parsing is done
        await self.main_menu(callback_query)
        
        
    ###################### CANCEL SEARCH ########################
    # @dp.message_handler(lambda callback_query: callback_query.text == mark.LANGUAGE.menu_buttons["confirm_no"], state="*")
    # @dp.message_handler(commands=["stop"], state="*")
    # @dp.callback_query_handler(lambda x: x.data == "confirm_no", state="*")
    async def cancellation(self, callback_query: types.CallbackQuery, state: FSMContext, *text):
        await task_helper.cancel_tasks("process_sub_categories", "parsing_queue", "parser", "sending_queue")
        if not "/settings" in text:
            await handlers.delete_message.del_from_state(state)
            await handlers.update_states.cancellation(state)
            await handlers.send_message.cancel_button_clicked(callback_query, self.text, self.markup)
            
            await self.main_menu(callback_query)
        
        
    ################# CONFIRM CONTINUE SENDING ##################
    @staticmethod
    async def sending_captcha(callback_query: types.CallbackQuery, q_size: int, text, markup) -> bool:
        await handlers.update_states.sending_captcha()
        message = await handlers.send_message.sending_captcha(callback_query, q_size, text, markup)
        await handlers.update_states.store_message(message)
        
        answer: bool = asyncio.create_task(confirmation_queue.get_input())
        return await answer
    
    
    ##################### CONFIRM SENDING #######################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_confirmSendingMenu.keys(), state=ParsingStates.sending_captcha)
    async def after_captcha(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        answer = helper.sending_captcha(callback_query)
        await handlers.update_states.after_captcha(state, answer)
        await confirmation_queue.queue.put(answer)
        
        
    @staticmethod
    async def stop_sending(callback_query: types.CallbackQuery, text, markup):
        await task_helper.cancel_tasks("process_sub_categories", "parsing_queue", "parser")
        # await handlers.send_message.stop_sending(callback_query, text, markup)
        await handlers.send_message.cancel_button_clicked(callback_query, text, markup)


    ######################## SETTINGS MENU #######################
    # @dp.message_handler(commands=["settings"], state="*")
    async def settings_menu(self, message: types.Message, state: FSMContext):
        await self.cancellation(message, state, message.text)
        await handlers.update_states.settings(state)
        message = await handlers.send_message.settings(message, self.text, self.markup)
        await handlers.update_states.store_message(message)
    
    
    async def language_menu(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        await handlers.update_states.language_menu(state)
        message = await handlers.send_message.language_menu(callback_query, self.text, self.markup)
        await handlers.update_states.store_message(message)


    async def select_language(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        self.user.update_language(callback_query)
        self.markup.update_language(self.user.language)
        self.text.update_language(self.user.language)
        await self.close_settings(callback_query, state, text=self.text.language_updated(callback_query.data))


    #################### NUM OF MSG AT ONCE #####################
    # @dp.callback_query_handler(lambda x: x.data == "msg_send_items_at_once", state=SettingsStates.settings)
    async def msg_send_items_at_once(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        await handlers.update_states.msg_send_items_at_once(state)
        message = await handlers.send_message.msg_send_items_at_once(callback_query, self.text, self.markup)
        await handlers.update_states.store_message(message, state)


    ################### SET NUM OF MSG AT ONCE ###################
    # @dp.callback_query_handler(lambda x: x.data in Buttons.buttons_msgAtOnceMenu.keys(), state=SettingsStates.msg_send_items_at_once)
    async def set_msg_send_items_at_once(self, callback_query: types.CallbackQuery, state: FSMContext):
        await handlers.delete_message.del_from_state(state)
        self.user.update_msg_at_once(callback_query)
        await self.close_settings(callback_query, state, text=self.text.msg_send_items_at_once_done(self.user.msg_send_at_once))


    ######################## CLOSE SETTINGS ######################
    async def close_settings(self, callback_query: types.CallbackQuery, state: FSMContext, text: str):
        await handlers.send_message.settings_close(callback_query, text=text)
        await handlers.update_states.settings_close(state)
        await self.main_menu(callback_query)