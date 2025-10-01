from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_mail import Mail
import os
from flask_jwt_extended import JWTManager


load_dotenv()

# instancias
app = Flask(__name__)
app.config.from_object('connection')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

app.secret_key = os.getenv("SECRET_KEY", "chave_insegura_padrao_para_dev")

# configuração de login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#configuracao email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')


# Config JWT
app.config['JWT_SECRET_KEY'] = 'uma_chave_secreta_qualquer'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
jwt = JWTManager(app)

from src.models import usuario_models, valvula_models, registro_models
from src import routes
from src.services import usuario_services, valvula_services, registro_services