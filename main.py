import asyncio
from src.telegram.handlers import command_handler
from utils.loader import dp


if __name__ == "__main__":
    command_handler.CommandHandler(dp)
    asyncio.run(dp.start_polling())