from src import app
from flask import render_template, redirect, jsonify, request, url_for
from flask_login import login_user, logout_user, login_required
from src.models import usuario_models
from src.services.usuario_services import cadastrar_usuario, listar_usuario_email
from src import login_manager


# ------------ ROTA DE INICIAL --------------------

@app.route('/')
def index():
    return render_template('index.html')



# função de carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return usuario_models.Usuario.query.get(int(user_id))

# ------------ ROTA DE LOGIN --------------------


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.json.get('email')
            senha = request.json.get('senha')
            print(f"Tentando login com: {email} / {senha}")

            if not email or not senha:
                return jsonify({"message": "E-mail e senha são obrigatórios"}), 400

            usuario_encontrado = usuario_models.Usuario.query.filter_by(email=email).first()

            print(usuario_encontrado)
            print(usuario_encontrado.senha)

            if usuario_encontrado and usuario_encontrado.verificar_senha(senha):
                login_user(usuario_encontrado)

                return jsonify({"success": True, "redirect_url": url_for('index')})
            else:
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




@app.route('/cadastro_usuario', methods=['GET', 'POST'])
def rota_cadastro_usuario():
    if request.method == 'POST':
        try:
            print("Recebendo requisição POST em /cadastro_usuario")

            data = request.get_json()
            print(f"Dados recebidos: {data}")

            nome = data.get('nome')
            email = data.get('email')
            senha = data.get('senha')

            if not nome or not email or not senha:
                print("Faltando campos obrigatórios")
                return jsonify({"message": "Nome, email e senha são obrigatórios."}), 400

            # Cria usuário sem senha em claro e gera o hash
            usuario = usuario_models.Usuario(nome=nome, email=email, senha="")
            usuario.gen_senha(senha)

            # DEBUG: mostra o hash gerado (somente em ambiente de desenvolvimento)
            print(f"Senha original: {senha}")
            print(f"Senha hash gerada: {usuario.senha}")

            # DEBUG: verifica se o hash confere com a senha fornecida
            ok = usuario.verificar_senha(senha)
            print(f"Verificação do hash com a senha original: {ok}")

            # Chama service para persistir
            cadastrar_usuario(usuario)
            print("Usuário cadastrado com sucesso!")

            return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201

        except ValueError as ve:
            print(f"Erro de validação: {ve}")
            return jsonify({"message": str(ve)}), 400

        except Exception as e:
            print(f"Erro inesperado no cadastro: {e}", flush=True)
            import traceback
            traceback.print_exc()
            return jsonify({"message": "Erro ao cadastrar usuário.", "error": str(e)}), 500

    # Se for GET, apenas renderiza o formulário
    print("Requisição GET em /cadastro_usuario")
    return render_template('cadastro_usuario.html')
