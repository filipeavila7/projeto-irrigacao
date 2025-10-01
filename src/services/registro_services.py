from datetime import datetime
from typing import List, Optional, Dict
from sqlalchemy.exc import SQLAlchemyError
from src import db
from src.models.registro_models import Registro
from datetime import timedelta


class RegistroService:
    """
    Service para gerenciar operações relacionadas aos registros de acionamento de válvulas
    """
    
    @staticmethod
    def criar_registro(status: bool, id_usuario: int, id_valvula: int) -> Dict:
        """
        Cria um novo registro de acionamento de válvula
        
        Args:
            status: True para ativada, False para desativada
            id_usuario: ID do usuário que acionou
            id_valvula: ID da válvula acionada
            
        Returns:
            Dict com sucesso e dados do registro ou mensagem de erro
        """
        try:
            novo_registro = Registro(
                status=status,
                data_acionamento=datetime.now(),
                id_usuario=id_usuario,
                id_valvula=id_valvula
            )
            
            db.session.add(novo_registro)
            db.session.commit()
            
            return {
                'sucesso': True,
                'mensagem': 'Registro criado com sucesso',
                'dados': {
                    'id': novo_registro.id,
                    'status': novo_registro.status,
                    'data_acionamento': novo_registro.data_acionamento.isoformat(),
                    'id_usuario': novo_registro.id_usuario,
                    'id_valvula': novo_registro.id_valvula
                }
            }
            
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao criar registro: {str(e)}'
            }
    
    @staticmethod
    def buscar_por_id(id_registro: int) -> Optional[Registro]:
        """
        Busca um registro pelo ID
        
        Args:
            id_registro: ID do registro
            
        Returns:
            Objeto Registro ou None se não encontrado
        """
        try:
            return Registro.query.get(id_registro)
        except SQLAlchemyError:
            return None
    
    @staticmethod
    def listar_todos() -> List[Registro]:
        """
        Lista todos os registros com paginação
            
        Returns:
            Lista de registros
        """
        try:
            return Registro.query.order_by(
                Registro.data_acionamento.desc()
            ).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def buscar_por_valvula(id_valvula: int) -> List[Registro]:
        """
        Busca registros de uma válvula específica
        
        Args:
            id_valvula: ID da válvula
            
        Returns:
            Lista de registros da válvula
        """
        try:
            return Registro.query.filter_by(
                id_valvula=id_valvula
            ).order_by(
                Registro.data_acionamento.desc()
            ).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def buscar_por_usuario(id_usuario: int) -> List[Registro]:
        """
        Busca registros de um usuário específico
        
        Args:
            id_usuario: ID do usuário
            
        Returns:
            Lista de registros do usuário
        """
        try:
            return Registro.query.filter_by(
                id_usuario=id_usuario
            ).order_by(
                Registro.data_acionamento.desc()
            ).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def buscar_por_periodo(data_inicio: datetime, data_fim: datetime) -> List[Registro]:
        """
        Busca registros em um período específico
        
        Args:
            data_inicio: Data inicial do período
            data_fim: Data final do período
            
        Returns:
            Lista de registros no período
        """
        try:
            return Registro.query.filter(
                Registro.data_acionamento.between(data_inicio, data_fim)
            ).order_by(
                Registro.data_acionamento.desc()
            ).all()
        except SQLAlchemyError:
            return []
    
    @staticmethod
    def contar_acionamentos_valvula(id_valvula: int, data_inicio: Optional[datetime] = None) -> Dict:
        """
        Conta quantas vezes uma válvula foi acionada (ativada/desativada)
        
        Args:
            id_valvula: ID da válvula
            data_inicio: Data inicial para contagem (opcional)
            
        Returns:
            Dict com contagem de ativações e desativações
        """
        try:
            query = Registro.query.filter_by(id_valvula=id_valvula)
            
            if data_inicio:
                query = query.filter(Registro.data_acionamento >= data_inicio)
            
            ativacoes = query.filter_by(status=True).count()
            desativacoes = query.filter_by(status=False).count()
            
            return {
                'ativacoes': ativacoes,
                'desativacoes': desativacoes,
                'total': ativacoes + desativacoes
            }
        except SQLAlchemyError:
            return {'ativacoes': 0, 'desativacoes': 0, 'total': 0}
    
    @staticmethod
    def deletar_registros_antigos(dias: int = 90) -> Dict:
        """
        Remove registros mais antigos que X dias
        
        Args:
            dias: Número de dias para manter os registros
            
        Returns:
            Dict com resultado da operação
        """
        try:
            data_limite = datetime.now() - timedelta(days=dias)
            
            registros_deletados = Registro.query.filter(
                Registro.data_acionamento < data_limite
            ).delete()
            
            db.session.commit()
            
            return {
                'sucesso': True,
                'mensagem': f'{registros_deletados} registros deletados',
                'quantidade': registros_deletados
            }
        except SQLAlchemyError as e:
            db.session.rollback()
            return {
                'sucesso': False,
                'mensagem': f'Erro ao deletar registros: {str(e)}'
            }
    
    @staticmethod
    def gerar_relatorio_valvula(id_valvula: int, periodo_dias: int = 7) -> Dict:
        """
        Gera relatório de uso de uma válvula
        
        Args:
            id_valvula: ID da válvula
            periodo_dias: Período em dias para análise
            
        Returns:
            Dict com estatísticas da válvula
        """
        try:
            data_inicio = datetime.now() - timedelta(days=periodo_dias)
            
            registros = Registro.query.filter(
                Registro.id_valvula == id_valvula,
                Registro.data_acionamento >= data_inicio
            ).order_by(Registro.data_acionamento).all()
            
            if not registros:
                return {
                    'valvula_id': id_valvula,
                    'periodo_dias': periodo_dias,
                    'total_acionamentos': 0,
                    'ativacoes': 0,
                    'desativacoes': 0,
                    'tempo_ativa_minutos': 0
                }
            
            ativacoes = sum(1 for r in registros if r.status)
            desativacoes = sum(1 for r in registros if not r.status)
            
            # Calcula tempo total ativa (aproximado)
            tempo_ativa = 0
            ultima_ativacao = None
            
            for registro in registros:
                if registro.status:
                    ultima_ativacao = registro.data_acionamento
                elif ultima_ativacao:
                    tempo_ativa += (registro.data_acionamento - ultima_ativacao).total_seconds() / 60
                    ultima_ativacao = None
            
            return {
                'valvula_id': id_valvula,
                'periodo_dias': periodo_dias,
                'total_acionamentos': len(registros),
                'ativacoes': ativacoes,
                'desativacoes': desativacoes,
                'tempo_ativa_minutos': round(tempo_ativa, 2),
                'primeiro_registro': registros[0].data_acionamento.isoformat(),
                'ultimo_registro': registros[-1].data_acionamento.isoformat()
            }
            
        except SQLAlchemyError:
            return {
                'valvula_id': id_valvula,
                'erro': 'Erro ao gerar relatório'
            }