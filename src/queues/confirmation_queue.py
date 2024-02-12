import asyncio

queue = asyncio.Queue(maxsize=1) # Initiate the queue
# Await for user input
async def get_input() -> bool:
    while True:
        if not queue.empty():
            input: bool = await queue.get()
            return input
        await asyncio.sleep(1)