import datetime
import re
from aiogram import types
from pymongo import MongoClient


def get_user_from_callback(callback_query) -> list:
    # types.Message
    try: 
        _id: int = callback_query.from_id
        username: str = callback_query.from_user.username
    
    # types.CallbackQuery
    except AttributeError: # 'CallbackQuery' object has no attribute 'from_id'
        _id: int = callback_query.from_user.id
        username: str = callback_query.from_user.username
    
    return _id, username


class UserData:
    def __init__(self, client: MongoClient, callback_query: types.Message or types.CallbackQuery) -> None:
        # Mongo DB
        self.db = client['ParserBot']
        self.collection = self.db['userdata']
        # User identity from Telegram
        self._id: int = get_user_from_callback(callback_query)[0] # From telegram get user ID 
        self.username: str = get_user_from_callback(callback_query)[1] # From telegram get username
        # User default settings
        self.language: str = "en" # Set a default language
        self.msg_send_at_once: int = 5 # Set default number of msg to be sent before captcha
        self.last_choice = None # Last category parsed
        # Get user
        self.on_init()


    def on_init(self) -> None:
        self.fetch_document() # Read user from DB if exists, otherwise create one
        self.fetch_settings() # Set user details/settings in the class
        
        
    def fetch_document(self) -> None:
        db_user: dict = self.get_user_from_db(self._id)
        if db_user: # If user exists in database, check if username has changed
            self.validate_username(db_user, self.username)
        elif not db_user: # Add user to the database
            self.collection.insert_one({'_id': self._id, 'username': self.username, **self.default_values()})
            
            
    def fetch_settings(self) -> None:
        db_user: dict = self.get_user_from_db(self._id)
        # Update user info in the class
        self.username = db_user['username'] # Username can change, keep a track of it as well
        self.language = db_user['language']
        self.msg_send_at_once = db_user['msg_send_at_once']
        self.last_choice = db_user['last_choice']
        
        
    def get_user_from_db(self, _id: str) -> dict:
        db_user: dict = self.collection.find_one({"_id": _id})
        return db_user
    
    
    def validate_username(self, db_user: dict, username: str) -> None:
        # Update username, if user changed it
        if username != db_user['username']:
            self.collection.update_one({'_id': db_user['_id']}, {'$set': {'username': username}})
            
            
    def default_values(self) -> dict:
        settings = {
            'registration_date': datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0),
            'language': self.language,
            'msg_send_at_once': self.msg_send_at_once,
            'last_choice': self.last_choice}
        return settings
    
    
    def update_language(self, callback_query: types.CallbackQuery):
        language: str = callback_query.data.split('_')[1]
        self.collection.update_one({'_id': self._id}, {'$set': {'language': language}})
        self.language = language
    
    
    # Settings. Set number of messages to be sent before prompt pops up.
    def update_msg_at_once(self, callback_query: types.CallbackQuery) -> int:
        msg_at_once: str = re.sub(r"\D", "", callback_query.data)
        self.collection.update_one({'_id': self._id}, {'$set': {'msg_send_at_once': int(msg_at_once)}})
        self.msg_send_at_once = int(msg_at_once)


    def update_last_choice(self, filters: dict) -> dict:
        self.collection.update_one({'_id': self._id}, {'$set': {'last_choice': filters}})
        self.last_choice = filters