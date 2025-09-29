from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# instancias
app = Flask(__name__)
app.config.from_object('connection')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# configuração de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'



from src import models
from src import routes