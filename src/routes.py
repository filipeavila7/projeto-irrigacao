from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from src.services.registro_service import RegistroService
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.valvula_service import ValvulaService
from src import app

'''
# Cria o Blueprint para as rotas de registros
registro_bp = Blueprint('registro', __name__, url_prefix='/api/registros')
'''


# ============================================================
# ROTAS REGISTROS (CRUD)
# ============================================================

@app.route('/api/registros/', methods=['POST'])
@jwt_required()
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
        usuario_id = get_jwt_identity()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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


@app.route('/api/registros/usuario/<int:id_usuario>', methods=['GET'])
@jwt_required()
def listar_por_usuario(id_usuario):
    """
    GET /api/registros/usuario/<id_usuario>
    
    Lista registros de um usuário específico
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_usuario: ID do usuário
    
    Returns:
        200: Lista de registros
        401: Não autenticado
        500: Erro interno
    """
    try:
        
        registros = RegistroService.buscar_por_usuario(id_usuario)
        
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
            'usuario_id': id_usuario,
            'total': len(registros_lista),
            'registros': registros_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao listar registros do usuário: {str(e)}'
        }), 500


@app.route('/api/registros/meus', methods=['GET'])
@jwt_required()
def listar_meus_registros():
    """
    GET /api/registros/meus
    
    Lista registros do usuário autenticado
    
    Headers:
        Authorization: Bearer <access_token>
    
    Returns:
        200: Lista de registros do usuário
        401: Não autenticado
        500: Erro interno
    """
    try:
        usuario_id = get_jwt_identity()
        
        registros = RegistroService.buscar_por_usuario(usuario_id)
        
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
            'total': len(registros_lista),
            'registros': registros_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao listar seus registros: {str(e)}'
        }), 500


@app.route('/api/registros/periodo', methods=['GET'])
@jwt_required()
def listar_por_periodo():
    """
    GET /api/registros/periodo
    
    Lista registros em um período específico
    
    Headers:
        Authorization: Bearer <access_token>
    
    Query Parameters:
        data_inicio: Data inicial (formato: YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)
        data_fim: Data final (formato: YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS)
    
    Returns:
        200: Lista de registros no período
        400: Parâmetros inválidos
        401: Não autenticado
        500: Erro interno
    """
    try:
        data_inicio_str = request.args.get('data_inicio')
        data_fim_str = request.args.get('data_fim')
        
        if not data_inicio_str or not data_fim_str:
            return jsonify({
                'sucesso': False,
                'mensagem': 'data_inicio e data_fim são obrigatórios'
            }), 400
        
        # Converte strings para datetime
        try:
            data_inicio = datetime.fromisoformat(data_inicio_str)
            data_fim = datetime.fromisoformat(data_fim_str)
        except ValueError:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Formato de data inválido. Use: YYYY-MM-DD ou YYYY-MM-DD HH:MM:SS'
            }), 400
        
        if data_inicio > data_fim:
            return jsonify({
                'sucesso': False,
                'mensagem': 'data_inicio não pode ser posterior a data_fim'
            }), 400
        
        registros = RegistroService.buscar_por_periodo(data_inicio, data_fim)
        
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
            'periodo': {
                'data_inicio': data_inicio.isoformat(),
                'data_fim': data_fim.isoformat()
            },
            'total': len(registros_lista),
            'registros': registros_lista
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao buscar registros por período: {str(e)}'
        }), 500


# ============================================================
# ROTAS DE ESTATÍSTICAS E RELATÓRIOS
# ============================================================

@app.route('/api/registros/contar/<int:id_valvula>', methods=['GET'])
@jwt_required()
def contar_acionamentos(id_valvula):
    """
    GET /api/registros/contar/<id_valvula>
    
    Conta acionamentos de uma válvula
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Query Parameters:
        data_inicio: Data inicial para contagem (opcional, formato: YYYY-MM-DD)
    
    Returns:
        200: Contagem de acionamentos
        401: Não autenticado
        500: Erro interno
    """
    try:
        data_inicio_str = request.args.get('data_inicio')
        data_inicio = None
        
        if data_inicio_str:
            try:
                data_inicio = datetime.fromisoformat(data_inicio_str)
            except ValueError:
                return jsonify({
                    'sucesso': False,
                    'mensagem': 'Formato de data inválido. Use: YYYY-MM-DD'
                }), 400
        
        resultado = RegistroService.contar_acionamentos_valvula(id_valvula, data_inicio)
        
        return jsonify({
            'sucesso': True,
            'valvula_id': id_valvula,
            'data_inicio': data_inicio.isoformat() if data_inicio else None,
            **resultado
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao contar acionamentos: {str(e)}'
        }), 500


@app.route('/api/registros/relatorio/<int:id_valvula>', methods=['GET'])
@jwt_required()
def gerar_relatorio(id_valvula):
    """
    GET /api/registros/relatorio/<id_valvula>
    
    Gera relatório de uso de uma válvula
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        id_valvula: ID da válvula
    
    Query Parameters:
        periodo_dias: Período em dias para análise (padrão: 7)
    
    Returns:
        200: Relatório de uso
        400: Parâmetros inválidos
        401: Não autenticado
        500: Erro interno
    """
    try:
        periodo_dias = request.args.get('periodo_dias', 7, type=int)
        
        if periodo_dias < 1:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Período deve ser maior que 0'
            }), 400
        
        relatorio = RegistroService.gerar_relatorio_valvula(id_valvula, periodo_dias)
        
        if 'erro' in relatorio:
            return jsonify({
                'sucesso': False,
                'mensagem': relatorio['erro']
            }), 500
        
        return jsonify({
            'sucesso': True,
            **relatorio
        }), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao gerar relatório: {str(e)}'
        }), 500


# ============================================================
# ROTAS DE MANUTENÇÃO
# ============================================================

@app.route('/api/registros/limpar-antigos', methods=['DELETE'])
@jwt_required()
def deletar_registros_antigos():
    """
    DELETE /api/registros/limpar-antigos
    
    Remove registros mais antigos que X dias
    ATENÇÃO: Esta operação não pode ser desfeita!
    
    Headers:
        Authorization: Bearer <access_token>
    
    Query Parameters:
        dias: Número de dias para manter os registros (padrão: 90)
    
    Returns:
        200: Registros deletados com sucesso
        400: Parâmetros inválidos
        401: Não autenticado
        500: Erro interno
    """
    try:
        dias = request.args.get('dias', 90, type=int)
        
        if dias < 1:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Período deve ser maior que 0'
            }), 400
        
        # Confirmação de segurança
        confirmacao = request.args.get('confirmar', 'false').lower()
        if confirmacao != 'true':
            return jsonify({
                'sucesso': False,
                'mensagem': 'Esta operação requer confirmação. Adicione ?confirmar=true'
            }), 400
        
        resultado = RegistroService.deletar_registros_antigos(dias)
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao deletar registros antigos: {str(e)}'
        }), 500


# ============================================================
# ROTAS VALVULAS (CRUD)
# ============================================================

@app.route('/api/valvulas/', methods=['POST'])
@jwt_required()
def criar_valvula():
    """
    POST /api/valvulas/
    
    Cria uma nova válvula no sistema
    
    Headers:
        Authorization: Bearer <access_token>
    
    Body (JSON):
        {
            "nome_valvula": "string",
            "local_valvula": "string" (opcional)
        }
    
    Returns:
        201: Válvula criada com sucesso
        400: Dados inválidos ou válvula já existe
        401: Não autenticado
        500: Erro interno
    """
    try:
        dados = request.get_json()
        
        if not dados:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Dados não fornecidos'
            }), 400
        
        nome_valvula = dados.get('nome_valvula')
        local_valvula = dados.get('local_valvula')
        
        if not nome_valvula:
            return jsonify({
                'sucesso': False,
                'mensagem': 'Nome da válvula é obrigatório'
            }), 400
        
        resultado = ValvulaService.criar_valvula(
            nome_valvula=nome_valvula,
            local_valvula=local_valvula
        )
        
        if resultado['sucesso']:
            return jsonify(resultado), 201
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao criar válvula: {str(e)}'
        }), 500


@app.route('/api/valvulas/', methods=['GET'])
@jwt_required()
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
@jwt_required()
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


@app.route('/api/valvulas/buscar/<nome_valvula>', methods=['GET'])
@jwt_required()
def buscar_por_nome(nome_valvula):
    """
    GET /api/valvulas/buscar/<nome_valvula>
    
    Busca uma válvula pelo nome
    
    Headers:
        Authorization: Bearer <access_token>
    
    Path Parameters:
        nome_valvula: Nome da válvula
    
    Returns:
        200: Dados da válvula
        404: Válvula não encontrada
        401: Não autenticado
    """
    try:
        valvula = ValvulaService.buscar_por_nome(nome_valvula)
        
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
            'mensagem': f'Erro ao buscar válvula: {str(e)}'
        }), 500


@app.route('/api/valvulas/<int:id_valvula>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
            id_usuario=get_jwt_identity()
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