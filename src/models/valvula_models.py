from src import db


class Valvulas(db.Model):
    __tablename__ = 'tb_valvulas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    nome_valvula = db.Column(db.String(120), nullable=False)
    local_valvula = db.Column(db.String(120), nullable=True)
