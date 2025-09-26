from src import db


class Valvulas(db.Model):
    __tablename__ = 'tb_valvula'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome_valvula = db.Column(db.String(120), nullable=False)
    local_valvula = db.Column(db.String(120), nullable=True)


    def __init__(self, nome, email, data_login, senha):
        self.__nome = nome #esat vindo da view
        self.__email = email
        self.__data_login = data_login
        self.__senha = senha