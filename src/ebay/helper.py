import aiohttp
import asyncio
import itertools
import re
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from src.queues.parsing_queue import ParsingQueue
from utils import config
from utils.loader import proxy as PROXY


################### CANCEL PARSING TASKS #######################
async def cancel_tasks(*task_names) -> None:
    # Get all tasks
    tasks: set = asyncio.all_tasks()
    # Cancel tasks
    for task in tasks:
        for task_name in task_names:
            name: str = task.get_name()
            if name.startswith(task_name):
                task.cancel()
                print(f"\nCANCELLED TASK: {name}")
    
################### CHECK IF TASK IS RUNNING ##################
def validate_task_running(*task_names: list) -> bool:
    # Check if parsing is still running
    running = [task for task in asyncio.all_tasks() if (lambda x: task.get_name().startswith(x), task_names)]
    if running:
        return True


######################## URL EDITOR ############################
class UrlHelper:
    def __init__(self):
        self.category_links: list[str] = []
    
    def get_parameters(self, url: str, sold: bool) -> dict:
        parameters = dict()
        parameters['LH_Auction'] = '1' # Search in auction
        parameters['_sop'] = '5' # Sort from most bids to less
        parameters['_pgn'] = self.get_page(url) # Get page number
        if sold:
            parameters['LH_Sold'] = '1' # Search sold items
        return parameters
    
    def get_page(self, url: str) -> str:
        next_page: int = 1
        if "_pgn=" in url:
            page = re.search(r"(_pgn=\d*)", url)
            page = re.sub(r"\D", "", page.group(0))
            next_page = int(page) + 1
        return str(next_page)
    
    def remove_parameters(self, url: str) -> str:
        for link in self.category_links:
            if link in url:
                return link
    
    
    def revert_page(self, url: str) -> str:
        page = int(self.get_page(url))
        if page > 2:
            current_page = re.search(r"(_pgn=\d*)", url)
            url = re.sub(current_page, '', url)
            url = f'{url}&_pgn={page-2}'
        return url
    
    def link_proxy(self, url: str) -> str:
        proxy: str = PROXY.current
        proxy_domain: str = f"http://api.scraperapi.com/?api_key={proxy}&url="
        
        if config.ENABLE_PROXY:
            url: str = f"{proxy_domain}{url}?"
        return url
