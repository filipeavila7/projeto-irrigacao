from src import db
from passlib.hash import pbkdf2_sha256 as sha256

class Usuario(db.Model):
    __tablename__ = 'tb_usuario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome = db.Column(db.String(120), nullable=False)                 
    email = db.Column(db.String(120), nullable=False, unique=True)  
    senha = db.Column(db.String(255), nullable=False)                
    data_login = db.Column(db.Datetime, nullable=False) 

    def __init__(self, nome, email, data_login, senha):
        self.__nome = nome #esat vindo da view
        self.__email = email
        self.__data_login = data_login
        self.__senha = senha

    # get e set para manipular os atributos encapsulados

    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, nome):
        self.nome = nome
        
    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.email = email
    
        
    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.senha = senha
    
    
    @property
    def data_login(self):
        return self.__data_login
    
    @data_login.setter
    def data_login(self, data_login):
        self.data_login = data_login


    # Gera o hash da senha e armazena no campo 'senha'
    def gen_senha(self, senha):
        self.senha = sha256.hash(senha)

    # Verifica se a senha informada corresponde ao hash armazenado
    def verificar_senha(self, senha):
        return sha256.verify(senha, self.senha)
    



    
        

