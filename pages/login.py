from app import *
from funcoes import *
from data import *


# ===================== Layout =========================
def render_login(state):

    if state == 2:
        message = "Senha incorreta!"
    elif state == 3:
        message = "Email não cadastrado!"
    else:
        message = ""

    

    login =  dbc.Container([
        dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H2("Bem-vindo(a) ao Get Organized", id="login-title"),
                    html.Legend("Email", className="login-legend"),
                    dbc.Input(id="email", placeholder="Digite seu email", type="email"),
                    html.P("Email inválido", hidden=True,id="email-check", className="valider"),

                    html.Legend("Senha", className="login-legend"),
                    dbc.Input(id="password", placeholder="Digite sua senha", type="password"),

                    dcc.Checklist(id="mostrar-senha", options={"label": "Mostrar senha"}, style={"margin-top": 10}, inputStyle={"margin-right": 10}),

                    html.Div([
                        dbc.Button("Login", id="login-button", color="primary", size="lg", disabled=True),
                    ], className="div-login"),
                    html.P(children=message, id="error-message", className="valider", style={"textAlign":"center"}),

                    html.Hr(),
                    html.Div([
                        html.A("Registre-se", href="/register")
                    ], className="div-login")
                ])
            ], class_name="card")
        ], align="center", sm=12)
    ], id="row-login")
    ], class_name="login-register", fluid=True)

    return login



# ===================== callbacks verifica login =======================


@app.callback(
    Output("email-check", "hidden"),
    Output("login-button", "disabled"),
    Output("error-message", "hidden"),

    Input("email", "value"),
    Input("password", "value"),

    prevent_initial_call = True
)
def data_login_valider(email, password):
      
    if email == "":
        return True, True, True

    elif verifica_email(email):       
        return False, True, True
    
    elif password != None:
        return True, False, False

    else:
        return True, True, False


@app.callback(
    Output("password", "type"),

    Input("mostrar-senha", "value")
)
def show_password(value):
    if value:
        return "text"
    return "password"


@app.callback(
    Output("load-user-data", "data"),

    Input("login-button", "n_clicks"),

    State("email", "value"),
    State("password", "value")
)
def logar_usuario(n_clicks, email, password):

    if not n_clicks:
        return 0

    user = verifica_usuario_banco_de_dados(email)
    
    if user != None:
        if check_password_hash(user[2], password):

            
            login_user(User(user[0], user[1]))
            return 1
        else:
            return 2
    else:
        return 3

# 1 -> Sucesso
# 2 -> Senha incorreta
# 3 -> Usuario nao encontrado

@app.callback(
    Output("user-receitas","data"),
    Output("user-despesas","data"),
    Output("user-bancos","data"),
    Output("login-state", "data"), 


    Input("trigger-reload-data", "data"),
    Input("load-user-data", "data"),
    Input("trigger-reload-datatable", "data")
)
def get_data_from_database(reload, user_data, datatable):
    trigger = dash.callback_context.triggered_id

    if (trigger == "load-user-data" and user_data == 1) or (trigger== "trigger-reload-data") or (trigger == "trigger-reload-datatable"):

        receitas, despesas, bancos = get_user_receitas(current_user.id)

        if trigger == "trigger-reload-data":
            return receitas, despesas, bancos, 4

        return receitas, despesas, bancos, user_data
    
    elif (trigger == "load-user-data"):
        return "", "", "", user_data

    else:
        raise PreventUpdate
