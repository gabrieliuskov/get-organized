# Get Organized - Web App para Gestão Financeira

O Get Organized é um Web App intuitivo e prático para ajudar você a manter suas finanças sob controle. Desenvolvido totalmente em Python, ele utiliza o framework Flask para criar uma aplicação web poderosa e fácil de usar. 

## Pré-requisitos

Antes de executar o Get Organized, certifique-se de ter as seguintes dependências instaladas:

- Python 3.x (https://www.python.org/)
- PostgreSQL (https://www.postgresql.org/)

## Configuração do Banco de Dados

Para que o aplicativo funcione corretamente, você precisará configurar as credenciais do banco de dados no código. Altere os trechos de código que se conecta ao banco de dados seguindo o modelo abaixo:
Substitua `<seu_usuario>` pelo nome de usuário do PostgreSQL e `<sua_senha>` pela senha do banco de dados:

```python
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="financas",
    user="<seu_usuario>",
    password="<sua_senha>"
)
```
Certifique-se de ter criado um banco de dados chamado "financas" no PostgreSQL antes de executar o aplicativo.

## Funcionalidades Principais

- Adicionar e categorizar receitas e despesas.
- Acompanhar o saldo e as movimentações financeiras.
- Visualizar gráficos para análise financeira.

## Como Utilizar

Execute o aplicativo:

```python
python index.py
```

Abra seu navegador e acesse http://127.0.0.1:8050/ para começar a usar o Get Organized.

Para mais informações sobre mim e meus projetos, visite meu perfil no LinkedIn:
[Gabriel Iuskov](https://www.linkedin.com/in/gabriel-gustavo-iuskov-rosario-1689841b3/)
