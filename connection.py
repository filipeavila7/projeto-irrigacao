from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()


SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
SECRET_KEY = os.getenv("SECRET_KEY")

#teste de conexão

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    connection = engine.connect()
    print("banco conectado")
except Exception as e:
    print(f"falha ao conectar {e}")