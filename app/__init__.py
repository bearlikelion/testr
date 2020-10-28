import os
import sys
import yaml

from cvpysdk.commcell import Commcell
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/testr.db'
app.secret_key = 'AJdfjasd8i0fawsjef'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

with open("config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        raise exc

cs = Commcell(config['cshostname'], config['username'], config['password'])

from app import routes, models, testcase