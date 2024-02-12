import requests
import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.telegram import helper
from src.telegram.handlers.markup_handler import MarkupHandler
from src.telegram.handlers.text_handler import TextHandler
from utils.loader import bot



######################### MAIN MENU #########################
async def main_menu(callback_query: types.CallbackQuery or types.Message, text: TextHandler, markup: MarkupHandler) -> types.Message:
    # Send a new message with main menu
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.main_menu(),
        reply_markup = markup.keyboard_mainMenu()
    )
    return message


################### EBAY CATEGORIES MENU ####################
async def ebay_menu(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    # Send ebay categories
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.ebay_menu(state),
        reply_markup = markup.keyboard_ebayMenu()
    )
    return message


######################### BIDS MENU #########################
async def bids_menu(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    # Send bids menu
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text =  await text.bids_menu(state),
        reply_markup = markup.keyboard_bidsMenu()
    )
    return message


#################### CUSTOM BIDS MENU #######################
async def custom_bid(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.custom_bids_menu(state)
    )
    return message


################## INVALID CUSTOM BIDS MENU #################
async def invalid_custom_bid(message: types.Message, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    # If custom bids input is not a number
    message = await bot.send_message(
        chat_id = helper.get_message_details(message)['chat_id'],
        text = text.invalid_custom_bids_menu(),
    )
    return message


######################## PRICE MENU #########################
async def price_menu(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:

    # Send price menu
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.price_menu(state),
        reply_markup = markup.keyboard_priceMenu()
    )
    return message


#################### CUSTOM PRICE MENU ######################
async def custom_price(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    # Send a message prompting a user for input. Expected plain number.
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.custom_price_menu(state)
    )
    return message


################ INVALID CUSTOM PRICE MENU ##################
async def invalid_custom_price(message: types.Message, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    # If custom price input is not a number
    message = await bot.send_message(
        chat_id = helper.get_message_details(message)['chat_id'],
        text = text.invalid_custom_price_menu(),
    )
    return message


######################### SOLD MENU #########################
async def sold_menu(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    
    # Send sold menu
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.sold_menu(state),
        reply_markup = markup.keyboard_soldMenu()
    )
    return message


####################### PREVIEW MENU #######################
async def summary_preview(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:

    # Send the finished conversation information
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.preview_menu(state),
        reply_markup = markup.keyboard_confirmStartMenu()
    )
    return message


################### STARTED SEARCH MENU ####################
async def start_search(callback_query: types.CallbackQuery, state: FSMContext, text: TextHandler, markup: MarkupHandler) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = await text.started_search_menu(state))
    return message


async def cancel_button(message: types.Message, text: TextHandler, markup: MarkupHandler):
    await message.reply(
        text = text.cancel_button(),
        reply_markup = markup.keyboard_cancel()
    )
async def cancel_button_clicked(message: types.Message, text: TextHandler, markup: MarkupHandler):
    try: 
        await message.reply(
            text=text.cancel_button_clicked(),
            reply_markup = types.ReplyKeyboardRemove()
        )
    except AttributeError: # 'CallbackQuery' object has no attribute 'reply'
        await bot.send_message(
            chat_id = helper.get_message_details(message)['chat_id'],
            text=text.cancel_button_clicked(),
            reply_markup = types.ReplyKeyboardRemove()
        )


############## SEND PARSED ITEMS TO TELEGRAM ################
async def send_item(callback_query: types.CallbackQuery, info: dict, text: TextHandler, markup: MarkupHandler):
    try:
        # Send message
        await send_content(callback_query, info, text, markup)
    except aiogram.utils.exceptions.CantParseEntities as e:
        raise e
    except aiogram.utils.exceptions.WrongFileIdentifier as r:
        print(r)
        info['image']: bytes = requests.get(info["image"]).content
        await send_content(callback_query, info, text, markup)


async def send_content(callback_query: types.CallbackQuery, info: dict, text: TextHandler, markup: MarkupHandler):
    content: dict = {}
    content['chat_id'] = callback_query.message.chat.id
    content['photo'] = info["image"]
    content['caption'] = text.send_item(info)
    content['parse_mode'] = types.ParseMode.MARKDOWN
    content['reply_markup'] = markup.create_link_button(info["url"])
    # Send message
    await bot.send_photo(**content)


################# CONFIRM CONTINUE SENDING ##################
async def sending_captcha(callback_query: types.CallbackQuery, q_size: int, text: TextHandler, markup: MarkupHandler) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.sending_captcha(q_size),
        reply_markup = markup.keyboard_sendingCaptchaMenu()
    )
    return message


async def settings(message: types.Message, text: TextHandler, markup: MarkupHandler) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(message)['chat_id'],
        text = text.settings(),
        reply_markup = markup.keyboard_settingsMenu()
    )
    return message


async def language_menu(callback_query: types.CallbackQuery, text: TextHandler, markup: MarkupHandler) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.language_menu(),
        reply_markup = markup.keyboard_languageMenu()
    )
    return message


async def msg_send_items_at_once(callback_query: types.CallbackQuery, text: TextHandler, markup: MarkupHandler) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text.msg_send_items_at_once(),
        reply_markup = markup.keyboard_msg_send_items_at_once_buttonsMenu()
    )
    return message


async def settings_close(callback_query: types.CallbackQuery, text: str) -> types.Message:
    message = await bot.send_message(
        chat_id = helper.get_message_details(callback_query)['chat_id'],
        text = text
    )
    return message