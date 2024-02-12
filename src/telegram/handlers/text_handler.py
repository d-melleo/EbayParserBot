import importlib
from textwrap import dedent
from types import ModuleType
from aiogram.dispatcher import FSMContext
from anim import emoji
from src.telegram import helper


LANG_PATH = 'src.telegram.language.{}'


class TextHandler:
    def __init__(self, language: str) -> None:
        # Import language module
        self.language = None
        self.update_language(language)


    def update_language(self, language) -> ModuleType:
        self.language: ModuleType = importlib.import_module(LANG_PATH.format(language))


    ############### MAIN MENU ###################
    def main_menu(self, state: FSMContext=None) -> str:
        text: str = dedent('''\
            {select_website} {emoji}
        ''').format(
            select_website=self.language.vocabulary['select_website'],
            emoji=emoji.rand_emoji(1)
        )
        return text


    ############### EBAY MENU ###################
    async def ebay_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
                
                ❗️ {select_category}:
        ''').format(
            site=self.language.vocabulary['site'],
            select_category=self.language.vocabulary['select_category'],
            *await helper.get_state_data(state,
                'site')
        )
        return text


    ############### BIDS MENU ###################
    async def bids_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            
                ❗️ {select_bids}
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            select_bids=self.language.vocabulary['select_bids'],
            *await helper.get_state_data(state,
                'site',
                'category')
        )
        return text


    ############ CUSTOM BIDS MENU ###############
    async def custom_bids_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            
                ❗️ {select_custom_bids}
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            select_custom_bids=self.language.vocabulary['select_custom_bids'],
            *await helper.get_state_data(state,
                'site',
                'category')
        )
        return text


    ######## INVALID CUSTOM BIDS MENU ###########
    def invalid_custom_bids_menu(self, state: FSMContext=None) -> str:
        text: str = dedent('''\
            🚫 {invalid_custom_bids}
        ''').format(
            invalid_custom_bids=self.language.vocabulary['invalid_custom_bids']
        )
        return text


    ############### PRICE MENU ##################
    async def price_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            ✅ {bids} - {}+
            
                ❗️ {select_price} $
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            bids=self.language.vocabulary['bids'],
            select_price=self.language.vocabulary['select_price'],
            *await helper.get_state_data(state,
                'site',
                'category',
                'bids')
        )
        return text


    ############ CUSTOM PRICE MENU ###############
    async def custom_price_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            ✅ {bids} - {}+
            
                ❗️ {select_custom_price} $
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            bids=self.language.vocabulary['bids'],
            select_custom_price=self.language.vocabulary['select_custom_price'],
            *await helper.get_state_data(state,
                'site',
                'category',
                'bids')
        )
        return text


    ######## INVALID CUSTOM PRICE MENU ###########
    def invalid_custom_price_menu(self, state: FSMContext=None) -> str:
        text: str = dedent('''\
            🚫 {invalid_custom_price}
        ''').format(
            invalid_custom_price=self.language.vocabulary['invalid_custom_price']
        )
        return text


    ################# SOLD MENU ##################
    async def sold_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            ✅ {bids} - {}+
            ✅ {price} - ${}+
            
                ❗️ {select_sold}
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            bids=self.language.vocabulary['bids'],
            price=self.language.vocabulary['price'],
            select_sold=self.language.vocabulary['select_sold'],
            *await helper.get_state_data(state,
                'site',
                'category',
                'bids',
                'price')
        )
        return text


    ############## PREVIEW MENU #################
    async def preview_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            ✅ {bids} - {}+
            ✅ {price} - {}+
            {} {sold}
            
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            bids=self.language.vocabulary['bids'],
            price=self.language.vocabulary['price'],
            sold=self.language.vocabulary['sold'],
            *await helper.get_state_data(state,
                'site',
                'category',
                'bids',
                'price',
                'sold_label')
        )
        return text


    ########### STARTED SEARCH MENU #############
    async def started_search_menu(self, state: FSMContext) -> str:
        text: str = dedent('''\
            ✅ {site} - {}
            ✅ {category} - {}
            ✅ {bids} - {}+
            ✅ {price} - {}+
            {} {sold}
            
            
                🔍 {searching} 👀
        ''').format(
            site=self.language.vocabulary['site'],
            category=self.language.vocabulary['category'],
            bids=self.language.vocabulary['bids'],
            price=self.language.vocabulary['price'],
            sold=self.language.vocabulary['sold'],
            searching=self.language.vocabulary['searching'],
            *await helper.get_state_data(state,
                'site',
                'category',
                'bids',
                'price',
                'sold_label')
        )
        return text


    ####### SEND PARSED ITEMS TO TELEGRAM #######
    def send_item(self, info: dict) -> str:
        text: str = dedent('''\
            📍 {item_title}
            
            📌 {bids}: {item_bids}
            💰 {price}: {item_price}
            ''').format(
                bids=self.language.vocabulary['bids'],
                price=self.language.vocabulary['price'],
                item_title=info["title"],
                item_bids=info["bids"],
                item_price=info["price"]
            )
        return text


    ############## CONFIRM SENDING ##############
    def sending_captcha(self, q_size: int) -> str:
        text: str = dedent('''\
            {keep_sending} ({queue_size})
        ''').format(
            keep_sending=self.language.vocabulary['keep_sending'],
            queue_size=str(q_size)
        )
        return text


    ################# SETTINGS ##################
    def settings(self) -> str:
        text: str = dedent('''\
            {settings}
        ''').format(
            settings=self.language.vocabulary['settings']
        )
        return text


    def language_menu(self) -> str:
        text: str = dedent('''\
            {select_language}
        ''').format(
            select_language=self.language.vocabulary['select_language']
        )
        return text


    def language_updated(self, lang_data: str) -> str:
        text: str = dedent('''\
            {language_change} {language}
        ''').format(
            language_change=self.language.vocabulary['language_changed'],
            language=self.language.language_buttons[lang_data]
        )
        return text


    def msg_send_items_at_once(self) -> str:
        text: str = dedent('''\
            {change_msg_at_once}
        ''').format(
            change_msg_at_once=self.language.vocabulary['change_msg_at_once']
        )
        return text


    def msg_send_items_at_once_done(self, msg_at_once: int) -> str:
        text: str = dedent('''\
            {changed_to} {msg_at_once}
        ''').format(
            changed_to=self.language.vocabulary['changed_to'],
            msg_at_once = (lambda x: self.language.menu_buttons['msg_at_once_set_to_0'] if x == '0' else str(x))(msg_at_once)
        )
        return text


    def cancel_button(self) -> str:
        text: str = dedent('''\
            {cancel_tip}
        ''').format(
            cancel_tip=self.language.vocabulary['cancel_tip']
        )
        return text

    def cancel_button_clicked(self) -> str:
        text: str = dedent('''\
            {emoji}
        ''').format(
            # cancelled=LANGUAGE.vocabulary['cancelled'],
            emoji=emoji.rand_emoji(1, ['👌', '👌🏻', '👌🏼', '👌🏽', '👌🏾', '👌🏿'])
        )
        return text