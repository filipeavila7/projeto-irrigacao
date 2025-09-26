from src import db

class Registro(db.Model):
    __tablename__ = 'tb_registro'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    status = db.Column(db.Boolean, nullable=False)
    data_acionamento = db.Column(db.Datetime, nullable=False)    

    # chaves estrangeiras 
    id_usuario = db.Column(db.Integer, db.ForeignKey('tb_usuario.id'), nullable=False)             
    id_valvula = db.Column(db.Integer, db.ForeignKey('tb_valvula.id'), nullable=False)             

    # Relacionamentos com outras tabelas
    usuario = db.relationship("Usuario", backref="tb_registro")  
    valvula = db.relationship("Valvula", backref="tb_valvula")  