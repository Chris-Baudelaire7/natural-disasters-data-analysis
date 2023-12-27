import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

from components import *
from apps.header_page.header2 import *
from callbacks.climate_change_and_disasters_callback.graph import *


dash.register_page(__name__, path="/Non-Climate-Related-Natural-Disasters", order=3,
                   name="Non-Climate-Related Natural Disasters")

layout = html.Div(className="row g-0", children=[


    html.Div(className="col-lg-5 left_content", children=[

        html.H4("In progress...", className="mt-5 pt-5")

    ]),


    html.Div(className="col-lg-7 right_content", id="content-disaster-world", children=[
        
        html.Div(className="text-center", children=[
            html.H4("Non-Climate-Related Natural Disasters", className="mt-4 fw-bold"),
            html.Span("Namely, Geophysical Natural Disasters", className="text-center subtitle fw-bold text-dark"),
        ]),
        
        html.H4("In progress...", className="mt-5 pt-5 text-center")


    ])

])
