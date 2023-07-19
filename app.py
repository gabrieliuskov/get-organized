import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import html, dcc, Input, Output, State
from dash import dash_table
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os
import flask
import pdb
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import random
from dash.exceptions import PreventUpdate
import numpy as np



# ====================== Style ==================
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"


load_figure_template("united")
server = flask.Flask(__name__)
app = dash.Dash(__name__,server=server ,external_stylesheets=[dbc.themes.UNITED, FONT_AWESOME, dbc_css], title="Get Organized", suppress_callback_exceptions=True, update_title="")
server.config.update(SECRET_KEY=os.urandom(65))

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin):
    def __init__(self, id, username):
        self.id = str(id)
        self.username = username
 





