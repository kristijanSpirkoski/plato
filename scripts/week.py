from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from app.logic import generate_randomized_week
from db.db import ping
from db.credentials import uri


client = MongoClient(uri, server_api=ServerApi('1'))

def run_weekly_random_engine(uuid = 0):
    ping()
    db = client.thales
    users = db.users

    user = users.find_one({"uuid": uuid})

    for app in user["apps"].keys():
        days_per_week = user["apps"][app]["moderation"]["days_per_week"]

        this_week = generate_randomized_week(days_per_week)

        users.update_one({"uuid": uuid}, { "$set": {f"apps.{app}.this_week": this_week}})

run_weekly_random_engine()