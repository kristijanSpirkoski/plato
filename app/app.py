import logging
from datetime import datetime
from flask import Flask, request
from app.logic import use_app, generate_randomized_week
from mongo.db import db
app = Flask(__name__)

DEFAULT_UUID = 0
DEFAULT_DAYS_PER_WEEK = 7
DEFAULT_MINUTES_PER_DAY = 15

logging.basicConfig(
    format='%(asctime)s %(levelname)-4s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/users/<uuid>/apps', methods=['GET'])
def get_apps(uuid):
    app.logger.info("GET: Request received")

    user = db.thales.users.find_one({"uuid": int(uuid)})
    dt = datetime.now()
    today = dt.strftime('%A').lower()
    user_apps = user["apps"]

    for user_app in user_apps.keys():
        todays_moderation = user_apps[user_app]["this_week"][today]
        del user_apps[user_app]["this_week"]
        user_apps[user_app]["today"] = todays_moderation

    response = {
        "apps": user_apps
    }

    return response

@app.route('/users/<uuid>/apps/<appId>', methods=['POST'])
def use_app_for_user(uuid, appId):
    app.logger.info("POST: Request received")
    app.logger.info(request.args.to_dict())
    
    use_app(app=appId, uuid=int(uuid))
    return "Success"

@app.route('/users/<uuid>/apps/<appId>', methods=['PUT'])
def add_app_for_user(uuid, appId):
    this_week = generate_randomized_week(DEFAULT_DAYS_PER_WEEK)

    users = db.thales.users
    app_obj = {
        "app_name": appId,
        "moderation": {
            "days_per_week": DEFAULT_DAYS_PER_WEEK,
            "minutes_per_day": DEFAULT_MINUTES_PER_DAY

        },
        "this_week": this_week
    }
    query = { "$set" : { f"apps.{appId.lower()}" : app_obj}}
    users.update_one({"uuid": int(uuid)}, query)

    return "Success"

@app.route('/users/<uuid>/apps/<appId>', methods=['DELETE'])
def delete_app_for_user(uuid, appId):
    users = db.thales.users
    query = { "$unset": { f"apps.{appId}": "" } }
    users.update_one({"uuid": int(uuid)}, query)

    return "Success"

if __name__ == "__main__":
    app.run()

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')