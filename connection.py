import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

# Basic config pulled from env
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE = os.getenv("DATABASE")
_port_env = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
USER = os.getenv("USER")

# Try to parse port as int if provided; otherwise leave as None
try:
    PORT = int(_port_env) if _port_env not in (None, "", "None") else None
except ValueError:
    # If someone set an invalid port string, treat it as unset
    PORT = None

# Build SQLALCHEMY_DATABASE_URI safely. If core DB vars are missing, fall back to sqlite.
if USER and PASSWORD and HOST and DATABASE:
    # include port only when available
    if PORT:
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
else:
    # Fallback for development/local runs
    SQLALCHEMY_DATABASE_URI = f"sqlite:///./{DATABASE or 'app.db'}"

SQLALCHEMY_TRACK_MODIFICATIONS = True

# Test connection only when using a non-sqlite DB to avoid spurious errors during import
if SQLALCHEMY_DATABASE_URI.startswith("sqlite:"):
    # skip create_engine test for sqlite fallback
    pass
else:
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URI)
        connection = engine.connect()
        print("banco conectado")
        connection.close()
    except Exception as e:
        # print error but don't raise at import time
        print(f"falha ao conectar {e}")
