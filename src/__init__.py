from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config.from_object('connection')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
