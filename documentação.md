# 🌱 Projeto de Irrigação Automática - Backend

## 🎯 Objetivos

- Automatizar o processo de irrigação.
- Monitorar em tempo real os níveis de umidade do solo.
- Controlar a irrigação com base nos dados recebidos dos sensores.
- Fornecer uma interface de comunicação via API RESTful.

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Flask** (Framework Web para API RESTful)
- **SQLAlchemy** (ORM para banco de dados)
- **Banco de dados relacional** (SQLite, PostgreSQL, MySQL, etc.) utilizado para testes
- **Sensor de Umidade** (Hardware)
- **Microcontrolador (Arduino/ESP32)** (para coleta de dados e controle)

## 📁 Estrutura de Pastas
PROJETO_IRRIGACAO/
├── .venv/ # Ambiente virtual Python
├── migrations/ # Arquivos de migração do banco de dados
├── src/
│ ├── entities/ # Definição das entidades do banco (models)
│ │ ├── registro_entities.py
│ │ ├── usuario_entities.py
│ │ └── valvula_entities.py
│ ├── models/ # Modelos para manipulação de dados
│ │ ├── registro_models.py
│ │ ├── usuario_models.py
│ │ └── valvula_models.py
│ ├── services/ # Lógica de negócio e regras do sistema
│ │ ├── registro_services.py
│ │ ├── tempo_services.py
│ │ ├── usuario_services.py
│ │ └── valvula_services.py
│ ├── templates/ # Arquivos HTML para a interface (frontend simples)
│ │ ├── cadastro_usuario.html
│ │ ├── cadastro_valvula.html
│ │ ├── esqueci_a_senha.html
│ │ ├── index.html
│ │ ├── login.html
│ │ └── resetar_senha.html
│ └── routes.py # Definição das rotas da API e páginas
├── .env # Variáveis de ambiente
├── app.py # Arquivo principal para iniciar a aplicação Flask
├── connection.py # Configuração da conexão com banco de dados
├── documentação.md # Documentação do projeto
└── requirements.txt # Dependências do projeto

## 🔌 Funcionalidades da API

| Método | Descrição |
|--------|-----------|
| GET | Retorna o último valor de umidade |
| POST | Recebe um novo valor de umidade enviado pelo microcontrolador |
| POST | Aciona manualmente a irrigação |
| GET | Retorna o status atual da irrigação |

## 🔄 Fluxo de Funcionamento

1. O microcontrolador coleta dados do sensor de umidade.
2. Os dados são enviados para a API via requisição HTTP ou MQTT.
3. O backend analisa os dados e decide se deve ativar a irrigação.
4. Caso necessário, um comando é enviado ao microcontrolador para acionar a bomba d’água.
5. O sistema registra as ações no banco de dados.

## 🚀 Como Executar o Projeto

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/projeto-irrigacao.git

# Entrar na pasta
cd projeto-irrigacao

# Criar e ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Definir variáveis de ambiente no arquivo .env (exemplo abaixo)

# Executar a aplicação
python app.py
```

## 👨‍🏫 Conclusão

Este projeto demonstrou como a integração entre software e hardware pode ser aplicada para resolver problemas reais, como o uso eficiente da água na agricultura. O back-end fornece uma base sólida para controle e monitoramento remoto, podendo ser expandido com funcionalidades como notificações, dashboards e inteligência artificial.

👥 Integrantes do Projeto

- João Pedro Q
- Juan Costa 
- Filipe Avila
- William Banks
- Natan H Penaz
- Kauan vinicius
- Kawe Henrique