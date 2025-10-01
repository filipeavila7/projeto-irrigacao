from datetime import datetime, timedelta
from typing import List, Optional, Dict
from sqlalchemy.exc import SQLAlchemyError
from src import db
from src.models.valvula_models import Valvulas
from src.models.registro_models import Registro
from src.services.registro_services import RegistroService


class ValvulaService:
    """
    Service para gerenciar operações relacionadas às válvulas do sistema de irrigação
    """
    
    # ============================================================
    # OPERAÇÕES BÁSICAS (CRUD)
    # ============================================================
    
    @staticmethod
    def criar_valvula(nome_valvula: str, local_valvula: str = None) -> Dict:
        """
        Cria uma nova válvula
        
        Args:
            nome_valvula: Nome identificador da válvula
            local_valvula: Localização física da válvula (opcional)
            
        Returns:
            Dict com sucesso e dados da válvula ou mensagem de erro
        """
        try:
            # Validação básica
            if not nome_valvula or nome_valvula.strip() == "":
                return {
                    'sucesso': False,
                    'mensagem': 'Nome da válvula não pode ser vazio'
                }
            
            # Verifica se já existe válvula com mesmo nome
            valvula_existente = Valvulas.query.filter_by(
                nome_valvula=nome_valvula.strip()
            ).first()
            
            if valvula_existente:
                return {
                    'sucesso': False,
                    'mensagem': 'Já existe uma válvula com este nome'
                }
            
            nova_valvula = Valvulas(
                nome_valvula=nome_valvula.strip(),
                local_valvula=local_valvula.strip() if local_valvula else None
            )
            
            db.session.add(nova_valvula)
            db.session.commit()
            
            return {
                'sucesso': True,
                'mensagem': 'Válvula criada com sucesso',
                'dados': {
                    'id': nova_valvula.id,
                    'nome_valvula': nova_valvula.nome_valvula,
                    'local_valvula': nova_valvula.local_valvula
                }
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao criar válvula: {str(e)}'
            }
    
    @staticmethod
    def buscar_por_id(id_valvula: int) -> Optional[Valvulas]:
        """
        Busca uma válvula pelo ID
        
        Args:
            id_valvula: ID da válvula
            
        Returns:
            Objeto Valvulas ou None se não encontrada
        """
        try:
            return Valvulas.query.get(id_valvula)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def buscar_por_nome(nome_valvula: str) -> Optional[Valvulas]:
        """
        Busca uma válvula pelo nome
        
        Args:
            nome_valvula: Nome da válvula
            
        Returns:
            Objeto Valvulas ou None se não encontrada
        """
        try:
            return Valvulas.query.filter_by(
                nome_valvula=nome_valvula
            ).first()
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def listar_todas() -> List[Valvulas]:
        """
        Lista todas as válvulas cadastradas
        
        Returns:
            Lista de objetos Valvulas
        """
        try:
            return Valvulas.query.order_by(Valvulas.nome_valvula).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def atualizar_valvula(id_valvula: int, nome_valvula: str = None, 
                         local_valvula: str = None) -> Dict:
        """
        Atualiza informações de uma válvula
        
        Args:
            id_valvula: ID da válvula
            nome_valvula: Novo nome (opcional)
            local_valvula: Nova localização (opcional)
            
        Returns:
            Dict com resultado da operação
        """
        try:
            valvula = ValvulaService.buscar_por_id(id_valvula)
            
            if not valvula:
                return {
                    'sucesso': False,
                    'mensagem': 'Válvula não encontrada'
                }
            
            # Atualiza apenas os campos fornecidos
            if nome_valvula is not None:
                if nome_valvula.strip() == "":
                    return {
                        'sucesso': False,
                        'mensagem': 'Nome não pode ser vazio'
                    }
                valvula.nome_valvula = nome_valvula.strip()
            
            if local_valvula is not None:
                valvula.local_valvula = local_valvula.strip() if local_valvula else None
            
            db.session.commit()
            
            return {
                'sucesso': True,
                'mensagem': 'Válvula atualizada com sucesso',
                'dados': {
                    'id': valvula.id,
                    'nome_valvula': valvula.nome_valvula,
                    'local_valvula': valvula.local_valvula
                }
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao atualizar válvula: {str(e)}'
            }
    
    @staticmethod
    def deletar_valvula(id_valvula: int, forcar: bool = False) -> Dict:
        """
        Deleta uma válvula
        
        Args:
            id_valvula: ID da válvula
            forcar: Se True, deleta mesmo com registros associados
            
        Returns:
            Dict com resultado da operação
        """
        try:
            valvula = ValvulaService.buscar_por_id(id_valvula)
            
            if not valvula:
                return {
                    'sucesso': False,
                    'mensagem': 'Válvula não encontrada'
                }
            
            # Verifica se há registros associados
            total_registros = Registro.query.filter_by(
                id_valvula=id_valvula
            ).count()
            
            if total_registros > 0 and not forcar:
                return {
                    'sucesso': False,
                    'mensagem': f'Válvula possui {total_registros} registros associados. '
                                f'Use forcar=True para deletar mesmo assim.',
                    'total_registros': total_registros
                }
            
            # Se forçar, deleta os registros primeiro
            if forcar and total_registros > 0:
                Registro.query.filter_by(id_valvula=id_valvula).delete()
            
            db.session.delete(valvula)
            db.session.commit()
            
            return {
                'sucesso': True,
                'mensagem': 'Válvula deletada com sucesso',
                'registros_deletados': total_registros if forcar else 0
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao deletar válvula: {str(e)}'
            }
    
    # ============================================================
    # OPERAÇÕES DE STATUS E CONTROLE
    # ============================================================
    
    @staticmethod
    def obter_status_atual(id_valvula: int) -> Dict:
        """
        Obtém o status atual da válvula baseado no último registro
        
        Args:
            id_valvula: ID da válvula
            
        Returns:
            Dict com status atual e informações
        """
        try:
            valvula = ValvulaService.buscar_por_id(id_valvula)
            
            if not valvula:
                return {
                    'sucesso': False,
                    'mensagem': 'Válvula não encontrada'
                }
            
            # Busca último registro
            ultimo_registro = Registro.query.filter_by(
                id_valvula=id_valvula
            ).order_by(Registro.data_acionamento.desc()).first()
            
            if not ultimo_registro:
                return {
                    'sucesso': True,
                    'valvula_id': id_valvula,
                    'nome': valvula.nome_valvula,
                    'status': False,  # Assume desligada se nunca foi acionada
                    'mensagem': 'Válvula nunca foi acionada',
                    'ultimo_acionamento': None
                }
            
            return {
                'sucesso': True,
                'valvula_id': id_valvula,
                'nome': valvula.nome_valvula,
                'status': ultimo_registro.status,
                'status_texto': 'ATIVADA' if ultimo_registro.status else 'DESATIVADA',
                'ultimo_acionamento': ultimo_registro.data_acionamento.isoformat(),
                'id_usuario': ultimo_registro.id_usuario
            }
            
        except SQLAlchemyError:
            return {
                'sucesso': False,
                'mensagem': 'Erro ao obter status da válvula'
            }
    
    @staticmethod
    def acionar_valvula(id_valvula: int, ativar: bool, id_usuario: int) -> Dict:
        """
        Aciona a válvula (liga ou desliga) e cria registro
        
        Args:
            id_valvula: ID da válvula
            ativar: True para ligar, False para desligar
            id_usuario: ID do usuário que está acionando
            
        Returns:
            Dict com resultado da operação
        """
        try:
            valvula = ValvulaService.buscar_por_id(id_valvula)
            
            if not valvula:
                return {
                    'sucesso': False,
                    'mensagem': 'Válvula não encontrada'
                }
            
            # Verifica status atual
            status_atual = ValvulaService.obter_status_atual(id_valvula)
            
            if status_atual['sucesso'] and status_atual.get('status') == ativar:
                acao = 'ativada' if ativar else 'desativada'
                return {
                    'sucesso': False,
                    'mensagem': f'Válvula já está {acao}',
                    'status_atual': ativar
                }
            
            # Cria registro do acionamento

            novo_registro = RegistroService.criar_registro(status=ativar, id_usuario=id_usuario, id_valvula=id_valvula)
            
            acao = 'ativada' if ativar else 'desativada'
            
            return {
                'sucesso': True,
                'mensagem': f'Válvula {acao} com sucesso',
                'dados': {
                    'valvula_id': id_valvula,
                    'nome': valvula.nome_valvula,
                    'status': ativar,
                    'status_texto': 'ATIVADA' if ativar else 'DESATIVADA',
                    'data_acionamento': novo_registro.data_acionamento.isoformat(),
                    'registro_id': novo_registro.id
                }
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao acionar válvula: {str(e)}'
            }
    
    @staticmethod
    def ligar_valvula(id_valvula: int, id_usuario: int) -> Dict:
        """
        Atalho para ligar a válvula
        """
        return ValvulaService.acionar_valvula(id_valvula, True, id_usuario)
    
    @staticmethod
    def desligar_valvula(id_valvula: int, id_usuario: int) -> Dict:
        """
        Atalho para desligar a válvula
        """
        return ValvulaService.acionar_valvula(id_valvula, False, id_usuario)