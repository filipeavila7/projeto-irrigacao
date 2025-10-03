import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

# instancias
app = Flask(__name__)
app.config.from_object("connection")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

app.secret_key = os.getenv("SECRET_KEY", "chave_insegura_padrao_para_dev")

# configuração de login
login_manager = LoginManager(app)
login_manager.login_view = "login"  # type: ignore

# configuracao email
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")


# Config JWT
app.config["JWT_SECRET_KEY"] = "uma_chave_secreta_qualquer"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
jwt = JWTManager(app)

# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src import routes

# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src.models import registro_models, usuario_models, valvula_models

# trunk-ignore(ruff/E402)
# trunk-ignore(ruff/F401)
from src.services import registro_services, usuario_services, valvula_services
