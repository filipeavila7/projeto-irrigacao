from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from src.models.usuario_models import Usuario

# instancias
app = Flask(__name__)
app.config.from_object('connection')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# configuração de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# função de carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

from src import models
from src import routes