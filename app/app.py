import logging
from datetime import datetime
from flask import Flask, request
from db.db import get_user_data, create_app, delete_app
from app.logic import use_app, generate_randomized_week
app = Flask(__name__)

DEFAULT_UUID = 0
DEFAULT_DAYS_PER_WEEK = 7
DEFAULT_MINUTES_PER_DAY = 15

logging.basicConfig(
    format='%(asctime)s %(levelname)-4s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

@app.route('/apps', methods=['GET'])
def get_apps():
    app.logger.info("GET: Request received")
    app.logger.info(request.args)
    uuid = int(request.args.get('uuid', default = DEFAULT_UUID))
    user_data = get_user_data(uuid=uuid)

    dt = datetime.now()
    today = dt.strftime('%A').lower()
    user_apps = user_data["apps"]

    for user_app in user_apps.keys():
        todays_moderation = user_apps[user_app]["this_week"][today]
        del user_apps[user_app]["this_week"]
        user_apps[user_app]["today"] = todays_moderation

    response = {
        "apps": user_apps
    }

    return response

@app.route('/apps', methods=['POST'])
def use_app_for_user():
    app.logger.info("POST: Request received")
    app.logger.info(request.args.to_dict())
    uuid = int(request.args.get('uuid', default = DEFAULT_UUID))
    user_app = request.args.get('app')
    
    use_app(app=user_app, uuid=uuid)
    return "Success"

@app.route('/apps', methods=['PUT'])
def add_app_for_user():
    uuid = int(request.args.get('uuid', default = DEFAULT_UUID))
    app = request.args.get('app')
    
    this_week = generate_randomized_week(DEFAULT_DAYS_PER_WEEK)

    create_app(
        uuid=uuid,
        app=app,
        this_week_schedule=this_week,
    )

    return "Success"

@app.route('/apps', methods=['DELETE'])
def delete_app_for_user():
    uuid = int(request.args.get('uuid', default = DEFAULT_UUID))
    app = request.args.get('app')
    
    delete_app(
        uuid=uuid,
        app=app
    )

    return "Success"

if __name__ == "__main__":
    app.run()

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.DEBUG)
app.logger.debug('this will show in the log')