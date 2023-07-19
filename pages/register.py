from app import *
from funcoes import *

# ===================== Layout =======================

def render_register(state):

    if state == 0:
        message = ""
    elif state == 2:
        message = "Email já cadastrado!"
    elif state == 3:
        message = "Erro ao cadastrar! Tente novamente!"

    register =  dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H2("Bem-vindo(a) ao Get Organized", id="login-title"),
                        html.P("Insira as informações abaixo para se cadastrar."),

                        html.Legend("Usuario", className="login-legend"),
                        dbc.Input(id="user", placeholder="Digite seu usuario", type="text"),
                        html.P("Usuario vazio", id="user-valider", className="valider", hidden=True),

                        html.Legend("Email", className="login-legend"),
                        dbc.Input(id="email", placeholder="Digite email", type="email"),
                        html.P("Email inválido", id="email-valider", className="valider", hidden=True),

                        html.Legend("Senha", className="login-legend"),
                        dbc.Input(id="in-password", placeholder="Digite sua senha", type="password"),
                        html.P(id="password-valider", className="valider"),
                        dcc.Checklist(id="mostrar-senha", options={"label": "Mostrar senha"}, style={"margin-top": 10}, inputStyle={"margin-right": 10}),

                        html.Legend("Confirmar senha", className="login-legend"),
                        dbc.Input(id="re-password", placeholder="Digite sua senha", type="password"),
                        html.P("Senhas diferentes", id="re-password-valider", className="valider", hidden=True),

                        html.Div([
                            dbc.Button("Register", id="register-button", color="primary", size="lg", disabled=True),
                            
                        ], className="div-login"),
                        html.P(children=message, id="error-register", className="valider", style={"textAlign":"center"}),

                        html.Hr(),
                        html.Div([
                            html.A("Faça login", href="/login")
                        ], className="div-login")
                    ])
                ], class_name="card")
            ], align="center", sm=12)
        ], id="row-login")
    ], class_name="login-register", fluid=True)

    return register


# ===================== callbacks verifica registro =======================

@app.callback(
    Output("user-valider", "hidden"),
    Output("email-valider", "hidden"),
    Output("password-valider", "children"),
    Output("password-valider", "style"),
    Output("re-password-valider", "hidden"),
    Output("register-button", "disabled"),
    Output("error-register", "hidden"),

    Input("user", "value"),
    Input("email", "value"),
    Input("in-password", "value"),
    Input("re-password", "value"),

    State("error-register", "children"),
    prevent_initial_call = True
)
def data_register_valider(user,email, password, password2, error):

    if user != None and user != "":
        if not verifica_email(email):

            senha = valida_senha(password)
            style = define_style(senha)

            if senha:
                if password == password2:
                    return True, True, senha, style, True, False, False
                
                elif password2 == "" or password2 == None:
                    return True, True, senha, style, True, True, True
                
                return True, True, senha, style, False, True, True

            else:
                return True, True, "", style, True, True, True
        
        else:
            if email == None:
                return True, True, "", {}, True, True, True
            return True, False, "", {}, True, True, True
    elif  error != "":
        return  False, True, "", {},True, True, False

    else:
        return False, True, "", {},True, True, True

@app.callback(
    Output("in-password", "type"),
    Output("re-password", "type"),
    
    Input("mostrar-senha", "value")
)
def show_password(value):
    if value:
        return "text", "text"
    return "password", "password"


@app.callback(
    Output("register-state", "data"),

    Input("register-button", "n_clicks"),

    State("user", "value"),
    State("email", "value"),
    State("in-password", "value"),
)
def register_user(n_clicks, user, email, password):
    if not n_clicks:
        return 0
    
    result = verifica_usuario_banco_de_dados(email)

    if result:
        return 2

    else:
        try:
            registra_usuario_banco_de_dados(user, email, password)
            
            return 1
        except:
            return 3


# 1 - OK
# 2 - Email existente
# 3 - Erro ao cadastrar