from src import app
from flask import render_template, redirect, jsonify, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from src.models import usuario_models
from src.services.usuario_services import cadastrar_usuario, listar_usuario_email
from src import login_manager
from datetime import datetime
from src.services.registro_services import RegistroService
from src.services.valvula_services import ValvulaService


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
            data = request.get_json()
            if not data:
                return jsonify({"message": "JSON inválido ou não enviado"}), 400

            email = data.get('email')
            senha = data.get('senha')
            print(f"Tentando login com: {email} / {senha}")

            if not email or not senha:
                return jsonify({"message": "E-mail e senha são obrigatórios"}), 400

            usuario_encontrado = usuario_models.Usuario.query.filter_by(email=email).first()

            print(usuario_encontrado)
            print(usuario_encontrado.senha if usuario_encontrado else "Usuário não encontrado")

            if usuario_encontrado and usuario_encontrado.senha == senha:
                login_user(usuario_encontrado)
                # Retornar JSON com a URL para redirecionar
                return jsonify({"redirect_url": url_for("index")})

            else:
                print("Senha incorreta ou usuário não encontrado")
                return jsonify({"message": "Usuário ou senha inválidos."}), 401

        except Exception as e:
            print("Erro no login:", str(e))
            return jsonify({"message": "Erro interno", "error": str(e)}), 500

    return render_template("login.html")



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

            # Cria usuário com senha em texto claro (sem hash)
            usuario = usuario_models.Usuario(nome=nome, email=email, senha=senha)

            # DEBUG: mostra a senha armazenada (em texto claro)
            print(f"Senha original: {senha}")
            print(f"Senha armazenada: {usuario.senha}")

            # Salva no banco
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




# ============================================================
# ROTAS REGISTROS (CRUD)
# ============================================================

@app.route('/api/registros/', methods=['POST'])
@login_required
def criar_registro():
    """
    POST /api/registros/
    
    Cria um novo registro de acionamento de válvula
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body (JSON):
        {
            "status": true/false,
            "id_valvula": int
        }
    
    Returns:
        201: Registro criado com sucesso
        400: Dados inválidos
        401: Não autenticado
        500: Erro interno
    """
    try:
        usuario_id = current_user.id
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Dados não fornecidos'
            }), 400
        
        status = dados.get('status')
        id_valvula = dados.get('id_valvula')
        
        # Validações
        if status is None:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Status é obrigatório'
            }), 400
        
        if not isinstance(status, bool):
            return jsonify({
                'sucesso': False,
                'mensagem': 'Status deve ser boolean (true/false)'
            }), 400
        
        if id_valvula is None:
            return jsonify({
                'sucesso': False,
                'mensagem': 'ID da válvula é obrigatório'
            }), 400
        
        # Cria o registro usando o service
        resultado = RegistroService.criar_registro(
            status=status,
            id_usuario=usuario_id,
            id_valvula=id_valvula
        )
        
        if resultado['sucesso']:
            return jsonify(resultado), 201
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao criar registro: {str(e)}'
        }), 500


@app.route('/api/registros/<int:id_registro>', methods=['GET'])
@login_required
def obter_registro(id_registro):
    """
    GET /api/registros/<id_registro>
    
    Obtém um registro específico pelo ID
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_registro: ID do registro
    
    Returns:
        200: Dados do registro
        404: Registro não encontrado
        401: Não autenticado
    """
    try:
        registro = RegistroService.buscar_por_id(id_registro)
        
        if not registro:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Registro não encontrado'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'dados': {
                'id': registro.id,
                'status': registro.status,
                'status_texto': 'ATIVADA' if registro.status else 'DESATIVADA',
                'data_acionamento': registro.data_acionamento.isoformat(),
                'id_usuario': registro.id_usuario,
                'id_valvula': registro.id_valvula
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao obter registro: {str(e)}'
        }), 500


# ============================================================
# ROTAS DE LISTAGEM E CONSULTA
# ============================================================

@app.route('/api/registros/', methods=['GET'])
@login_required
def listar_registros():
    """
    GET /api/registros/
    
    Lista registros com paginação
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Lista de registros
        401: Não autenticado
        500: Erro interno
    """
    try:
        registros = RegistroService.listar_todos()
        
        registros_lista = [{
            'id': r.id,
            'status': r.status,
            'status_texto': 'ATIVADA' if r.status else 'DESATIVADA',
            'data_acionamento': r.data_acionamento.isoformat(),
            'id_usuario': r.id_usuario,
            'id_valvula': r.id_valvula
        } for r in registros]
        
        return jsonify({
            'total': len(registros_lista),
            'registros': registros_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao listar registros: {str(e)}'
        }), 500


@app.route('/api/registros/valvula/<int:id_valvula>', methods=['GET'])
@login_required
def listar_por_valvula(id_valvula):
    """
    GET /api/registros/valvula/<id_valvula>
    
    Lista registros de uma válvula específica
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Returns:
        200: Lista de registros
        401: Não autenticado
        500: Erro interno
    """
    try:
        
        registros = RegistroService.buscar_por_valvula(id_valvula)
        
        registros_lista = [{
            'id': r.id,
            'status': r.status,
            'status_texto': 'ATIVADA' if r.status else 'DESATIVADA',
            'data_acionamento': r.data_acionamento.isoformat(),
            'id_usuario': r.id_usuario,
            'id_valvula': r.id_valvula
        } for r in registros]
        
        return jsonify({
            'sucesso': True,
            'valvula_id': id_valvula,
            'total': len(registros_lista),
            'registros': registros_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao listar registros da válvula: {str(e)}'
        }), 500

# ============================================================
# ROTAS VALVULAS (CRUD)
# ============================================================

@app.route('/valvulas/cadastro', methods=['GET', 'POST'])
@login_required
def cadastro_valvula():
    if request.method == 'POST':
        try:
            dados = request.get_json()  # se o formulário enviar via form, não JSON
            
            nome_valvula = dados.get('nome_valvula')
            local_valvula = dados.get('local_valvula')
            
            if not nome_valvula:
                return render_template('cadastro_valvula.html', mensagem='Nome da válvula é obrigatório')
            
            resultado = ValvulaService.criar_valvula(
                nome_valvula=nome_valvula,
                local_valvula=local_valvula
            )
            
            if resultado['sucesso']:
                return render_template('cadastro_valvula.html', mensagem='Válvula criada com sucesso!')
            else:
                return render_template('cadastro_valvula.html', mensagem=resultado['mensagem'])
            
        except Exception as e:
            return render_template('cadastro_valvula.html', mensagem=f'Erro: {str(e)}')
    else:
        # GET - só exibe o formulário
        return render_template('cadastro_valvula.html')

    


@app.route('/api/valvulas/', methods=['GET'])
@login_required
def listar_valvulas():
    """
    GET /api/valvulas/
    
    Lista todas as válvulas cadastradas
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Lista de válvulas
        401: Não autenticado
        500: Erro interno
    """
    try:
        valvulas = ValvulaService.listar_todas()
        
        valvulas_lista = [{
            'id': v.id,
            'nome_valvula': v.nome_valvula,
            'local_valvula': v.local_valvula
        } for v in valvulas]
        
        return jsonify({
            'sucesso': True,
            'total': len(valvulas_lista),
            'valvulas': valvulas_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao listar válvulas: {str(e)}'
        }), 500


@app.route('/api/valvulas/<int:id_valvula>', methods=['GET'])
@login_required
def obter_valvula(id_valvula):
    """
    GET /api/valvulas/<id_valvula>
    
    Obtém informações de uma válvula específica
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Returns:
        200: Dados da válvula
        404: Válvula não encontrada
        401: Não autenticado
    """
    try:
        valvula = ValvulaService.buscar_por_id(id_valvula)
        
        if not valvula:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Válvula não encontrada'
            }), 404
        
        return jsonify({
            'sucesso': True,
            'dados': {
                'id': valvula.id,
                'nome_valvula': valvula.nome_valvula,
                'local_valvula': valvula.local_valvula
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao obter válvula: {str(e)}'
        }), 500


@app.route('/api/valvulas/<int:id_valvula>', methods=['PUT'])
@login_required
def atualizar_valvula(id_valvula):
    """
    PUT /api/valvulas/<id_valvula>
    
    Atualiza informações de uma válvula
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Body (JSON) - Todos os campos são opcionais:
        {
            "nome_valvula": "string",
            "local_valvula": "string"
        }
    
    Returns:
        200: Válvula atualizada
        400: Dados inválidos
        404: Válvula não encontrada
        401: Não autenticado
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nenhum dado fornecido'
            }), 400
        
        resultado = ValvulaService.atualizar_valvula(
            id_valvula=id_valvula,
            nome_valvula=dados.get('nome_valvula'),
            local_valvula=dados.get('local_valvula')
        )
        
        if resultado['sucesso']:
            return jsonify(resultado), 200
        else:
            status_code = 404 if 'não encontrada' in resultado['mensagem'] else 400
            return jsonify(resultado), status_code
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao atualizar válvula: {str(e)}'
        }), 500


@app.route('/api/valvulas/<int:id_valvula>', methods=['DELETE'])
@login_required
def deletar_valvula(id_valvula):
    """
    DELETE /api/valvulas/<id_valvula>
    
    Deleta uma válvula do sistema
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Query Parameters:
        forcar: true/false - Força deleção mesmo com registros (opcional)
    
    Returns:
        200: Válvula deletada
        400: Não pode deletar (tem registros)
        404: Válvula não encontrada
        401: Não autenticado
    """
    try:
        # Obtém parâmetro de query
        forcar = request.args.get('forcar', 'false').lower() == 'true'
        
        resultado = ValvulaService.deletar_valvula(
            id_valvula=id_valvula,
            forcar=forcar
        )
        
        if resultado['sucesso']:
            return jsonify(resultado), 200
        else:
            status_code = 404 if 'não encontrada' in resultado['mensagem'] else 400
            return jsonify(resultado), status_code
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao deletar válvula: {str(e)}'
        }), 500


# ============================================================
# ROTAS DE STATUS E CONTROLE
# ============================================================

@app.route('/api/valvulas/<int:id_valvula>/status', methods=['GET'])
@login_required
def obter_status(id_valvula):
    """
    GET /api/valvulas/<id_valvula>/status
    
    Obtém o status atual da válvula baseado no último registro
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Returns:
        200: Status da válvula
        404: Válvula não encontrada
        401: Não autenticado
    """
    try:
        resultado = ValvulaService.obter_status_atual(id_valvula)
        
        if resultado['sucesso'] or 'valvula_id' in resultado:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 404
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao obter status: {str(e)}'
        }), 500


@app.route('/api/valvulas/<int:id_valvula>/acionar', methods=['POST'])
@login_required
def acionar_valvula(id_valvula):

    """
    POST /api/valvulas/<id_valvula>/acionar
    
    Aciona a válvula (liga ou desliga) e cria registro automaticamente
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Body (JSON):
        {
            "ativar": true/false
        }
    
    Returns:
        200: Válvula acionada
        400: Requisição falha
    """
    
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nenhum dado fornecido'
            }), 400
        
        resultado = ValvulaService.acionar_valvula(
            id_valvula=id_valvula,
            ativar=dados.get('ativar'),
            id_usuario=current_user.id
        )
        
        if resultado['sucesso']:
            return jsonify(resultado), 200
        else:
            status_code = 404 if 'não encontrada' in resultado['mensagem'] else 400
            return jsonify(resultado), status_code
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao atualizar válvula: {str(e)}'
        }), 500