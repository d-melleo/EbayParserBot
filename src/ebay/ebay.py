import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import types
from src.ebay import helper
from src.ebay import parser
from src.queues import parsing_queue, sending_queue
from src.telegram.handlers.markup_handler import MarkupHandler
from src.telegram.handlers.text_handler import TextHandler
from src.user.userdata import UserData


class Ebay:
    def __init__(self):
        self.parser: parser.Parser = None
        self.url_helper: helper.UrlHelper = None
        self.parsing_queue: parsing_queue.ParsingQueue = None
        self.sending_queue: sending_queue.SendingQueue = None


    ########################### MAIN LOGIC ##############################
    async def run(self, callback_query: types.CallbackQuery, filters: dict, user: UserData, text: TextHandler, markup: MarkupHandler):
        self.sending_queue = sending_queue.SendingQueue(callback_query, user, text, markup)
        self.parsing_queue = parsing_queue.ParsingQueue(self)
        self.url_helper = helper.UrlHelper()
        self.parser = parser.Parser(filters, self.parsing_queue, self.sending_queue, self.url_helper, markup, user)
        
        workers = [
            asyncio.create_task(self.parser.run(), name="parser"),
            asyncio.create_task(self.sending_queue.run(), name="sending_queue"),
            asyncio.create_task(self.parsing_queue.run(), name="parsing_queue")
        ]
        await asyncio.gather(*workers)
        
        print("\n*********************************** CATEGORY PARSING IS DONE ***********************************")


async def run_ebay(callback_query: types.CallbackQuery, filters: dict, state: FSMContext, user: UserData, text: TextHandler, markup: MarkupHandler):
    # Parse category
    ebay = Ebay()
    task = asyncio.create_task(
        ebay.run(callback_query, filters, user, text, markup))
    await task