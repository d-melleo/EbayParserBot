import itertools
import json


JSON_PATH = "./json/proxy.json"

class Proxy:
    def __init__(self) -> None:
        # A list of proxy servers
        self.proxies: list = self.load_json()
        # Create a cycle iterator
        self.cycle_iterator = itertools.cycle(self.proxies)
        # Use the cycle iterator
        self.current: str = next(self.cycle_iterator)
        
        
    def load_json(self) -> list:
        with open(JSON_PATH, 'r') as file:
            data: dict = json.load(file)
            return data['proxies']
    
    def next_proxy(self):
        self.current = next(self.cycle_iterator)
        
    def validate_response(self, response_code: int):
        # 500 - After retrying for 60 seconds, the API was unable to receive a successful response.
        # 429 - You are sending requests too fast, and exceeding your concurrency limit.
        # 403 - You have used up all your API credits.
        if response_code in [500, 429, 403]:
            self.next_proxy()
        # if response_code == 200:
        #     raise NoException
        if response_code == 500:
            raise UnableToRetrieveResponse
        if response_code == 429:
            raise ConcurrencyLimitExceeded
        if response_code == 403:
            raise OutOfRequests


class NoException(Exception):
    def __init__(self, message = "All GOOD"):
        super().__init__(message)

class UnableToRetrieveResponse(Exception):
    def __init__(self, message = "500 - After retrying for 60 seconds, the API was unable to receive a successful response."):
        super().__init__(message)

class ConcurrencyLimitExceeded(Exception):
    def __init__(self, message = "429 - You are sending requests too fast, and exceeding your concurrency limit."):
        super().__init__(message)

class OutOfRequests(Exception):
    def __init__(self, message = "403 - You have used up all your API credits."):
        super().__init__(message)