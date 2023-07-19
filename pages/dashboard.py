from app import *
from dash.exceptions import PreventUpdate
from navbar import *
from funcoes import *

graph_config = {"displayModeBar": False, "showTips": False, "scrollZoom": False, "editSelection": False}

def render_dashboard(usuario):
    
    layout = dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            define_navbar(usuario),

                            dbc.Row([
                                dbc.Col([
                                    # Coluna do lado esquerdo responsável pelos filtros e graficos de analise
                                    dbc.Row([
                                        # Linha responsável pelos filtros
                                        dbc.Col([
                                            # Radio item mês-ano clas radio-options
                                            html.Legend("Selecione uma opção de visualização", className="dash-legend"),
                                            dbc.RadioItems([
                                                {"label": "Mês", "value": "mes"}, {"label": "Ano", "value": "ano"}
                                            ],
                                            id="radio-view",
                                            value="mes",
                                            inline=True,
                                            class_name="mb-3",
                                            style={
                                                        "justify-content": "center",
                                                        "align-items": "center",
                                                        "display":"flex"
                                                    }
                                            )
                                        ], sm=12, md=6),


                                        dbc.Col([
                                            # Select mês ou ano
                                            html.Legend("Selecione uma opção", className="dash-legend", style={"margin-top": 10}),
                                            dbc.Select(size="md", class_name="select", id="select-ano-mes")

                                        ], sm=12, md=6, align="center"),
                                    ], justify="center", align="center"),

                                    dbc.Row([
                                        # Grafico de entrada e saída
                                        dbc.Col([
                                            dbc.Spinner(dcc.Graph(id="entrada-saida-graph", config=graph_config))
                                        ])
                                    ]),

                                    dbc.Row([
                                        # Grafico de fluxo de caixa
                                        dbc.Col([
                                            dbc.Spinner(dcc.Graph(id="fluxo-caixa-graph", config=graph_config))
                                        ])
                                    ]),

                                ], sm=12, md=8),

                                dbc.Col([
                                    # Coluna do lado direito contendo saldos e status do cartão
                                    dbc.Row([
                                        # Linha responsável por conter os cards de entrada, saída e saldo geral
                                        dbc.Col([
                                            html.H4("Resultados Gerais", style={"fontStyle": "italic", "textAlign": "center"}),
                                            dbc.CardGroup([
                                                dbc.Card([
                                                    html.Legend("Entradas", className="dash-legend"),
                                                    html.H5("R$ - ", id="valor-entradas", className="dash-legend")
                                                ]),

                                                dbc.Card(
                                                    html.Div(DashIconify(icon="guidance:bank", width=100, height=65), className="card-icon"),
                                                    color="info")
                                                ], class_name="card-group"),

                                            dbc.CardGroup([
                                                dbc.Card([
                                                    html.Legend("Saídas", className="dash-legend"),
                                                    html.H5("R$ - ", id="valor-saidas", className="dash-legend")
                                                ]),

                                                dbc.Card(
                                                    html.Div(DashIconify(icon="material-symbols:money-off", width=100, height=65), className="card-icon"),
                                                    color="primary"
                                                )
                                            ], class_name="card-group"),

                                            dbc.CardGroup([
                                                dbc.Card([
                                                    html.Legend("Saldo", className="dash-legend"),
                                                    html.H5("R$ - ", id="valor-saldos", className="dash-legend")
                                                ]),

                                                dbc.Card(
                                                    html.Div(DashIconify(icon="material-symbols:balance", width=100, height=65), className="card-icon-balance"),
                                                    color="secondary"
                                                )
                                            ], class_name="card-group")
                                        ])
                                    ]),

                                    dbc.Row([
                                        # Linha responsável por conter os dados de cartão
                                        dbc.Col([
                                            html.H4("Status do cartão", style={"fontStyle": "italic", "textAlign": "center"}),
                                            html.Div(id="cartao-status")
                                        ])
                                    ]),
                                ], sm=12, md=4)
                            ])

                        ], sm=12)
                            ])
                ], class_name="dashboard-container", fluid=True)

    return layout


@app.callback(
    Output("logout-state", "data"),

    Input("logout-button", "n_clicks"),
)
def logout(n_clicks):
    if n_clicks == None:
        raise PreventUpdate
    
    if current_user.is_authenticated:
        logout_user()
        return 1
    else: 
        return 1


@app.callback(
    Output("page-state", "data"),

    Input("lancamentos-button", "n_clicks"),
    Input("dashboard-button", "n_clicks")
)
def update_dash_layout(n_clicks1, n_clicks2):

    trigger = dash.callback_context.triggered_id

    if trigger:
        if trigger == "dashboard-button":
            return 1
        
        else:
            return 2

    else:
        raise PreventUpdate


@app.callback(
    Output("select-ano-mes", "options"),
    Output("select-ano-mes", "value"),

    Input("radio-view", "value"),

    State("user-receitas", "data"),
    State("user-despesas", "data")
)
def update_select(radio, receitas, despesas):
    # receitas = {'id': {'0': 3}, 'tipo': {'0': 'Inss'}, 'valor': {'0': 539}, 'descricao': {'0': 'Auxilio Por Incapacidade'}, 'data': {'0': '2023-06-21'}, 'id_usuario': {'0': 2}}
    # despesas = {'id': {'0': 2}, 'tipo': {'0': 'Gasolina'}, 'valor': {'0': 20}, 'descricao': {'0': 'Gasolina Posto Carijó'}, 'data': {'0': '2023-06-24'}, 'id_usuario': {'0': 2}, 'id_pagamento': {'0': 3}, 'id_responsavel': {'0': 1}}


    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)

    if len(df_despesas) or len(df_receitas) > 0:
        coluna = "mes-ano" if radio == "mes" else "ano"
        if len(df_despesas) and len(df_receitas) > 0:

            df_receitas["data"] = pd.to_datetime(df_receitas["data"])
            df_despesas["data"] = pd.to_datetime(df_despesas["data"])

            if coluna == "mes-ano":
                df_receitas[coluna] = df_receitas["data"].apply(lambda x: f"{x.month}-{x.year}")
                df_despesas[coluna] = df_despesas["data"].apply(lambda x: f"{x.month}-{x.year}")
            else:
                df_receitas[coluna] = df_receitas["data"].apply(lambda x: x.year)
                df_despesas[coluna] = df_despesas["data"].apply(lambda x: x.year)

            
            df_result = pd.concat([df_receitas, df_despesas])
            data = df_result[coluna].unique()

        
        elif len(df_despesas) == 0:
            
            df_receitas["data"] = pd.to_datetime(df_receitas["data"])

            if coluna == "mes-ano":
                df_receitas[coluna] = df_receitas["data"].apply(lambda x: f"{x.month}-{x.year}")
            else:
                df_receitas[coluna] = df_receitas["data"].apply(lambda x: x.year)
            

            data = df_receitas[coluna].unique()
            
        
        else:
            df_despesas["data"] = pd.to_datetime(df_despesas["data"])

            if coluna == "mes-ano":
                df_despesas[coluna] = df_despesas["data"].apply(lambda x: f"{x.month}-{x.year}")
            else:
                df_despesas[coluna] = df_despesas["data"].apply(lambda x: x.year)

            data = df_despesas[coluna].unique()
            
        
        data = np.sort(data)[::-1]
        options = [{"label": str(i), "value": str(i)} for i in data]
        value = options[0]["value"]
        
        return options, value


    else:
        return [{"label": "Sem informações", "value": "Sem informacoes"}], "Sem informacoes"


@app.callback(
    Output("entrada-saida-graph", "figure"),
    Output("fluxo-caixa-graph", "figure"),
    Output("valor-entradas", "children"),
    Output("valor-saidas", "children"),
    Output("valor-saldos", "children"),
    Output("cartao-status", "children"),

    Input("select-ano-mes", "value"),

    State("user-receitas","data"),
    State("user-despesas","data"),
    State("user-bancos","data"),
)
def update_dashboard_layout(select, receitas, despesas, banco):

    #select = "2023"

    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)
    df_banco = pd.DataFrame(banco)

    if select != "Sem informacoes":

        if len(df_despesas) > 0 and len(df_receitas) > 0:

            df_receitas["data"] = pd.to_datetime(df_receitas["data"])
            df_despesas["data"] = pd.to_datetime(df_despesas["data"])

            if "-" in select:
                
                df_receitas["mes-ano"] = df_receitas["data"].apply(lambda x: f"{x.month}-{x.year}")
                df_despesas["mes-ano"] = df_despesas["data"].apply(lambda x: f"{x.month}-{x.year}")
                
                df_receitas_filtered = df_receitas[df_receitas["mes-ano"] == select].copy()
                df_despesas_filtered = df_despesas[df_despesas["mes-ano"] == select].copy()

                df_receitas_filtered.rename(columns={"valor": "Receitas"}, inplace=True)
                df_despesas_filtered.rename(columns={"valor": "Despesas"}, inplace=True)

                df_receitas_filtered["Dias"] = df_receitas_filtered["data"].apply(lambda x: x.day)
                df_despesas_filtered["Dias"] = df_despesas_filtered["data"].apply(lambda x: x.day)

                eixo_x = "Dias"
            
            else:
                df_receitas["ano"] = df_receitas["data"].apply(lambda x: x.year)
                df_despesas["ano"] = df_despesas["data"].apply(lambda x: x.year)

                df_receitas_filtered = df_receitas[df_receitas["ano"] == int(select)].copy()
                df_despesas_filtered = df_despesas[df_despesas["ano"] == int(select)].copy()

                df_receitas_filtered.rename(columns={"valor": "Receitas"}, inplace=True)
                df_despesas_filtered.rename(columns={"valor": "Despesas"}, inplace=True)

                df_receitas_filtered["Mes"] = df_receitas_filtered["data"].apply(lambda x: x.month)
                df_despesas_filtered["Mes"] = df_despesas_filtered["data"].apply(lambda x: x.month)      

                eixo_x = "Mes"

            total_despesa = round(float(df_despesas["valor"].sum()),2)
            total_receita = round(float(df_receitas["valor"].sum()),2)

            return graph_com_informacao_total(df_receitas_filtered, df_despesas_filtered, df_banco, df_despesas,total_despesa, total_receita, eixo_x)
        
        elif len(df_despesas) > 0:

            df_despesas["data"] = pd.to_datetime(df_despesas["data"])

            if "-" in select:

                df_despesas["mes-ano"] = df_despesas["data"].apply(lambda x: f"{x.month}-{x.year}")
                
                df_despesas_filtered = df_despesas[df_despesas["mes-ano"] == select].copy()

                df_despesas_filtered.rename(columns={"valor": "Despesas"}, inplace=True)

                df_despesas_filtered["Dias"] = df_despesas_filtered["data"].apply(lambda x: x.day)

                eixo_x = "Dias"
            
            else:

                df_despesas["ano"] = df_despesas["data"].apply(lambda x: x.year)

                df_despesas_filtered = df_despesas[df_despesas["ano"] == int(select)].copy()

                df_despesas_filtered.rename(columns={"valor": "Despesas"}, inplace=True)

                df_receitas_filtered["Mes"] = df_receitas_filtered["data"].apply(lambda x: x.month)      

                eixo_x = "Mes"

            total_despesa = round(float(df_despesas["valor"].sum()),2)
            total_receita = 0
        
            return graph_sem_receitas(df_despesas_filtered, df_banco,df_despesas, total_despesa, total_receita, eixo_x)
        
        else:
            
            if "-" in select:
                
                df_receitas["mes-ano"] = df_receitas["data"].apply(lambda x: f"{x.month}-{x.year}")
                
                df_receitas_filtered = df_receitas[df_receitas["mes-ano"] == select]

                df_receitas_filtered.rename(columns={"valor": "Receitas"}, inplace=True)

                df_receitas_filtered["Dias"] = df_receitas_filtered["data"].apply(lambda x: x.day)

                eixo_x = "Dias"
            
            else:
                df_receitas["ano"] = df_receitas["data"].apply(lambda x: x.year)

                df_receitas_filtered = df_receitas[df_receitas["ano"] == int(select)]

                df_receitas_filtered.rename(columns={"valor": "Receitas"}, inplace=True)

                df_receitas_filtered["Mes"] = df_receitas_filtered["data"].apply(lambda x: x.month)     

                eixo_x = "Mes"

            total_despesa = 0
            total_receita = round(float(df_receitas["valor"].sum()),2)

            return graph_sem_despesas(df_receitas_filtered, total_despesa, total_receita, eixo_x)
        


    else:
        graph_entrada_saida, graph_fluxo_caixa, valor, valor, valor, card = graph_sem_informacao()

        return graph_entrada_saida, graph_fluxo_caixa, valor, valor, valor, card




