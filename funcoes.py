import psycopg2
from werkzeug.security import generate_password_hash
from app import *

margin = {"l":0, "r":0, "t":30, "b":0}
dict_empty = {"Dias": [0], "Valor": [0]}


def verifica_email(email):

    if email == None:
        return True

    test = len(email.split("@")) == 2 

    if (".com" not in email) and (("@gmail" not in email) or ("@hotmail" not in email) or ("@outlook" not in email)) or (test == False):
        return True
    else:
        return False
    

def valida_senha(password):

    if password == "" or password == None:
        return False

    caracteres_especiais = "!@#$%^&*"
    caracteres = False
    maiusculo = False
    numero = False
    tamanho = False

    if len(password) >= 8:
        tamanho = True

    for caracter in password:
        if caracter in caracteres_especiais:
            caracteres = True
        
        if caracter.isupper():
            maiusculo = True

        if caracter.isdigit():
            numero = True
        
    
    if tamanho and caracteres and maiusculo and numero:
        return "Senha forte!"
    elif not tamanho and not caracteres and not maiusculo and not numero:
        return "Senha fraca!"
    else:
        return "Senha média!"
    

def define_style(password):

    if password == "Senha forte!":
        return {"color": "green"}
    elif password == "Senha fraca!":
        return {}
    else:
        return {"color": "orange"}
    

def verifica_usuario_banco_de_dados(email):
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )

    cursor = conn.cursor()

    query = "SELECT id, usuario, password, email FROM usuarios WHERE email=%s"

    cursor.execute(query, ( email, ))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def registra_usuario_banco_de_dados(user, email, password):
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )

    hash_password = generate_password_hash(password, method='sha256')

    cursor = conn.cursor()

    query = "INSERT INTO usuarios (usuario, password, email) VALUES (%s, %s, %s)"

    cursor.execute(query, (user, hash_password, email,))
    conn.commit()

    cursor.close()
    conn.close()


def loga_usuario_banco_de_dados(id):
    conn = psycopg2.connect(
        host="localhost",
        database="financas",
        user="postgres",
        password="admin"
    )

    cursor = conn.cursor()

    query = "SELECT id, usuario FROM usuarios WHERE id=%s"

    cursor.execute(query, ( id, ))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def graph_sem_informacao():

    graph_entrada_saida = px.bar(dict_empty,x="Dias", y="Valor", title="Entradas e saídas")
    graph_entrada_saida.add_annotation(text="Sem informações", xref="paper", yref="paper", showarrow=False)
    graph_entrada_saida.update_layout(margin=margin, height=360)

    graph_fluxo_caixa = px.line(dict_empty, x="Dias", y="Valor", title="Fluxo de caixa")
    graph_fluxo_caixa.add_annotation(text="Sem informações", xref="paper", yref="paper", showarrow=False)
    graph_fluxo_caixa.update_layout(margin=margin, height=360)

    valor = "R$ -"

    card = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody("Sem informações")
            ])
        ])
    ])

    return graph_entrada_saida, graph_fluxo_caixa, valor, valor, valor, card


def graph_com_informacao_total(df_receitas_filtered, df_despesas_filtered, df_banco, df_despesas, total_despesa, total_receita, eixo_x ):
    df_graph_entrada_saida = pd.concat([df_receitas_filtered[[eixo_x, "Receitas"]], df_despesas_filtered[[eixo_x, "Despesas"]]])

    df_graph_entrada_saida.fillna(0, inplace=True)

    graph_entrada_saida = px.bar(title="Entradas e saídas", barmode='group')
    graph_entrada_saida.add_bar(x=df_graph_entrada_saida[eixo_x], y=df_graph_entrada_saida["Despesas"], name="Despesas", marker_color="#FF3D00")
    graph_entrada_saida.add_bar(x=df_graph_entrada_saida[eixo_x], y=df_graph_entrada_saida["Receitas"], name="Receitas", marker_color="#25B4F1")
    graph_entrada_saida.update_layout(margin=margin, height=360, xaxis_title=eixo_x, yaxis_title="Valores (R$)")
    graph_entrada_saida.update_xaxes(tickvals=df_graph_entrada_saida[eixo_x].unique())


    df_fluxo_caixa = pd.concat([df_receitas_filtered[[eixo_x, "Receitas"]], df_despesas_filtered[[eixo_x, "Despesas"]]]).fillna(0)
    df_fluxo_caixa["Fluxo"] = df_fluxo_caixa["Receitas"] - df_fluxo_caixa["Despesas"]
    df_fluxo_caixa.sort_values(eixo_x, inplace=True)
    df_fluxo_caixa["Acumulado"] = df_fluxo_caixa["Fluxo"].cumsum()

    if len(df_fluxo_caixa[eixo_x].unique()) > 1:

        graph_fluxo_caixa = px.line(df_fluxo_caixa, x=eixo_x, y="Acumulado", title="Fluxo de caixa")
    else:
        df_fluxo_caixa = df_fluxo_caixa.groupby(eixo_x).agg({"Fluxo": "sum"}).reset_index().rename(columns={"Fluxo": "Acumulado"})

        graph_fluxo_caixa = px.scatter(df_fluxo_caixa, x=eixo_x, y="Acumulado", title="Fluxo de caixa")

    graph_fluxo_caixa.update_layout( height=360, margin=margin, yaxis_title="Valor")
    graph_fluxo_caixa.update_xaxes(tickvals=df_graph_entrada_saida[eixo_x].unique())


    entradas = f'R$ {total_receita}'
    saidas = f'R$ {total_despesa}'
    saldo = f"R$ {round(total_receita - total_despesa,2)}"

    bancos = [{"id":0, "nome": "Desconhecido", "eu": 0, "terceiros": 0}]
    list_cards = []


    for index, row in df_banco.iterrows():
        if row["id"] != 1:
            bank_dict = {"id": row["id"], "nome": row["nome"], "eu": 0, "terceiros": 0}
            bancos.append(bank_dict)


    for index, row in df_despesas.iterrows():
        if row["id_pagamento"] != 1:

            valider = True
            for i in bancos:
                if row["id_pagamento"] == i["id"]:
                    if row["id_responsavel"] == 1:
                        i["eu"] = i["eu"] + row["valor"]
                    else:
                        i["terceiros"] = i["terceiros"] + row["valor"]

                    valider = False
                    break
            
            if valider:
                if row["id_responsavel"] == 1:
                    bancos[0]["eu"] = bancos[0]["eu"] + row["valor"]
                else:
                    bancos[0]["terceiros"] = bancos[0]["terceiros"] + row["valor"]
    
    new_bancos = []
    i = 0
    for bank in bancos:
        if bank["eu"] != 0 or bank["terceiros"] != 0:
            new_bancos.append(bank)
        i+=1

    for bank in new_bancos:

        new_card = dbc.CardGroup([
            dbc.Card([

                html.Legend(f'Valor total: R$ {round(float(bank["eu"]), 2)+round(float(bank["terceiros"]), 2)}',className="status-info"),
                html.Legend(f'Eu - R$ {round(float(bank["eu"]), 2)}', style={"color": "#FF3D00"}, className="status-info"),
                html.Legend(f'Terceiros - R$ {round(float(bank["terceiros"]), 2)}', style={"color": "#25B4F1"}, className="status-info")
            ]),

            dbc.Card([
                html.Legend(bank["nome"], className="status-name-bank")               
            ])
        ], style={"margin-top": 10})

        list_cards.append(new_card)

    return graph_entrada_saida, graph_fluxo_caixa, entradas, saidas, saldo, list_cards


def graph_sem_receitas(df_despesas_filtered, df_banco, df_despesas, total_despesa, total_receita, eixo_x ):
   
    graph_entrada_saida = px.bar(title="Entradas e saídas", barmode='group')
    graph_entrada_saida.add_bar(x=df_despesas_filtered[eixo_x], y=df_despesas_filtered["Despesas"], name="Despesas", marker_color="#25B4F1")
    graph_entrada_saida.update_layout(margin=margin, height=360, xaxis_title=eixo_x, yaxis_title="Valores (R$)")
    graph_entrada_saida.update_xaxes(tickvals=df_despesas_filtered[eixo_x].unique())

    df_despesas.sort_values(eixo_x, inplace=True)
    df_despesas["Acumulado"] = (-1 * df_despesas["valor"]).cumsum()

    if len(df_despesas_filtered[eixo_x].unique()) > 1:
        graph_fluxo_caixa = px.line(df_despesas_filtered, x=eixo_x, y="Acumulado", title="Fluxo de caixa")
    
    else:
        df_despesas_filtered = df_despesas_filtered.groupby(eixo_x).agg({"valor": "sum"}).reset_index()
        graph_fluxo_caixa = px.scatter(df_despesas_filtered, x=eixo_x, y="valor", title="Fluxo de caixa")

    graph_fluxo_caixa.update_layout( height=360, margin=margin, yaxis_title="Valores (R$)")
    graph_fluxo_caixa.update_xaxes(tickvals=df_despesas_filtered[eixo_x].unique())



    entradas = f'R$ {total_receita}'
    saidas = f'R$ {total_despesa}'
    saldo = f"R$ {round(total_receita - total_despesa,2)}"

    bancos = [{"id":0, "nome": "Desconhecido", "eu": 0, "terceiros": 0}]
    list_cards = []

    for index, row in df_banco.iterrows():
        if row["id"] != 1:
            bank_dict = {"id": row["id"], "nome": row["nome"], "eu": 0, "terceiros": 0}
            bancos.append(bank_dict)


    for index, row in df_despesas.iterrows():
        if row["id_pagamento"] != 1:

            valider = True
            for i in bancos:
                if row["id_pagamento"] == i["id"]:
                    if row["id_responsavel"] == 1:
                        i["eu"] = i["eu"] + row["valor"]
                    else:
                        i["terceiros"] = i["terceiros"] + row["valor"]

                    valider = False
                    break
            
            if valider:
                if row["id_responsavel"] == 1:
                    bancos[0]["eu"] = bancos[0]["eu"] + row["valor"]
                else:
                    bancos[0]["terceiros"] = bancos[0]["terceiros"] + row["valor"]
    
    new_bancos = []
    i = 0
    for bank in bancos:
        if bank["eu"] != 0 or bank["terceiros"] != 0:
            new_bancos.append(bank)
        i+=1


    for bank in new_bancos:

        new_card = dbc.Card([

            dbc.CardHeader(html.Legend(bank["nome"], className="status-name-bank")),

            dbc.CardBody([
                html.Label(f'Eu - R$ {round(float(bank["eu"]), 2)}', style={"color": "#FF3D00"}, className="status-info"),
                html.Label(f'Terceiros - R$ {round(float(bank["terceiros"]), 2)}', style={"color": "#25B4F1"},className="status-info")
            ])
        ], style={"margin-top": 10})

        list_cards.append(new_card)

    return graph_entrada_saida, graph_fluxo_caixa, entradas, saidas, saldo, list_cards


def graph_sem_despesas(df_receitas_filtered, total_despesa, total_receita, eixo_x ):
    
    graph_entrada_saida = px.bar(title="Entradas e saídas", barmode='group')
    graph_entrada_saida.add_bar(x=df_receitas_filtered[eixo_x], y=df_receitas_filtered["Receitas"], name="Receitas", marker_color="#FF3D00")
    graph_entrada_saida.update_layout(margin=margin, height=360, xaxis_title=eixo_x, yaxis_title="Valores (R$)")
    graph_entrada_saida.update_xaxes(tickvals=df_receitas_filtered[eixo_x].unique())

    df_receitas_filtered.sort_values(eixo_x, inplace=True)
    df_receitas_filtered["Acumulado"] = df_receitas_filtered["valor"].cumsum()

    if len(df_receitas_filtered[eixo_x].unique()) > 1:
        graph_fluxo_caixa = px.line(df_receitas_filtered, x=eixo_x, y="Acumulado", title="Fluxo de caixa")
    else:
        df_receitas_filtered = df_receitas_filtered.groupby(eixo_x).agg({"valor": "sum"}).reset_index()

        graph_fluxo_caixa = px.scatter(df_receitas_filtered, x=eixo_x, y="valor", title="Fluxo de caixa")

 
    graph_fluxo_caixa.update_layout( height=360, margin=margin, yaxis_title="Valor")
    graph_fluxo_caixa.update_xaxes(tickvals=df_receitas_filtered[eixo_x].unique())


    entradas = f'R$ {total_receita}'
    saidas = f'R$ {total_despesa}'
    saldo = f"R$ {round(total_receita - total_despesa,2)}"

    card = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody("Sem informações")
            ])
        ])
    ])
    

    return graph_entrada_saida, graph_fluxo_caixa, entradas, saidas, saldo, card