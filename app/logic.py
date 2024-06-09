from threading import Timer
from datetime import datetime
import random

from mongo.db import db
from scripts.run_script import whitelist, blacklist

def generate_randomized_week(days_per_week):
    weekly_values = ["usable" if (i < days_per_week) else "unusable" for i in range(7)]
    random.shuffle(weekly_values)
    
    weekly_values = map(lambda x : {"status": x}, weekly_values)
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    this_week = dict(zip(days_of_week, weekly_values))
    return this_week

def use_app(app, uuid = 0):
    dt = datetime.now()
    day = dt.strftime('%A').lower()

    user = db.thales.users.find_one({"uuid": uuid})
    minutes_per_day = user["apps"][app]["moderation"]["minutes_per_day"]
    
    users = db.thales.users
    users.update_one({"uuid": uuid}, { "$set": {
                                                    f"apps.{app}.this_week.{day}.status": "used",
                                                    f"apps.{app}.this_week.{day}.usage": minutes_per_day
                                                }
                    })

    whitelist(app)

    t = Timer(minutes_per_day * 60.0, blacklist, args=(app,))
    t.start()

