from src import db

class Usuario(db.Model):
    __tablename__ = 'tb_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome = db.Column(db.String(120), nullable=False)                 
    email = db.Column(db.String(120), nullable=False, unique=True)  
    senha = db.Column(db.String(255), nullable=False)                
    data_login = db.Column(db.Date, nullable=False) 