🏦 Banco Digital API

API REST de um sistema bancário desenvolvida em Python com FastAPI, com o objetivo de praticar o desenvolvimento back-end, a organização de aplicações e a implementação de operações bancárias.

O projeto permite gerenciar clientes e contas, realizar depósitos e transferências, consultar extratos e autenticar usuários. Também possui testes automatizados para verificar o comportamento das operações e a integridade dos saldos.

Status: concluído.

📌 Funcionalidades

- Cadastro de clientes: criação de clientes com validação de dados e verificação de CPF duplicado.

- Autenticação: login de clientes e geração de tokens JWT.

- Gerenciamento de contas: criação e consulta de contas bancárias.

- Depósitos: adição de valores ao saldo de uma conta.

- Transferências: movimentação de valores entre contas, com validações de saldo e titularidade.

- Consulta de extrato: listagem das transações relacionadas a uma conta.

- Validação de operações: tratamento de valores inválidos e de contas inexistentes ou bloqueadas.

- Testes automatizados: verificação de autenticação, permissões, movimentações financeiras e consistência dos saldos.

🛠️ Tecnologias utilizadas

- Python — linguagem de programação.

- FastAPI — criação dos endpoints da API REST.

- SQLAlchemy — interação com o banco de dados.

- SQLite — armazenamento dos dados durante o desenvolvimento.

- JWT — autenticação baseada em tokens.

- Pytest — execução dos testes automatizados.

- Uvicorn — servidor ASGI utilizado para executar a aplicação.

📂 Estrutura do projeto

banco-digital/
├── app/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_auth.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

Organização do código

- database: configuração da conexão com o banco de dados e gerenciamento das sessões.

- models: definição das entidades e tabelas do banco.

- routers: definição das rotas e dos endpoints da API.

- schemas: validação dos dados de entrada e definição dos formatos de resposta.

- services: implementação das regras de negócio.

- tests: testes automatizados para verificar o comportamento da aplicação.

- main.py: inicialização da aplicação FastAPI e registro dos routers.

⚙️ Como executar o projeto

1. Pré-requisitos

- Python instalado.

- Git instalado, caso deseje clonar o repositório.

2. Clonar o repositório

- git clone URL_DO_REPOSITORIO
- cd banco-digital

- Substitua URL_DO_REPOSITORIO pelo endereço do repositório no GitHub.

3. Criar o ambiente virtual

- python -m venv .venv

- No Windows, ative o ambiente virtual:

- .venv\Scripts\Activate.ps1

4. Instalar as dependências

- pip install -r requirements.txt

5. Configurar as variáveis de ambiente

- Se a aplicação utilizar variáveis de ambiente, crie um arquivo .env com base no .env.- example.

- Preencha os valores localmente e não publique chaves secretas ou credenciais reais.

6. Iniciar a aplicação

- Na raiz do projeto, execute:

- uvicorn app.main:app --reload

7. Acessar a documentação da API

- Com a aplicação em execução, acesse:

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

A documentação interativa permite consultar os endpoints e realizar requisições para testar a API.

🧪 Testes automatizados

Os testes são executados com Pytest e utilizam uma configuração de banco de dados isolada para evitar que os dados de teste alterem o banco local de desenvolvimento.

Para executar todos os testes:

python -m pytest -v

Os testes buscam verificar comportamentos como:

- Autenticação e acesso às rotas protegidas.

- Rejeição de credenciais inválidas.

- Validação de operações financeiras.

- Verificação de titularidade das contas.

- Atualização correta dos saldos após transferências.

- Comportamento do extrato quando não existem movimentações.

- Integridade dos saldos quando uma transferência falha.

🔐 Segurança e integridade

O projeto utiliza autenticação baseada em JWT e validações para restringir operações de acordo com o cliente autenticado.

As operações de transferência devem garantir que a movimentação seja realizada de forma consistente, evitando que uma falha deixe os saldos das contas parcialmente atualizados.

As funcionalidades e os mecanismos de segurança descritos devem ser considerados conforme sua implementação e seus testes atuais.

⚠️ Limitações

Este é um projeto educacional, desenvolvido para fins de estudo e portfólio. Não deve ser utilizado para movimentações financeiras reais nem considerado um sistema bancário pronto para produção.

👨‍💻 Autor

Desenvolvido por Luiz Felipe Silva.