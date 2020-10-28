from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/testr.db'
app.secret_key = 'AJdfjasd8i0fawsjef'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models