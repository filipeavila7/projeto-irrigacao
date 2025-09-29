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



    def __init__(self, status, dt_acionamento, id_valvula,id_usuario ):
      self.__status = status
      self.__dt_acionamento = dt_acionamento
      self.__id_valvula = id_valvula
      self.__id_usuario = id_usuario

   # get e set para manipular os atributos encapsulados

    @property
    def status(self):
      return self.__status
   
    @status.setter
    def status(self, status):
      self.status = status

    @property
    def dt_acionamento(self):
      return self.__dt_acionamento
   
    @dt_acionamento.setter
    def dt_acionamento(self, dt_acionamento):
      self.dt_acionamento = dt_acionamento

    @property
    def id_valvula(self):
      return self.__id_valvula
   
    @id_valvula.setter
    def id_valvula(self, id_valvula):
      self.id_valvula = id_valvula

    @property
    def id_usuario(self):
      return self.__id_usuario
   
    @id_usuario.setter
    def id_usuario(self, id_usuario):
      self.id_usuario = id_usuario



    
        

