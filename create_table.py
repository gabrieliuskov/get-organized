import psycopg2


conn = psycopg2.connect(
    host="localhost",
    database="financas",
    user="postgres",
    password="admin"
)

# def criar_tabela_usuario(table):

#     cursor = conn.cursor()

#     comando = f"""
#     CREATE TABLE {table} (
#         id SERIAL PRIMARY KEY,
#         usuario VARCHAR(50),
#         password VARCHAR(150),
#         email VARCHAR(50) UNIQUE
#     )"""

#     cursor.execute(comando)
#     conn.commit()

#     cursor.close()
#     conn.close()

# criar_tabela_usuario("usuarios")


# def criar_tabela_lancamento(table):

#     cursor = conn.cursor()

#     comando = f"""
#     CREATE TABLE {table} (
#         id SERIAL PRIMARY KEY,
#         tipo VARCHAR(30),
#         valor NUMERIC(10,2),
#         descricao VARCHAR(50),
#         data DATE,
#         id_usuario INTEGER 
#     )"""

#     cursor.execute(comando)
#     conn.commit()

#     cursor.close()
#     conn.close()

# criar_tabela_lancamento("receitas")

# def criar_tabela_lancamento(table):

#     cursor = conn.cursor()

#     comando = f"""
#     CREATE TABLE {table} (
#         id SERIAL PRIMARY KEY,
#         tipo VARCHAR(30),
#         valor NUMERIC(10,2),
#         descricao VARCHAR(50),
#         data DATE,
#         id_usuario INTEGER,
#         id_pagamento INTEGER,
#         id_responsavel INTEGER
#     )"""

#     cursor.execute(comando)
#     conn.commit()

#     cursor.close()
#     conn.close()

# criar_tabela_lancamento("despesas")



# def criar_tabela_lancamento(table):

#     cursor = conn.cursor()

#     comando = f"""
#     CREATE TABLE {table} (
#         id SERIAL PRIMARY KEY,
#         nome VARCHAR(20) UNIQUE
#     )"""

#     cursor.execute(comando)
#     conn.commit()

#     comando = f"""
#     INSERT INTO {table} (nome) VALUES ('Dinheiro')
#     """
#     cursor.execute(comando)
#     conn.commit()

#     cursor.close()
#     conn.close()

# criar_tabela_lancamento("banco")