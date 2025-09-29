from src import app
from flask import render_template, redirect, jsonify, request, url_for
from flask_login import login_user, logout_user, login_required
from src.models.usuario_models import Usuario
from src.services.usuario_services import cadastrar_usuario, listar_usuario_email


# ------------ ROTA DE INICIAL --------------------

@app.route('/')
def index():
    return render_template('index.html')


# ------------ ROTA DE LOGIN --------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # se o método for post:
    if request.method == 'POST':
        try:
            # Se enviar JSON no corpo:
            data = request.get_json()
            # pega o email e senha via json do formulario
            email = data.get('email') if data else None
            senha = data.get('senha') if data else None

            # Se enviar form-data, use:
            # email = request.form.get('email')
            # senha = request.form.get('senha')

            print(f"Tentando login com: {email} / {senha}")

            # caso o usuário não forneça email e nem senha
            if not email or not senha:
                return jsonify({"message": "E-mail e senha são obrigatórios"}), 400

            # variável de listar usuário pelo email
            usuario_encontrado = listar_usuario_email(email)

            if usuario_encontrado and usuario_encontrado.verifica_senha(senha):
                login_user(usuario_encontrado)
                return jsonify({"success": True, "redirect_url": url_for('painel_admin')})

            print("Senha incorreta ou usuário não encontrado")
            return jsonify({"message": "Usuário ou senha inválidos."}), 401

        except Exception as e:
            print("Erro no login:", str(e))
            return jsonify({"message": "Erro interno", "error": str(e)}), 500

    return render_template("login.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))




# ------------ ROTA DE usuario --------------------
@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def rota_cadastro_usuario():
    if request.method == 'POST':
        try:
            # 🔹 Captura os dados enviados pelo formulário
            nome = request.form.get('nome')
            email = request.form.get('email')
            senha = request.form.get('senha')  # se houver senha, criptografe antes de salvar!

            # 🔹 Chama o service responsável por cadastrar o usuário
            cadastrar_usuario(nome, email, senha)

            return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

        except ValueError as ve:
            # Erros de validação (ex.: email inválido, nome vazio, etc.)
            return jsonify({"message": str(ve)}), 400

        except Exception as e:
            # Erros inesperados no banco ou no backend
            return jsonify({"message": "Erro ao cadastrar usuário."}), 500

    # 🔹 Para requisições GET, apenas renderiza a página do painel ou formulário
    return render_template('painel_admin.html')