from src import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'tb_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome = db.Column(db.String(120), nullable=False)                 
    email = db.Column(db.String(120), nullable=False, unique=True)  
    senha = db.Column(db.String(255), nullable=False)                


    
    # Gera o hash da senha e armazena no campo 'senha'
    def gen_senha(self, senha):
        self.senha = generate_password_hash(senha)

    # Verifica se a senha informada corresponde ao hash armazenado
    def verificar_senha(self, senha):
        return check_password_hash(self.senha, senha)
    





    
        

