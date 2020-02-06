from flask_pymongo import PyMongo
from app import mongo,user_collection
class User:
    def __init__(self,username):
        self.name=name
        user_dict=user_collection.find_one({"uname":username})
        if user_dict:
            self.events=user_dict['events']
            
        