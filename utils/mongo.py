from pymongo import MongoClient

USERNAME = 'your_username'
PASSWORD = 'your_password'
CONNECTION_STRING = f'mongodb+srv://{USERNAME}:{PASSWORD}@cluster0.qh8t139.mongodb.net/'
CLIENT = MongoClient(CONNECTION_STRING)