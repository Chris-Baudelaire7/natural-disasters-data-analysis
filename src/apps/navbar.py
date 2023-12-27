import dash_bootstrap_components as dbc
from dash import html, dcc
from dash_iconify import DashIconify
import dash_mantine_components as dmc


navbar = html.Div(className="header container-fluid", children=[

    html.Div(className="d-flex flex-column flex-md-row align-items-center justify-content-center justify-content-md-between", children=[
        
        
        html.Div(className="d-flex flex-column flex-md-row align-items-center", children=[
            html.Div(className="d-flex align-items-center justify-content-center", children=[
                html.Div(className="title", children=[
                    html.Span("Analytics"),
                    html.Span("Paper", className="text-danger")
                ]),
                
                html.Div(children=[html.Div(className="thin-dash d-none d-md-block")]),
                
            ]),

            html.Div(className="small-title-text text-center text-md-start", children=[
                html.Span("Natural disaster in all over the world",
                          className="title-header"),
                html.Br(),
                html.Span("Statistical Analysis and Data Visualization",
                          className="subtitle-header text-center text-md-start")
            ])
        ]),
        

        html.Div(className="mt-4 mt-lg-0", children=[
            dbc.Nav(className="ms-auto d-flex flex-row align-items-center justify-content-center", navbar=True, children=[
                
                dmc.Tooltip(
                    label="Dashboard",
                    position="bottom",
                    withArrow=True,
                    arrowSize=6,
                    color="black",
                    transition="scale",
                    transitionDuration=300,
                    ff="serif",
                    className="button_class me-3 button",
                    children=[
                        dbc.Button(
                            id="open-offcanvas",
                            className="button_class", 
                            n_clicks=0,
                            children=[
                                DashIconify(icon="ion:menu", width=20), " Navigation sidebar"
                        ])
                    ]
                )
                
            ])
        ])        
        
    ])
])
