from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from db.credentials import uri

# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
def ping():
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

def create_user(uuid, email, first_name, last_name):
    db = client.thales
    users = db.users

    user = {
        "uuid": uuid,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "apps": {},
    }

    users.insert_one(user)

def create_app(app, this_week_schedule, uuid = 0, days_per_week = 7, minutes_per_day = 15):
    users = client.thales.users

    app_obj = {
        "app_name": app,
        "moderation": {
            "days_per_week": days_per_week,
            "minutes_per_day": minutes_per_day

        },
        "this_week": this_week_schedule
    }

    query = { "$set" : { f"apps.{app.lower()}" : app_obj}}

    users.update_one({"uuid": uuid}, query)

def delete_app(app, uuid = 0):
    users = client.thales.users

    query = { "$unset": { f"apps.{app}": "" } }

    users.update_one({"uuid": uuid}, query)

    return "Success"


def insert_read():
    db = client.thales
    users = db.users
    user = {
        "uuid": 0
    }

    users.insert_one(user)

    read_user = users.find_one({"uuid": 0})

def delete_all():
    db = client.thales
    users = db.users
    users.delete_many({})

def get_user_data(uuid = 0):
    users = client.thales.users
    user = users.find_one({"uuid": uuid})
    return user

def update_app_allowed(app, day_of_week, is_allowed, uuid = 0):
    users = client.thales.users

    users.update_one({"uuid": uuid}, { "$set": {f"apps.{app}.this_week.{day_of_week}.allowed": is_allowed}})