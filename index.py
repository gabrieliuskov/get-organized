from app import *
from pages import login, register, dashboard, lancamento
from funcoes import *


# ===================== Layout =========================
app.layout = dbc.Container([
                dcc.Location(id="url", refresh=False),
                dcc.Store(id="login-state", data=0),
                dcc.Store(id="register-state", data=0),
                dcc.Store(id="page-state", data=0),
                dcc.Store(id="logout-state", data=0),
                dcc.Store(id="user-receitas", data=""),
                dcc.Store(id="user-despesas", data=""),
                dcc.Store(id="user-bancos", data=""),
                dcc.Store(id="trigger-reload-data", data=0),
                dcc.Store(id="load-user-data", data=0),
                dcc.Store(id="table-div-data", data=""),
                dcc.Store(id="row-data", data=""),
                dcc.Store(id="trigger-reload-datatable", data=0),
                

                dbc.Container(id="layout", fluid=True)
            ], fluid= True, class_name="dbc")



# ===================== Callbacks =========================
@login_manager.user_loader
def load_user(user):
    user = loga_usuario_banco_de_dados(user)
    usuario = User(user[0],user[1])
    return usuario
    

@app.callback(
        Output("url", "pathname"),

        Input("login-state", "data"),
        Input("register-state", "data"),
        Input("page-state", "data"),
        Input("logout-state", "data"),
)
def route_user(login, register, page, logout):

    trigger = dash.callback_context.triggered_id

    if trigger:
        if trigger == "login-state" and login == 1:
            return "/dashboard"
        
        elif trigger == "login-state" and login == 4:
            raise PreventUpdate
        
        elif trigger == "login-state" or trigger == "logout-state":
            return "/login"
        
        elif trigger == "page-state" and page == 1:
            return "/dashboard"
        
        elif trigger == "page-state":
            return "/lancamento"

        elif trigger == "register-state" and register == 1:
            return "/login"
        else:
            return "/register"
        
    else:
        return "/"


@app.callback(
    Output("layout", "children"),

    Input("url", "pathname"),

    State("login-state", "data"),
    State("register-state", "data"),
)
def update_layout(pathname, login_message, register_message):
    if pathname == "/" or pathname == "/login":
        if current_user.is_authenticated:
            return dashboard.render_dashboard(current_user.username) 
        return login.render_login(login_message)
    
    elif pathname == "/register":

        if current_user.is_authenticated:
            return dashboard.render_dashboard(current_user.username) 
        
        return register.render_register(register_message)

    elif pathname == "/dashboard":
        if current_user.is_authenticated:
            return dashboard.render_dashboard(current_user.username)
        return login.render_login(login_message)
        
    elif pathname == "/lancamento":
        if current_user.is_authenticated:
            return lancamento.render_lancamento(current_user.username)
        return login.render_login(login_message)
    
    else:
        return html.H1("404 - Página não encontrada", style={"textAlign": "center", "font-style": "italic"})
    

if __name__ == "__main__":
    app.run_server(debug=True)