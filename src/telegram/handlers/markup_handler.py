import importlib
from types import ModuleType

from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


LANG_PATH = 'src.telegram.language.{}'


class MarkupHandler:
    def __init__(self, user) -> None:
        # Import language module
        self.user = user
        self.language = None
        self.update_language(user.language)


    def update_language(self, language) -> ModuleType:
        self.language: ModuleType = importlib.import_module(LANG_PATH.format(language))


    ################################# CANCEL BUTTON #################################
    def keyboard_cancel(self) -> ReplyKeyboardMarkup:
        btn_cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn_cancel_keyboard.add(KeyboardButton(text=self.language.confirm_buttons["confirm_no"]))
        return btn_cancel_keyboard


    ################################### SITE MENU ###################################
    def keyboard_mainMenu(self) -> InlineKeyboardMarkup:
        mainMenu = InlineKeyboardMarkup(row_width=1)
        mainMenu.add(InlineKeyboardButton(text=self.language.website_buttons["ebay"], callback_data="ebay"))
        if self.user.last_choice:
            mainMenu.add(InlineKeyboardButton(text=self.language.website_buttons["last_choice"], callback_data="last_choice"))
        return mainMenu


    ################################### EBAY MENU ###################################
    def keyboard_ebayMenu(self) -> InlineKeyboardMarkup:
        ebayMenu = InlineKeyboardMarkup(row_width=2)
        
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["0"], callback_data="0"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["20081"], callback_data="20081"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["550"], callback_data="550"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["2984"], callback_data="2984"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["267"], callback_data="267"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["12576"], callback_data="12576"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["625"], callback_data="625"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["15032"], callback_data="15032"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["11450"], callback_data="11450"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["11116"], callback_data="11116"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["1"], callback_data="1"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["58058"], callback_data="58058"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["293"], callback_data="293"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["14339"], callback_data="14339"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["237"], callback_data="237"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["11232"], callback_data="11232"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["6000"], callback_data="6000"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["45100"], callback_data="45100"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["172008"], callback_data="172008"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["26395"], callback_data="26395"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["11700"], callback_data="11700"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["281"], callback_data="281"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["11233"], callback_data="11233"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["619"], callback_data="619"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["1281"], callback_data="1281"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["870"], callback_data="870"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["10542"], callback_data="10542"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["316"], callback_data="316"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["888"], callback_data="888"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["64482"], callback_data="64482"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["260"], callback_data="260"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["1305"], callback_data="1305"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["220"], callback_data="220"))
        ebayMenu.insert(InlineKeyboardButton(text=self.language.ebay_buttons["3252"], callback_data="3252"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["1249"], callback_data="1249"))
        ebayMenu.add(InlineKeyboardButton(text=self.language.ebay_buttons["99"], callback_data="99"))
        # Cancel button
        ebayMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return ebayMenu


    ################################### BIDS MENU ###################################
    def keyboard_bidsMenu(self) -> InlineKeyboardMarkup:
        bidMenu = InlineKeyboardMarkup(row_width=4)
        
        bidMenu.add(InlineKeyboardButton(text=self.language.bids_buttons["bid_10"], callback_data="bid_10"))
        bidMenu.insert(InlineKeyboardButton(text=self.language.bids_buttons["bid_30"], callback_data="bid_30"))
        bidMenu.insert(InlineKeyboardButton(text=self.language.bids_buttons["bid_50"], callback_data="bid_50"))
        bidMenu.insert(InlineKeyboardButton(text=self.language.bids_buttons["bid_100"], callback_data="bid_100"))
        bidMenu.add(InlineKeyboardButton(text=self.language.bids_buttons["bid_custom"], callback_data="bid_custom"))
        # Cancel button
        bidMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return bidMenu


    ################################### PRICE MENU ##################################
    def keyboard_priceMenu(self) -> InlineKeyboardMarkup:
        priceMenu = InlineKeyboardMarkup(row_width=4)
        
        priceMenu.add(InlineKeyboardButton(text=self.language.price_buttons["price_0"], callback_data="price_0"))
        priceMenu.add(InlineKeyboardButton(text=self.language.price_buttons["price_100"], callback_data="price_100"))
        priceMenu.insert(InlineKeyboardButton(text=self.language.price_buttons["price_300"], callback_data="price_300"))
        priceMenu.insert(InlineKeyboardButton(text=self.language.price_buttons["price_500"], callback_data="price_500"))
        priceMenu.insert(InlineKeyboardButton(text=self.language.price_buttons["price_1000"], callback_data="price_1000"))
        priceMenu.add(InlineKeyboardButton(text=self.language.price_buttons["price_custom"], callback_data="price_custom"))
        # Cancel button
        priceMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return priceMenu


    ################################### SOLD MENU ###################################
    def keyboard_soldMenu(self) -> InlineKeyboardMarkup:
        soldMenu = InlineKeyboardMarkup(row_width=2)
        
        soldMenu.add(InlineKeyboardButton(text=self.language.sold_buttons["sold_1"], callback_data="sold_1"))
        soldMenu.insert(InlineKeyboardButton(text=self.language.sold_buttons["sold_0"], callback_data="sold_0"))
        # Cancel button
        soldMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return soldMenu


    ################################# START PARSING #################################
    def keyboard_confirmStartMenu(self) -> InlineKeyboardMarkup:
        confirmStartMenu = InlineKeyboardMarkup(row_width=1)
        
        confirmStartMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_yes"], callback_data="confirm_yes"))
        confirmStartMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return confirmStartMenu


    ################################ CONTINUE PARSING ###############################
    def keyboard_sendingCaptchaMenu(self) -> InlineKeyboardMarkup:
        sendingCaptchaMenu = InlineKeyboardMarkup(row_width=2)
        
        sendingCaptchaMenu.add(InlineKeyboardButton(text=self.language.captcha_buttons["confirm_send_yes"], callback_data="confirm_send_yes"))
        sendingCaptchaMenu.add(InlineKeyboardButton(text=self.language.captcha_buttons["confirm_send_no"], callback_data="confirm_send_no"))
        
        return sendingCaptchaMenu


    ################################### OPEN LINK ###################################
    def create_link_button(self, url: str) -> InlineKeyboardMarkup:
        link_inline = InlineKeyboardMarkup()
        
        link_button = InlineKeyboardButton(text=self.language.vocabulary['redirect'], url=url)
        link_inline.add(link_button)
        
        return link_inline


    ################################# SETTINGS MENU #################################
    def keyboard_settingsMenu(self) -> InlineKeyboardMarkup:
        settingsMenu = InlineKeyboardMarkup(row_width=1)
        
        settingsMenu.add(InlineKeyboardButton(text=self.language.setting_buttons["language_menu"], callback_data="language_menu"))
        settingsMenu.add(InlineKeyboardButton(text=self.language.setting_buttons["msg_send_items_at_once"], callback_data="msg_send_items_at_once"))
        # Cancel button
        settingsMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return settingsMenu


    def keyboard_languageMenu(self) -> InlineKeyboardMarkup:
        languageMenu = InlineKeyboardMarkup(row_width=1)
        
        languageMenu.add(InlineKeyboardButton(text=self.language.language_buttons["lang_en"], callback_data="lang_en"))
        languageMenu.add(InlineKeyboardButton(text=self.language.language_buttons["lang_ua"], callback_data="lang_ua"))
        # Cancel button
        languageMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return languageMenu


    ############################ SET NUMBER OF MESSAGES #############################
    def keyboard_msg_send_items_at_once_buttonsMenu(self) -> InlineKeyboardMarkup:
        msg_send_items_at_once_buttonsMenu = InlineKeyboardMarkup(row_width=5)
        
        msg_send_items_at_once_buttonsMenu.add(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_1"], callback_data="msg_at_once_set_to_1"))
        msg_send_items_at_once_buttonsMenu.insert(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_3"], callback_data="msg_at_once_set_to_3"))
        msg_send_items_at_once_buttonsMenu.insert(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_5"], callback_data="msg_at_once_set_to_5"))
        msg_send_items_at_once_buttonsMenu.insert(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_10"], callback_data="msg_at_once_set_to_10"))
        msg_send_items_at_once_buttonsMenu.insert(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_15"], callback_data="msg_at_once_set_to_15"))
        msg_send_items_at_once_buttonsMenu.add(InlineKeyboardButton(text=self.language.msg_at_once_buttons["msg_at_once_set_to_0"], callback_data="msg_at_once_set_to_0"))
        # Cancel button
        msg_send_items_at_once_buttonsMenu.add(InlineKeyboardButton(text=self.language.confirm_buttons["confirm_no"], callback_data="confirm_no"))
        
        return msg_send_items_at_once_buttonsMenu