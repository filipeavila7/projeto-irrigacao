from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object('connection')

# Config JWT
app.config['JWT_SECRET_KEY'] = 'uma_chave_secreta_qualquer'
app.config['JWT_TOKEN_LOCATION'] = ['headers']

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

from src import routes, models, services