import dash
import dash_mantine_components as dmc
from dash import dcc, html

from components import *
from constants import *
from apps.header_page.header1 import *
from callbacks.general_trends_callback.map import *


dash.register_page(__name__, path="/", order=1, name="Global Trend Of Natural Disasters")

layout = html.Div(className="row g-0 overview", children=[
    
    html.Div(className="col-xl-5 left_content", children=[
                
        html.Div(className="row mt-2 mt-xl-0", children=[
            
            html.Div(className="col-12 col-lg-7 col-xl-12", children=[
                hovercard_country(
                    dcc.Loading(
                        dcc.Graph(id="geo-map", config=dict(displayModeBar=False)), 
                        color="firebrick", type="cube"
                    ),
                    
                    html.Div(className="div_hoverdata", children=[
                        dcc.Graph(id="hoverdata", config=dict(displayModeBar=False)),
                        html.Div(className="mt-1", id="fig_country"),
                    ])
                )
            ]),
            
            html.Div(className="col-12 col-lg-5 col-xl-12 mt-5 mt-lg-0", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=scatter_mapbox_choropleth())
            ])
        ])
    ]),
    
    button_filter, filter1,
    
    
    html.Div(className="col-xl-7 right_content p-1 p-md-3 p-lg-5 p-xl-4", id="content-disaster-world", children=[
                
        html.Div(className="text-center", children=[
            html.H4("Global Trend Of Natural Disasters", className="mt-4 fw-bold"),
            html.Span("Comprehensive Analysis of Natural Disaster Trends",className="text-center subtitle fw-bold text-dark"),
        ]),
        
        html.Div(className="mt-3", children=[
            
            dmc.Spoiler(
                showLabel="Show more",
                hideLabel="Hide",
                maxHeight=55,
                children=[header],
            )
                        
        ]),     
        
        # html.Div(className="row align-items-center mt-5 pt-3", children=[
        #     html.Div(className="stats", children=[
        #         html.Div(className="rounded-circle circle mx-3", children=[
        #             html.H3("15109", className="number"),
        #             html.H6("Events", className="text")
        #         ]),

        #         html.Div(className="rounded-circle circle mx-3", children=[
        #             html.H3("7876763", className="number"),
        #             html.H6("Injured", className="text-warning")
        #         ]),

        #         html.Div(className="rounded-circle circle mx-3", children=[
        #             html.H3("22959336", className="number"),
        #             html.H6("Deaths", className="text-danger")
        #         ]),
                
        #         html.Div(className="rounded-circle circle mx-3", children=[
        #             html.H3("4317081036", className="number"),
        #             html.H6("Damages ($)", className="text-primary")
        #         ])
        #     ])
        # ]),
                
        
        html.Div(className="row align-items-center mt-5 pt-3", children=[

            html.Div(className="col-md-6", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="timeseries-world"), color="red"),

                html.Div(className="d-flex justify-content-center", children=[
                    dmc.ChipGroup(value="bar", id="type-graph", children=[
                        dmc.Chip(x, value=y, size="sm", color="red")
                        for x, y in zip(["Line chart", "Bar chart", "Area chart"], ["line", "bar", "area"])
                    ]),
                ]),
            ]),

            html.Div(className="col-md-6", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="timeseries-category"), color="red"),

                html.Div(className="d-flex justify-content-center", children=[
                    dmc.ChipGroup(value="absolue", id="type-serie", children=[
                        dmc.Chip(x, value=y, size="sm", color="red")
                        for x, y in zip(["Serie absolue", "Serie relative (en %)"], ["absolue", "relative"]
                        )
                    ]),
                ]),
            ]),

        ]),
        
        html.Div(id="div-events"),
        
        
        html.Div(className="row align-items-center mt-3", children=[

            html.Div(className="col-12", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="rate"), color="red")
            ])

        ]),
        
        
        html.Div(id="div-deaths"),
        
        html.Div(className="row align-items-center mt-5", id="share"),
        
        
        html.Div(className="row align-items-center mt-5 pt-3", children=[
            
            html.H4("High Level Trends",className="mb-3"),

            html.Div(className="col-md-4", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="hbar-disaster-group-and-type"), color="red"),
            ]),
            
            html.Div(className="col-md-8", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="ranking-graph"), color="red"),
            ]),
            
            html.Div(className="col-md-8", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="region-country-vbar"), color="red"),
                
                html.Div(className="d-flex justify-content-center", children=[
                    dmc.ChipGroup(value="Region", id="chip-region-country", children=[
                        dmc.Chip(x, value=y, size="sm", color="red")
                        for x, y in zip(["By region", "By country"], ["Region", "Country"]
                        )
                    ]),
                ]),
            ]),
            
            html.Div(className="col-md-4", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="hbar-continent"), color="red"),
            ]),
            
            

        ]),
        
        
        html.Div(className="row align-items-center mt-5 pt-3", children=[

            html.H4("Distribution", className="mb-4"),
            
            html.Div(className="col-12", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="group-repartition"), color="red")
            ]),
            
            # html.Div(className="col-12 col-md-6 col-xl-12 mb-md-0 mb-lg-0 mb-xl-5", children=[
            #     dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="group-repartition"), color="red")
            # ]),

            # html.Div(className="col-12 col-md-6 col-xl-12 mt-5 mt-md-0 mt-lg-0 mt-xl-5", children=[
            #     dcc.Loading(dcc.Graph(config=dict(displayModeBar=False),id="proportion-by-contnent"), color="red"),
            # ])
    

        ])
        
    ])
    
])
