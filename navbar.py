from app import *

def define_navbar(usuario):
    layout_nav_bar = dbc.Row([
        dbc.Navbar([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dbc.NavbarBrand("Get Organized", href="/dashboard", class_name="nav-brand"),
                        html.H5(f"Olá, {usuario}!", className="nav-brand", style={"color": "black", "font-style":"bold"})
                    ], sm=12, md=3, align="center"),
                    dbc.Col([
                        dbc.NavItem(dbc.Button("Dashboard", id="dashboard-button", color="secondary", class_name="nav-button")),
                    ], sm=12, md=3),
                    dbc.Col([
                        dbc.NavItem(dbc.Button("Lançamentos", id="lancamentos-button", color="secondary", class_name="nav-button")),
                    ], sm=12, md=3),
                    dbc.Col([
                        dbc.NavItem(dbc.Button("Logout", id="logout-button", color="secondary", class_name="nav-button")),
                    ], sm=12, md=3),
                ])
            ], sm=12, md=10)
        ], expand=True, fixed=True, dark=True, color="primary",class_name="navbar")
    ], justify="center")

    return layout_nav_bar