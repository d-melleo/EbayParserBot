import aiogram
import asyncio
from src.ebay import helper
from src.telegram.handlers import command_handler, send_message
from src.telegram.handlers.markup_handler import MarkupHandler
from src.telegram.handlers.text_handler import TextHandler
from src.user.userdata import UserData
from utils import config



class SendingQueue:
    def __init__(self, callback_query: aiogram.types.CallbackQuery, user: UserData, text: TextHandler, markup: MarkupHandler):
        self.started: bool = False
        self.queue = asyncio.Queue()
        self.callback_query = callback_query
        self.user = user
        self.text = text
        self.markup = markup
    
    
    # Queue worker that messages items to telegram
    async def run(self):
        counter = 0
        
        while True:
            if self.started:
                await asyncio.sleep(0)
                self.print_q_size()
                
                if not self.queue.empty():
                    item = await self.queue.get() # Get item from the queue
                    self.print_item(item)
                    await send_message.send_item(self.callback_query, item, self.text, self.markup) # Send to telegram
                    counter += 1 # Add 1 to counter
                    
                    if counter == self.user.msg_send_at_once: # If items were sent, ask if to continue sending more
                        answer: bool = await command_handler.CommandHandler.sending_captcha(self.callback_query, self.queue.qsize(), self.text, self.markup)
                        print("\nCONTINUE SENDING = " + str(answer).upper() + "\n")
                        
                        if answer == True:
                            counter = 0
                            await self.sort_queue()
                            continue
                        elif answer == False:
                            await command_handler.CommandHandler.stop_sending(self.callback_query, self.text, self.markup)
                            print("\n*******BREAK OUT OF THE SENDING QUEUE*******")
                            break
                            
                else:
                    # If queue is empty, check if there're still running parsing tasks
                    running: bool = helper.validate_task_running("process_sub_categories", "parsing_queue")
                    if not running: # Break out of the loop if no parsing tasks are running
                        print("\n*******BREAK OUT OF THE SENDING QUEUE PARSING NOT RUNNING*******")
                        break
                        
            await asyncio.sleep(config.MSG_DELAY)


    async def sort_queue(self) -> None:
        # Get all items in queue
        queue_items = self.queue._queue 
        # Get all items from queue sorted by most bids first
        most_bids_first: list[dict] = sorted(queue_items, key=lambda x: x['bids'], reverse=True)
        
        while not self.queue.empty(): # Remove all items from queue
            self.queue.get_nowait()
        for item in most_bids_first: # Add sorted items back in queue
            self.queue.put_nowait(item)


    def print_q_size(self) -> None:
        print(f'\n******************* QUEUE SIZE {self.queue.qsize()} *******************')
    def print_item(self, item: dict):
        print(f"\n{item.items()}")