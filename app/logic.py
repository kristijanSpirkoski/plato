from threading import Timer
from datetime import datetime
import random

from db.db import update_app_allowed, get_user_data
from scripts.run_script import whitelist, blacklist

def generate_randomized_week(days_per_week):
    weekly_values = [(i < days_per_week) for i in range(7)]
    random.shuffle(weekly_values)
    
    weekly_values = map(lambda x : {"allowed": x, "visible": False}, weekly_values)
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    this_week = dict(zip(days_of_week, weekly_values))
    return this_week

def use_app(app, uuid = 0):
    dt = datetime.now()
    day = dt.strftime('%A').lower()

    user = get_user_data(uuid)
    minutes_per_day = user["apps"][app]["moderation"]["minutes_per_day"]

    update_app_allowed(
        uuid=uuid,
        app=app,
        day_of_week=day,
        is_allowed=False
    )
    whitelist(app)

    t = Timer(minutes_per_day * 60.0, blacklist, args=(app,))
    t.start()

