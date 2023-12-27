import dash
from flask import Flask
from dash import html, Dash
import dash_bootstrap_components as dbc

from apps import navbar
from callbacks.callback_comp import *
from callbacks.general_trends_callback.callback import *
from callbacks.climate_change_and_disasters_callback.callback import *
from components import *


app_params = {
    "server": Flask(__name__),
    "title": "Natural Disaster Tracker",
    "use_pages": True,
    "update_title": "Wait a moment...",
    "url_base_pathname": "/",
    "external_stylesheets": [dbc.themes.CYBORG, dbc.icons.BOOTSTRAP],
    "suppress_callback_exceptions": True,
    "meta_tags": [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}]
}

server_params = {"debug": False}


app = Dash(__name__, **app_params)

server = app.server

app.layout = html.Div(id="app-root", className="app-root", children=[

    navbar.navbar, offcanvas,

    html.Div(id="pages", className="pages", children=[
        dash.page_container
    ]),

])


if __name__ == '__main__':
    app.run_server(**server_params)