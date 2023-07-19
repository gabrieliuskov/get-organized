from app import *


def get_user_receitas(user_id):
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()

    query = f"SELECT * FROM receitas WHERE id_usuario = %s"

    cursor.execute(query, (user_id, ))

    results = cursor.fetchall()

    colunas = [i[0] for i in cursor.description]

    df_dict_receitas = pd.DataFrame(results, columns=colunas).to_dict()

    


    query2 = f"SELECT * FROM despesas WHERE id_usuario = %s"

    cursor.execute(query2, (user_id, ))

    results = cursor.fetchall()

    colunas = [i[0] for i in cursor.description]

    df_dict_despesas = pd.DataFrame(results, columns=colunas).to_dict()

    query3 = f"SELECT * FROM banco"

    cursor.execute(query3)

    results = cursor.fetchall()

    colunas = [i[0] for i in cursor.description]

    df_dict_banco = pd.DataFrame(results, columns=colunas).to_dict()


    cursor.close()
    conn.close()

    return df_dict_receitas, df_dict_despesas, df_dict_banco


def add_receitas(descricao, data, valor, tipo):

    lista = data.split("-")

    data = date(int(lista[0]), int(lista[1]), int(lista[2]))
    valor = round(float(valor),2)
    
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()
   
    query = f"INSERT INTO receitas (tipo, valor, descricao, data, id_usuario) VALUES (%s, %s, %s, %s, %s)"

    cursor.execute(query, (tipo, valor, descricao, data, current_user.id, ))
    conn.commit()

    cursor.close()
    conn.close()


def add_despesas(descricao, data, tipo, forma_pagamento,resp, valor):
    lista = data.split("-")

    data = date(int(lista[0]), int(lista[1]), int(lista[2]))
    valor = round(float(valor),2)

    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()
   
    query = f"INSERT INTO despesas (tipo, valor, descricao, data, id_usuario, id_pagamento, id_responsavel) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    cursor.execute(query, (tipo, valor, descricao, data, current_user.id, forma_pagamento, resp, ))
    conn.commit()

    cursor.close()
    conn.close()


def add_banco(banco):
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()

    query = f"INSERT INTO banco (nome) VALUES (%s)"

    cursor.execute(query, (banco, ))
    conn.commit()

    cursor.close()
    conn.close()


def del_banco(banco):

    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )
    cursor = conn.cursor()

    query = f"DELETE FROM banco WHERE id = %s"

    cursor.execute(query, (banco,))
    conn.commit()

    cursor.close()
    conn.close()

def del_registro(data, base, id_user, banco):

    try:
        if base == 1:

            conn = psycopg2.connect(
                host="localhost",
                database="financas",
                user="postgres",
                password="admin"
            )

            cursor = conn.cursor()

            query = f"DELETE FROM receitas WHERE tipo = %s AND valor = %s AND descricao = %s AND data = %s AND id_usuario = %s"

            cursor.execute(query, (data["tipo"], data["valor"], data["descricao"], data["data"], id_user,))
            conn.commit()

            cursor.close()
            conn.close()

        else:

            df_bancos = pd.DataFrame(banco)

            for index, row in df_bancos.iterrows():
                if row["nome"] == data["Pagamento"]:
                    bank = row["id"]
                    break

            resp = 1 if data["Responsavel"] == "Eu" else 2

            conn = psycopg2.connect(
                host="localhost",
                database="financas",
                user="postgres",
                password="admin"
            )

            cursor = conn.cursor()

            query = f"DELETE FROM despesas WHERE tipo = %s AND valor = %s AND descricao = %s AND data = %s AND id_usuario = %s AND id_pagamento = %s AND id_responsavel = %s"
            cursor.execute(query, (data["tipo"], data["valor"], data["descricao"], data["data"], id_user, bank, resp,))
            conn.commit()

            cursor.close()
            conn.close()
        
        return 1
    
    except Exception as e:
        print(e)
        return 0