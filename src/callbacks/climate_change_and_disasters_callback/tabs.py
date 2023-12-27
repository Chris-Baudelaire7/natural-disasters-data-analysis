from dash import html, dcc
from data_preparation import *


heatmap_content_div = html.Div(className="mt-4", children=[
    dcc.Loading(dcc.Graph(id="heatmap-temperature-by-country", config=dict(displayModeBar=False), figure={}))
])

map_content_div = html.Div(className="mt-4", children=[
    html.Div(className="row align-items-center", children=[

        html.Div(className="col", children=[
            dcc.Graph(
                id="global-temperature-country",
                config=dict(displayModeBar=False),
                #figure=hhh()
            ),
            html.Div(className="", children=[
                
                dcc.Slider(
                    id="global-temperature-country-select",
                    min=temp_country_data["Year"].min(),
                    max=temp_country_data["Year"].max(),
                    value=temp_country_data["Year"].max(),
                    step=1,
                    marks=None,
                    tooltip={"placement": "bottom", "always_visible": True}
                ),

            ])
        ])
    ]),
])