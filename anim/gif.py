import json
import random

# Get gif urls from json file
def load_gifs() -> list[str]:
    with open("./json/anim.json", "r") as f:
        data: dict = json.load(f)
    return data["gifs"]

# Select random gif
def rand_gif(data: list[str]) -> str:
    gif: str = data[random.randint(0, len(data)-1)]
    return gif

# Return random gif
def get_gif() -> str:
    data: list[str] = load_gifs()
    gif: str = rand_gif(data)
    return gif