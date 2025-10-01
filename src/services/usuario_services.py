from src.models.usuario_models import Usuario
from src import db
from flask import flash, jsonify
from sqlalchemy.exc import SQLAlchemyError
from ..entities.usuario_entities import Usuario
from passlib.hash import pbkdf2_sha256


def cadastrar_usuario(usuario):
    usuario_db = Usuario(nome=usuario.nome, email=usuario.email, senha=usuario.senha)
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



def alterar_senha(usuario, senha, nova_senha, confirmar_senha):
    """Altera a senha do usuário, verificando se as senhas coincidem e se a senha atual está correta."""
    try:
        # Verifica se a nova senha e a confirmação são iguais
        if nova_senha != confirmar_senha:
            return jsonify({"message": "As senhas não coincidem!"}), 400

        # Verifica se a senha atual está correta
        if not usuario.verifica_senha(senha):
            return jsonify({"message": "Senha atual incorreta!"}), 400

        # Atualiza a senha do usuário
        usuario.senha = Usuario.gen_senha(nova_senha)
        db.session.commit()

        return jsonify({"message": "Senha alterada com sucesso!"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Erro ao atualizar a senha no banco de dados.", "error": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Erro inesperado ao alterar a senha.", "error": str(e)}), 500


def resetar_senha(usuario: Usuario, password):
    # Gera o hash da nova senha e atualiza no banco de dados
    usuario.password = pbkdf2_sha256.hash(password)
    db.session.commit()

    return jsonify({"message": "Senha redefinida com sucesso!"}), 200