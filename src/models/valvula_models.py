from src import db


class Valvulas(db.Model):
    __tablename__ = 'tb_valvula'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome_valvula = db.Column(db.String(120), nullable=False)
    local_valvula = db.Column(db.String(120), nullable=True)


    def __init__(self, nome_valvula, local_valvula):
        self.__nome_valvula = nome_valvula 
        self.__local_valvula = local_valvula
       
        