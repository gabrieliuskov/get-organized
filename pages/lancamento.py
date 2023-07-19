from app import *
from navbar import *
from data import *


def render_lancamento(usuario):
    layout = dbc.Container([

                    dbc.Row([
                        dbc.Col([
                            define_navbar(usuario),

                            dbc.Row([
                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader([html.Legend("Visualizar dados", className="dash-legend"),]),
                                        dbc.CardBody([
                                            html.Div([
                                                dbc.Button("Visualizar receitas", id="view-receitas", color="info", size="lg", class_name="lancamento-button"),
                                                dbc.Button("Visualizar despesas", id="view-despesas", color="primary", size="lg", class_name="lancamento-button"),
                                                dbc.Button("Visualizar bancos", id="view-bancos", color="secondary", size="lg", class_name="lancamento-button"),
                                            ])                                                        
                                        ])],class_name="option-card"
                                    ),

                                    dbc.Card([
                                        dbc.CardHeader([html.Legend("Adicionar dados", className="dash-legend"),]),
                                        dbc.CardBody([
                                            html.Div([
                                                dbc.Button("+ Receita", color="info",  id="add-receita", size="lg", class_name="lancamento-button"),
                                                dbc.Button("+ Despesa", color="primary",  id="add-despesa", size="lg", class_name="lancamento-button"),
                                                dbc.Button("+ Banco", color="secondary",  id="add-banco", size="lg", class_name="lancamento-button"),
                                            ]) 
                                        ])
                                    ], class_name="option-card")
                                ], sm=12, md=2),

                                dbc.Col([
                                    dbc.Card([
                                        dbc.CardHeader(html.Legend("Clique em alguma visualização para analisar os dados",id="table-name", className="dash-legend")),

                                        dbc.CardBody([
                                            dash_table.DataTable(id="lancamento-table", page_current=0, page_size=5, row_selectable="single"),
                                            html.Div(id="edit-div")
                                            ])
                                    ], class_name="table-card"),

                                ], sm=12, md=10)
                            ], class_name="row-lancamento"),


                            dbc.Modal([
                                dbc.ModalHeader(dbc.ModalTitle("Adicionar Receita")),

                                dbc.ModalBody([
                                    dbc.Label("Descrição", class_name="modal-labels"),
                                    dbc.Input(id="modal-descricao-receita", type="text", placeholder="Ex: Salário da empresa", class_name="modal-inputs"),

                                    dbc.Label("Data da receita", class_name="modal-labels"),
                                    html.Div(dcc.DatePickerSingle(date=datetime.today().date(), className="modal-inputs", id="modal-data-receita")),

                                    dbc.Label("Valor", class_name="modal-labels"),
                                    dbc.Input(id="modal-valor-receita", type="number", placeholder="Ex: 5000.50", class_name="modal-inputs"),

                                    dbc.Label("Tipo de receita", class_name="modal-labels"),
                                    dbc.Input(id="modal-tipo-receita", type="text", placeholder="Ex: Salário", class_name="modal-inputs"),

                                    dbc.Button("Adicionar", id="adiciona-receita-button", color="info", class_name="modal-button", disabled=True)
                                ])
                            ],
                            id="receita-modal",
                            is_open=False,
                            size="xl",
                            scrollable=True,
                            centered=True,
                            autofocus=True),

                            dbc.Modal([
                                dbc.ModalHeader(dbc.ModalTitle("Adicionar Despesa")),

                                dbc.ModalBody([
                                    dbc.Label("Descrição", class_name="modal-labels"),
                                    dbc.Input(id="modal-descricao-despesa", type="text", placeholder="Ex: Medicamentos para cirugia", class_name="modal-inputs"),

                                    dbc.Label("Data da despesa", class_name="modal-labels"),
                                    html.Div(dcc.DatePickerSingle(date=datetime.today().date(), className="modal-inputs", id="modal-data-despesa")),


                                    dbc.Label("Valor", class_name="modal-labels"),
                                    dbc.Input(id="modal-valor-despesa", type="number", placeholder="Ex: 1000.48", class_name="modal-inputs"),

                                    dbc.Label("Tipo de despesa", class_name="modal-labels"),
                                    dbc.Input(id="modal-tipo-despesa", type="text", placeholder="Ex: Remédios", class_name="modal-inputs"),

                                    dbc.Label("Forma de pagamento", class_name="modal-labels"),
                                    dbc.Select(id="pagamento-despesa", class_name="modal-inputs"),

                                    dbc.Label("Responsável", class_name="modal-labels"),
                                    dbc.Select(options=[{"label": "Eu", "value": 1},
                                                        {"label": "Terceiros", "value": 2} 
                                                        ],
                                                        id="responsavel-despesa", value=1, class_name="modal-inputs"),

                                    dbc.Button("Adicionar", id="adiciona-despesa-button", color="primary", class_name="modal-button", disabled=True)
                                ])
                            ],
                            id="despesa-modal",
                            is_open=False,
                            size="xl",
                            scrollable=True,
                            centered=True,
                            autofocus=True),

                            dbc.Modal([
                                dbc.ModalHeader(dbc.ModalTitle("Adicionar Banco")),

                                dbc.ModalBody([
                                    dbc.Label("Banco", class_name="modal-labels"),
                                    dbc.Input(id="banco", type="text", placeholder="Ex: Nubank", class_name="modal-inputs"),
                                    html.P(id="banco-error", children="Banco ou forma de pagamento já cadastrado!", hidden=True, className="valider"),

                                    dbc.Button("Adicionar", id="adiciona-banco-button", color="secondary", class_name="modal-button", disabled=True)
                                ]),

                                html.Hr(),

                                dbc.Accordion([
                                    dbc.AccordionItem([
                                        html.Label("Selecione o banco para deletar."),
                                        dbc.Select(id="deletar-banco-select"),
                                        dbc.Button("Confirmar", id="deletar-banco-button", class_name="modal-button", disabled=True, color="danger")

                                    ], title="Deletar banco",)
                                ], start_collapsed=True)
                            ],
                            id="banco-modal",
                            is_open=False,
                            size="xl",
                            scrollable=True,
                            centered=True,
                            autofocus=True),



                        ], sm=12)
                    ])
                ], class_name="dashboard-container", fluid=True)

    return layout


@app.callback(
        Output("lancamento-table", "data"),
        Output("lancamento-table", "columns"),
        Output("table-name", "children"),
        Output("table-div-data", "data"),

        Input("view-receitas", "n_clicks"),
        Input("view-despesas", "n_clicks"),
        Input("view-bancos", "n_clicks"),

        State("user-receitas", "data"),
        State("user-despesas", "data"),
        State("user-bancos", "data"),
        State("table-div-data", "data")
)
def update_table(n1, n2, n3, receitas, despesas, bancos, data):
    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)
    df_bancos = pd.DataFrame(bancos)

    trigger = dash.callback_context.triggered

    if len(trigger) > 1:
        return None, None, "Clique em alguma visualização para analisar os dados", 0

    if trigger[0]["prop_id"].split(".")[0] == "view-receitas":

        df_receitas.drop(["id_usuario", "id"], axis=1, inplace=True)
        df_receitas.fillna("-", inplace=True)

        return df_receitas.to_dict("records"), [{"name": str(i).title(), "id": i} for i in df_receitas.columns], "Receitas Lançadas", 1
    
    elif trigger[0]["prop_id"].split(".")[0] == "view-despesas":
        dict_bancos = {}
        dict_resp = {1: "Eu", 2: "Terceiros"}

        for index,row in df_bancos.iterrows():
            dict_bancos[row["id"]] = row["nome"]

        df_despesas.drop(["id_usuario", "id"], axis=1, inplace=True)
        df_despesas["id_pagamento"] = df_despesas["id_pagamento"].map(dict_bancos)
        df_despesas["id_responsavel"] = df_despesas["id_responsavel"].map(dict_resp)
        df_despesas.rename(columns={"id_pagamento": "Pagamento", "id_responsavel": "Responsavel"}, inplace=True)
        df_despesas.fillna("-", inplace=True)

        return df_despesas.to_dict("records"), [{"name": str(i).title(), "id": i} for i in df_despesas.columns], "Despesas Lançadas", 2
    
    elif trigger[0]["prop_id"].split(".")[0] == "view-bancos":

        df_bancos.drop(df_bancos[df_bancos["id"] == 1].index, inplace=True)
        df_bancos.drop("id", axis=1, inplace=True)
        df_bancos.rename(columns={"nome": "Banco"}, inplace=True)
        df_bancos.fillna("-", inplace=True)

        return df_bancos.to_dict("records"), [{"name": str(i).title(), "id": i} for i in df_bancos.columns], "Bancos Cadastrados", 3
    else:
        raise PreventUpdate
    


@app.callback(
        Output("pagamento-despesa", "options"),
        Output("pagamento-despesa", "value"),

        Input("despesa-modal", "is_open"),

        State("user-bancos", "data"),
)
def cria_forma_pagamento(is_open, data):

    if is_open:
        df_banco = pd.DataFrame(data)

        lista = [{"label": str(i).title(), "value": j} for i, j in zip(df_banco["nome"].unique(), df_banco["id"])]
        valor = lista[0]["value"]
        
        return lista, valor
        
    else:
        raise PreventUpdate
    

@app.callback(
        Output("deletar-banco-select", "options"),

        Input("banco-modal", "is_open"),

        State("user-bancos", "data")
)
def adiciona_bancos_deletar(is_open, data):

    if is_open:
        df_banco = pd.DataFrame(data) 

        lista = [{"label": str(i).title(), "value": j, "disabled": False} for i, j in zip(df_banco["nome"].unique(), df_banco["id"].unique())]

        for i in lista:
            if i["label"] == "Dinheiro":
                i["disabled"] = True
        
        return lista
        
    else:
        raise PreventUpdate


@app.callback(
        Output("edit-div", "children"),
        Output("row-data", "data"),

        Input("lancamento-table", "derived_virtual_data"),
        Input("lancamento-table", "derived_virtual_selected_rows"),
        Input("table-div-data", "data"),


        State("user-bancos", "data")

)
def atualiza_edit_div(virtual_data, virtual_selected_row, table_div_data, bancos):

    df_bancos = pd.DataFrame(bancos)
    
    if table_div_data == 1:

        if len(virtual_selected_row) > 0:

            row = virtual_data[virtual_selected_row[0]]
            
            edit_div = dbc.Row([          
                html.Legend("Deletar receitas", className="table-title"),

                html.Label("Tipo: ", className="table-label"),
                dbc.Input(id="receitas-tipo", value=row["tipo"], className="table-input", disabled=True),

                html.Label("Valor: ", className="table-label"),
                dbc.Input(id="receitas-valor",value=row["valor"], className="table-input", disabled=True),

                html.Label("Descrição: ", className="table-label"),
                dbc.Input(id="receitas-descricao", value=row["descricao"], className="table-input", disabled=True),

                html.Label("Data: ", className="table-label"),
                dcc.DatePickerSingle(date=row["data"], className="table-input", id="data-table", disabled=True),

                dbc.Button("Deletar registro", size="md", class_name="table-button", color="danger", id="delete", n_clicks=0)
            ])

            return edit_div, row

        else:
            edit_div = dbc.Row([          
            html.Legend("Deletar receitas", className="table-title"),

            html.Label("Tipo: ", className="table-label"),
            dbc.Input(id="receitas-tipo", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

            html.Label("Valor: ", className="table-label"),
            dbc.Input(id="receitas-valor", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

            html.Label("Descrição: ", className="table-label"),
            dbc.Input(id="receitas-descricao", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

            html.Label("Data: ", className="table-label"),
            dcc.DatePickerSingle(className="table-input", id="modal-data-despesa", disabled=True),

            dbc.Button("Deletar registro", disabled=True, size="md", class_name="table-button", color="danger", id="delete", n_clicks=0)
            ])

            return edit_div, ""
    
    elif table_div_data == 2:
        if len(virtual_selected_row) > 0:

            row = virtual_data[virtual_selected_row[0]]

            for index, item in df_bancos.iterrows():
                if row["Pagamento"] == item["nome"]:
                    pagamento = item["id"]

            resp = 1 if row["Responsavel"] == "Eu" else 2

            edit_div = dbc.Row([
                html.Legend("Deletar despesas", className="table-title"),

                html.Label("Tipo: ", className="table-label"),
                dbc.Input(id="despesas-tipo", value=row["tipo"], className="table-input", disabled=True),

                html.Label("Valor: ", className="table-label"),
                dbc.Input(id="despesas-valor", value=row["valor"], className="table-input", disabled=True),

                html.Label("Descrição: ", className="table-label"),
                dbc.Input(id="despesas-descricao", value=row["descricao"], className="table-input", disabled=True),

                html.Label("Data: ", className="table-label"),
                dcc.DatePickerSingle(date=row["data"], className="table-input", id="data-table", disabled=True),

                html.Label("Pagamento: ", className="table-label"),
                dbc.Select(options=[{"label": j, "value": i} for i, j in zip(df_bancos["id"],df_bancos["nome"])], value=pagamento, id="select-pagamento", className="table-input", disabled=True),

                html.Label("Responsavel: ", className="table-label"),
                dbc.Select(options=[{"label": "Eu", "value": 1}, {"label": "Terceiros", "value": 2}], value=resp, id="select-responsavel", className="table-input", disabled=True),

                dbc.Button("Deletar registro", size="md", class_name="table-button", color="danger", id="delete", n_clicks=0)
             ])
            
            return edit_div, row
        
        else:
            edit_div = dbc.Row([
                html.Legend("Deletar despesas", className="table-title"),

                html.Label("Tipo: ", className="table-label"),
                dbc.Input(id="despesas-tipo", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

                html.Label("Valor: ", className="table-label"),
                dbc.Input(id="despesas-valor", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

                html.Label("Descrição: ", className="table-label"),
                dbc.Input(id="despesas-descricao", placeholder="Selecione um dado na tabela acima", className="table-input", disabled=True),

                html.Label("Data: ", className="table-label"),
                dcc.DatePickerSingle(disabled=True, className="table-input", id="data-table"),

                html.Label("Pagamento: ", className="table-label"),
                dbc.Select(options=[{"label": j, "value": i} for i, j in zip(df_bancos["id"], df_bancos["nome"])], disabled=True, id="select-pagamento", className="table-input"),

                html.Label("Responsavel: ", className="table-label"),
                dbc.Select(options=[{"label": "Eu", "value": 1}, {"label": "Terceiros", "value": 2}], disabled=True, id="select-responsavel", className="table-input"),

                dbc.Button("Deletar registro", disabled=True, size="md", class_name="table-button", color="danger", id="delete", n_clicks=0)
            ])

            return edit_div, ""
        

    elif table_div_data == 3:
        return "", ""
    
    else:
        raise PreventUpdate


@app.callback(
        Output("trigger-reload-datatable", "data"),

        Input("delete", "n_clicks"),

        State("row-data", "data"),
        State("table-div-data", "data"),
        State("user-bancos", "data"),
        State("trigger-reload-datatable", "data")
)
def delete_data_on_database(n1, data, div_data, banco, value):
    trigger = dash.callback_context.triggered
    
    if len(trigger) > 1 or data == "":
        raise PreventUpdate

    if trigger[0]["prop_id"].split(".")[0] == "delete" and n1 > 0:
        retorno = del_registro(data,div_data, current_user.id, banco)

        if retorno == 1:
            return value + 1
            
    else:
        raise PreventUpdate



@app.callback(
        Output("adiciona-receita-button", "disabled"),

        Input("modal-descricao-receita", "value"),
        Input("modal-data-receita", "date"),
        Input("modal-valor-receita", "value"),
        Input("modal-tipo-receita", "value"),
)
def enable_add_receitas_button(descricao, data, valor, receita):
    if (descricao == "") or (data == "") or (valor == "") or (receita == "") or (descricao == None) or (data == None) or (valor == None) or (receita == None):
        return True
    else:
        return False
  

@app.callback(
        Output("adiciona-despesa-button", "disabled"),

        Input("modal-descricao-despesa", "value"),
        Input("modal-data-despesa", "date"),
        Input("modal-valor-despesa", "value"),
        Input("modal-tipo-despesa", "value"),
        Input("pagamento-despesa", "value"),
        Input("responsavel-despesa", "value"),
)
def enable_add_despesas_button(descricao, data, valor, despesa, pagamento, resp):

    if (descricao == "") or (data == "") or (valor == "") or (despesa == "") or (pagamento == "") or (resp == "") or (descricao == None) or (data == None) or (valor == None) or (despesa == None) or (pagamento == None) or (resp == None):
        return True
    else:
        return False


@app.callback(
        Output("adiciona-banco-button", "disabled"),
        Output("banco-error", "hidden"),

        Input("banco", "value"),
        State("user-bancos", "data")
)
def enable_add_bank_button(nome,data):

    if (nome == "") or (nome == None):
        return True, True
    
    else:
        nome = str(nome).title()
        df_banco = pd.DataFrame(data)

        if nome in df_banco["nome"].unique():
            return True, False

        return False, True


@app.callback(
        Output("deletar-banco-button", "disabled"),

        Input("deletar-banco-select", "value"),
)
def enable_del_bank_button(nome):
    if (nome == "") or (nome == None):
        return True
    else:
        return False


@app.callback(
        Output("modal-descricao-receita", "value"),
        Output("modal-valor-receita", "value"),
        Output("modal-tipo-receita", "value"),
        Output("modal-descricao-despesa", "value"),
        Output("modal-valor-despesa", "value"),
        Output("modal-tipo-despesa", "value"),
        Output("banco", "value"),

        
        Input("trigger-reload-data", "data"),
)
def clean_inputs(trigger):
    return "", "", "", "","", "", ""



@app.callback(
    Output("receita-modal", "is_open"),
    Output("despesa-modal", "is_open"),
    Output("banco-modal", "is_open"),

    Input("add-receita", "n_clicks"),
    Input("add-despesa", "n_clicks"),
    Input("add-banco", "n_clicks"),
    Input("trigger-reload-data", "data"),

    State("receita-modal", "is_open"),
    State("despesa-modal", "is_open"),
    State("banco-modal", "is_open"),

    prevent_initial_call = True
)
def open_modal(n_clicks1, n_clicks2, n_clicks3, n_clicks4, receita, despesa, banco):

    trigger = dash.callback_context.triggered_id
    
    if trigger == "add-receita":
        return not receita, despesa, banco
    elif trigger == "add-despesa":
        return receita, not despesa, banco
    elif trigger == "add-banco":
        return receita, despesa, not banco
    else:
        return False, False, False




@app.callback(
    Output("trigger-reload-data","data"),

    Input("adiciona-receita-button", "n_clicks"),
    Input("adiciona-despesa-button", "n_clicks"),
    Input("adiciona-banco-button", "n_clicks"),
    Input("deletar-banco-button", "n_clicks"),

    State("modal-descricao-receita", "value"),
    State("modal-data-receita", "date"),
    State("modal-valor-receita", "value"),
    State("modal-tipo-receita", "value"),

    State("modal-descricao-despesa", "value"),
    State("modal-data-despesa", "date"),
    State("modal-valor-despesa", "value"),
    State("modal-tipo-despesa", "value"),
    State("pagamento-despesa", "value"),
    State("responsavel-despesa", "value"),


    State("banco", "value"),
    State("deletar-banco-select", "value"),
    State("trigger-reload-data","data"),

    prevent_initial_call = True

)
def change_database_data(n1, n2, n3, n4, receita_descricao, receita_data, receita_valor, receita_tipo, 
                         despesa_descricao, despesa_data, despesa_valor, despesa_tipo, despesa_pagamento, despesa_resp, banco_criar, banco_deletar, valor_trigger):
    
    trigger = dash.callback_context.triggered

    if len(trigger) > 1:
        raise PreventUpdate
    else:
        trigger = dash.callback_context.triggered_id

    if trigger == "adiciona-receita-button":
        receita_descricao = str(receita_descricao).title()
        receita_tipo = str(receita_tipo).title()

        add_receitas(receita_descricao, receita_data, receita_valor, receita_tipo)
        return valor_trigger + 1
    
    elif trigger == "adiciona-despesa-button":
        despesa_descricao = str(despesa_descricao).title()
        despesa_tipo = str(despesa_tipo).title()


        add_despesas(despesa_descricao, despesa_data, despesa_tipo, despesa_pagamento, despesa_resp, despesa_valor)
        return valor_trigger + 1


    elif trigger == "adiciona-banco-button":
        banco_criar = str(banco_criar).title()

        add_banco(banco_criar)
        return valor_trigger + 1


    elif trigger == "deletar-banco-button":
        del_banco(banco_deletar)
        return valor_trigger + 1

    
