from src.models.usuario_models import Usuario
from src import db



def cadastrar_usuario(usuario):
    usuario_db = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
    #usuario_db.gen_senha(usuario.senha)
    db.session.add(usuario_db)
    db.session.commit()
    return usuario_db


def listar_usuario():
    usuario_db = Usuario.query.all()
    return usuario_db



def listr_usuario_id(id):
    usuario_encontrado = Usuario.query.get(id)
    return usuario_encontrado
    

def listar_usuario_email(email):
    usuario_encontrado = Usuario.query.filter_by(email=email).first()
    return usuario_encontrado