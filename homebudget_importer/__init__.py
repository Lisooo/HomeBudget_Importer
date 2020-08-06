from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from homebudget_importer.config import Config

# APP
app = Flask(__name__)
app.config.from_object(Config)

# DB
db = SQLAlchemy(app)

from homebudget_importer.main import utils as main

# EXECUTIVE APP
importer = main.importer()