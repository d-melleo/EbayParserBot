import aiohttp
import asyncio
import itertools
import re
from textwrap import dedent

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from src.ebay.helper import UrlHelper
from src.queues.parsing_queue import ParsingQueue
from src.queues.sending_queue import SendingQueue
from src.telegram.handlers.markup_handler import MarkupHandler
from utils.loader import proxy
from utils.proxy import UnableToRetrieveResponse, \
    ConcurrencyLimitExceeded, OutOfRequests, NoException

class Parser:
    def __init__(self, filters, parsing_queue, sending_queue, url_helper, markup, user) -> None:
        self.base_url: str = "https://www.ebay.com/"
        self.filters: dict = filters
        self.markup = markup
        self.parsing_queue: ParsingQueue = parsing_queue
        self.sending_queue: SendingQueue = sending_queue
        self.timeout = aiohttp.ClientTimeout(total=120)
        self.url_helper: UrlHelper = url_helper
        self.user = user


    def start(self, category: list[str]) -> list[str]:
        if "0" in category:
            category = list(filter(lambda x: x != "0", self.markup.language.ebay_buttons))
        return category


    def select_category(self, category: str) -> str:
        return f'{self.base_url}b/{category}'
    
    
    async def request_page(self, url: str, params:dict=None, base: bool = False) -> str:
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                async with session.get(url=url, params=params) as response:
                    print(f'\n=============== STATUS CODE: {response.status} ===============\n{response.url}')
                    proxy.validate_response(response.status)
                    page: str = await response.text()
                    return page, response.url
        except (UnableToRetrieveResponse, ConcurrencyLimitExceeded,\
            OutOfRequests, aiohttp.client_exceptions.TooManyRedirects, NoException) as err:
            if not base:
                await self.parsing_queue.queue.put(self.url_helper.revert_page(url)) # Add the url back in queue
                
            proxy.next_proxy() # Change proxy server
            print(err)
            return None, response.url
    
    
    def get_sub_categories(self, page: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        # Get url for "See all in {sub tree}" categories
        sub_trees: list[ResultSet] = list(map(lambda x: x.find_all(["a"], {"class": lambda x: "sibling" in x}), soup.find_all(["ul"], {"class": "b-accordion-subtree"})))
        sub_trees_links: list = [y["href"] for x in sub_trees for y in x if "see all" in y.text.lower()]
        # Get url for direct sub categories
        no_trees: ResultSet = soup.find(["div"], {"class": "dialog__cell"}).find_all(["a"], {"class": lambda x: "textlink" in x and "parent" in x})
        no_trees_links: list = [x["href"] for x in no_trees]
        # Collect all links in a list
        category_links: list = list(itertools.chain(sub_trees_links, no_trees_links))
        return category_links


    # async def get_sub_categories(self, category: str) -> list:
    #     with open("./json/ebay_categories.json", "r") as f:
    #         data = json.load(f)
    #         if category == '0':
    #             sub_categories = list(itertools.chain(*data.values()))
    #         else:
    #             sub_categories: List = data[category]
    #         return sub_categories


    def request_sub_category(self, page: str) -> ResultSet:
        soup = BeautifulSoup(page, "html.parser")
        return soup.find_all(["div"], {"s-item__wrapper clearfix"})
    
    def get_bid_n_price(self, item: Tag) -> int and float:
        tag: Tag = item.find(["div"], {"class": "s-item__details clearfix"}) # Select <div> with bids and price
        bids: str = re.search(r"\d+\s+bids?", tag.find(["span"], {"class": lambda x: "bidCount" in x}).text).group(0) # Get bids tag value
        bids: int = int(re.sub(r"\D", "", bids)) # Get bids plain number
        price: str = tag.find(["span"], {"class": lambda x: "price" in x}).text # Get price tag value
        _price: float = float(re.sub(r"[^\d\.]", "", price)) # Remove everything but digits and dots for float
        
        # Check if bids meet the criteria
        if bids >= int(self.filters["bids"]) and int(_price) >= int(self.filters["price"]):
            return bids, price
        else: return False
    
    def get_image(self, item: Tag):
        images = item.find(["div"], {"class": "s-item__image-section"}).find_all(["img"])
        for x in images:
            if x['src'].split('.')[-1] == "gif":
                image = x['data-src']
            else:
                image = x['src']
            return image
        
    async def select_item(self, item: Tag) -> dict:
        info = dict()
        bids, price = self.get_bid_n_price(item)
        
        # Get item info
        info["bids"] = str(bids)
        info["price"] = str(price)
        info["title"] = re.sub(r"[\*\"\'\~\[\]\(\)]", "", item.find(["h3"]).text)
        info["url"] = item.find(["a"], {"class": "s-item__link"}).get("href")
        info["image"] = self.get_image(item)
        # Put the item into the sending queue
        await self.sending_queue.queue.put(info)


    async def parse_category(self, url: str, i: int):
        # MIMIC A DELAY BETWEEN REQUESTS
        await asyncio.sleep(i)
        
        try:
            params: dict = self.url_helper.get_parameters(url, self.filters["sold"])
            url: str = self.url_helper.remove_parameters(url)
            url: str = self.url_helper.link_proxy(url)
            
            # REQUEST PAGE HTML
            page, response_url = await self.request_page(url, params)
            # PARSE PAGE (SUB CATEGORY)
            all_items_on_page: ResultSet = self.request_sub_category(page)
            
            # VALIDATE IF ITEM MEETS THE BIDS AND PRICE CRITERIA & SEND TO TELEGRAM
            tasks = [
                asyncio.create_task(
                    self.select_item(item)) # Send to Telegram
                for item in all_items_on_page
                    if self.get_bid_n_price(item) # Include only items that meet criteria
                ]
            
            if tasks:
                await self.parsing_queue.queue.put(str(response_url)) # If current page has items that meet criteria, then do next page for this sub category
                await asyncio.gather(*tasks)
            
        except asyncio.CancelledError:
            print("CANCELLED TASK: process_sub_categories" + str(i))
            
        
        
    def print_filters(self):
        print(dedent(f'''\
            =============== FILTERS ===============
            USER: {self.user.username}
            SITE: Ebay
            CATEGORY: {self.filters["category"]}
            BIDS: {self.filters["bids"]}
            PRICE: {self.filters["price"]}
            SOLD: {self.filters["sold"]}
            =======================================
        '''))
    
    
    async def run(self) -> None:
        try: # Main TRY for the parsing process
            await asyncio.sleep(0)
            self.print_filters()
            
            category_list: list = self.start([self.filters["category"]])
            
            while category_list:
                for category in category_list:
                    try:
                        url: str = self.select_category(category) # Add category ID to base url
                        url: str = self.url_helper.link_proxy(url) # Add proxy
                        main_page, response_url = await self.request_page(url, params=None, base=True) # Get HTML for main page ebay.com/b/{categoryID}
                        
                        if main_page:
                            category_list.remove(category)
                            category_links: list[str] = self.get_sub_categories(main_page) # Get all sub categories in the elected category
                            self.url_helper.category_links.extend(category_links) # Pass links to url helper for visibility
                            await self.parsing_queue.add_to_queue(category_links) # Put urls in the parsing queue
                        
                    except (UnableToRetrieveResponse, ConcurrencyLimitExceeded,\
                        OutOfRequests, aiohttp.client_exceptions.TooManyRedirects, NoException) as err:
                        proxy.next_proxy() # Change proxy server
                
                
        # On parsing task cancel
        except asyncio.CancelledError:
            print("\nCANCELLED TASK: PARSER")