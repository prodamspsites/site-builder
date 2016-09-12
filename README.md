# Site Builder

Construtor padrão de sites usado para criação de sites e hotsites.

## Ferramentas Usadas

- Python 3.5.2
- Flask
- PostgreSQL
- Docker
- Make

## Instalação

Para instalar, sugiro antes que avalie o uso da ferramenta [Pyenv][0] e 
o plugin [Virtualenv][1]. 

- Crie um ambiente com Python 3.5.2
- Copie o arquivo de configuração: 
`cp builder/config/local.py.example builder/config/local.py`
- Se for usar o Docker, ative com `docker-compose up -d`
- Rode as migrações com: `python manage.py db upgrade`
- Inicie o servidor com: `python manage.py runserver`


## Migração

Para criar uma migração deve seguir os seguintes passos:

- Rode um comando de upgrade: `python manage.py db upgrade`
- Crie a migração usando: `python manage.py db migrate`
- Será gerado o arquivo na pasta `migrations/versions`
- Renomeie o arquivo colocando um titulo após o under (`_`)
- Revise o arquivo para vericar inconsistências

**Observação:** Nas migrações, são importante tanto os comandos de 
upgrade quanto downgrade, então é relevante que o script seja criado 
para ambos os lados e serem testados antes de ser enviado para o 
repositório.

## Testes Unitários

A ferramenta de teste utilizada aqui é o **Pytest** com as seguintes 
definições:

- Todos os testes ficam na pasta `tests/*`
- Os fixtures são inseridos no arquivo `tests/conftest.py`
- Os fixtures não globais pode ser inseridos direto no arquivo de testes
- Todos arquivos de testes começam com o nome test: `test_*.py`
- As funções também deve seguir o padrão: `def test_*(**kwargs):`

### Rodando os testes

- Use o comando `PYTHONPATH=. py.test tests`

### Coverage

- Use o comando 
`PYTHONPATH=. py.test tests --cov-report=html --cov=builder`
- O coverage poderá ser visto no caminho `htmlconv/index.html`

## Make shortcuts

Adicionalmente há um Makefile com alguns atalhos:

- `clean`: Exclui temporários do Python (`*.pyc`)
- `coverage`: Roda o comando para gerar o coverage report
- `unit`: Roda todos os testes unitários
- `local_config`: Copia o exemplo de configuração local
- `upgrade_db`: Roda as migrações no banco
- `migrate_db`: Cria uma nova migração
- `runserver`: Inicializa o servidor local

[0]:https://github.com/yyuu/pyenv
[1]:https://github.com/yyuu/pyenv-virtualenv