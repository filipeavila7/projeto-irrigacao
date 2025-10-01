class Usuario:
    def __init__(self, name, email, senha):
        self.__name = name
        self.__email = email
        self.__senha = senha
  

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, senha):
        self.__senha = senha

    @property
    def ativo(self):
        return self.__ativo
    
    @ativo.setter
    def ativo(self, ativo):
        self.__ativo = ativo