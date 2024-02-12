from random import randint
from bs4 import BeautifulSoup
import requests

class Emoji:
    def __init__(self):
        self.emoji_list: list[str] = []
        self.list_indexes: list[str] = [0,1,2,3,4,8,9,10,11,12,13,17] # Select emoji sections from website
    
    # Request page
    def get_emoji(self) -> str:
        with requests.get("https://getemoji.com/") as response:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup

    # Parse emoji and get them in a list
    def filter_emoji(self, soup: str) -> list[str]:
        for i in self.list_indexes:
            l = soup.find_all(["p"], {"style": "font-family: Segoe UI Emoji; font-size: 3.5em"})[i].string.strip()
            self.emoji_list.extend(l.split('\n'))

    # Return random emoji as string
    def rand_emoji(self, emoji: int = 1, select: list[str] = None) -> str:
        if select:
            emoji_list = select
        else:
            emoji_list = self.emoji_list
            
        emojies: str = ''
        for i in range(emoji):
            emojies += emoji_list[randint(0, len(emoji_list)-1)]
        return emojies

    # Load emojies. Get ready for usage.
    def run(self) -> None:
        soup = self.get_emoji()
        self.filter_emoji(soup)