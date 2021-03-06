import os
import sys
import yaml
import logging

from cvpysdk.commcell import Commcell
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if not os.path.exists('logs/testr.log'):
    with open('logs/testr.log', 'w+') as logfile:
        print("Initalized new log file")
        logfile.close()

if not os.path.exists('app/db/testr.db'):
    with open('app/db/testr.db', 'w+') as database:
        print()
        print('[ERROR]: Testr DB does not exist, creating empty file, please run following commands:')
        print('    flask db init')
        print('    flask db migrate')
        print('    flask db upgrade')
        database.close()
        os._exit(0)

# File Config
with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise exc

# Flask App Config
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/testr.db'
app.secret_key = config['secret_key']

# Logging
logFormatStr = '[%(asctime)s]{%(module)s:%(lineno)d} %(levelname)s - %(message)s'
logging.basicConfig(format = logFormatStr, filename='logs/testr.log', level=logging.INFO)
formatter = logging.Formatter(logFormatStr,'%m-%d %H:%M:%S')

fileHandler = logging.FileHandler("logs/testr.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.DEBUG)
streamHandler.setFormatter(formatter)

werkzeuglog = logging.getLogger('werkzeug')
werkzeuglog.setLevel(logging.ERROR)

app.logger.addHandler(fileHandler)
app.logger.addHandler(streamHandler)

# Sqlite DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Commserv Object
cs = Commcell(config['cshostname'], config['username'], config['password'])
log = app.logger

from app import routes, models, testcase

@app.template_filter('time')
def format_datetime(value, format="%m-%d-%Y %H:%M:%S"):
    """Format a date time"""
    if value is None:
        return ""
    return value.strftime(format)

# Don't insert to DB if we are using flask db
if len(sys.argv) > 1:
    if not sys.argv[1]=='db':
        if models.Commserv.query.all():
            models.Commserv.query.delete()

        commcell = models.Commserv(
            name = cs.commserv_name,
            hostname = cs.commserv_hostname,
            servicepack = cs.commserv_version,
            username = config['username'],
            password = config['password']
        )

        db.session.add(commcell)
        db.session.commit()

        app.logger.info("Added Commvault Info to DB")
