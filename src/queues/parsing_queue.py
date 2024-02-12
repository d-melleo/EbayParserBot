import asyncio
from src.ebay import helper


class ParsingQueue:
    def __init__(self, ebay) -> None:
        self.ebay = ebay
        self.queue = asyncio.Queue()
        self.started: bool = False

    async def add_to_queue(self, links: list) -> None:
        for link in links:
            await self.queue.put(link)

    async def execute_tasks(self, links: list):
        # Crete a task for each sub category
        tasks = [
            asyncio.create_task(
                self.ebay.parser.parse_category(url = url,
                    i = links.index(url)), # index number will be used for sleep to slow down requests
                name = f"process_sub_categories{links.index(url)}"
                ) for url in links
            ]
        
        if not self.started:
            self.started = True
            self.ebay.sending_queue.started = True # Let the sending queue know that parsing has started
            
        await asyncio.gather(*tasks)


    async def run(self):
        try: 
            while True:
                links = list()
                while not self.queue.empty():
                    link: str = self.queue.get_nowait()
                    links.append(link)
                    
                if links:
                    await self.execute_tasks(links)
                
                running: bool = helper.validate_task_running("sending_queue")
                await asyncio.sleep(1)
                if not running:
                    print("\n*******BREAK OUT OF THE PARSING QUEUE*******")
                    break
        except asyncio.CancelledError:
            print("\nCANCELLED TASK: PARSING QUEUE")