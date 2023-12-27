import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from data_preparation import *


filter1 = dbc.Toast(
    id="positioned-toast",
    className="toastmap",
    header="Filter Option",
    is_open=False,
    dismissable=True,
    style={"position": "absolute"},
    children=[
        
        html.Div(children=[
            html.Span("Geographical area", className=""),
            dcc.Dropdown(
                id="filter-geo",
                options=[{"label": "World", "value": "World"}] +

                [{"label": "By continent---------------------------", "disabled": True, "value": "World"}] +

                [{"label": html.Span([x], style={'color': 'rgb(252,187,161)'}), "value": x, }
                 for x in sorted(list_continent)] +

                [{"label": "By region------------------------------", "disabled": True, "value": "World"}] +

                [{"label": html.Span([y], style={'color': 'rgb(254,224,210'}), "value": y}
                 for y in sorted(list_region)],
                
                value="World",
                placeholder="Selection",
                searchable=True,
                clearable=True,
                style={"color": "white"}
            )
        ]),

        html.Div(className="mt-3", children=[
            html.Span("Metric"),
            dcc.Dropdown(
                id="metric",
                options=[
                    {"label": x, "value": y}
                    for x, y in zip(["All Events Occurred", "People Injured", "People Deaths", "Total People Affected", "Economic Damages", "People Left Homeless"], ["size", "No Injured", "Total Deaths", "Total Affected", "Total Damages ('000 US$)", "No Homeless"])
                ],
                value="size",
                placeholder="Selection",
            )
        ]),


        html.Div(className="mt-3", children=[
            html.Span("Categoriy", className="d-block"),
            dcc.Dropdown(
                id="dropdown-category",
                options=[
                    {"label": x, "value": y}
                    for x, y in zip(["By group", "By type"], ["Disaster Subgroup", "Disaster Type"])
                ],
                value="Disaster Type",
            ),
        ]),
        
        
        html.Div(className="mt-3", children=[
            html.Span(id="title-dropdown", className="d-block"),
            dcc.Dropdown(id="choice-dropdown"),
        ]),
        
        
        html.Div(className="mt-3", children=[
            html.Div(className="text-enter", children=[
                html.P("Date range",
                       className="mb-4"),
            ]),

            dmc.RangeSlider(
                id="date-range-slider",
                min=list(df.Year.unique())[0],
                max=list(df.Year.unique())[-1],
                value=[1970, 2023],
                step=1, size=1.5, color="red",
                marks=[
                    {"value": 1900, "label": "1900"},
                    {"value": 2023, "label": "2023"},
                ],
                labelAlwaysOn=True,
                labelTransition="fade",
                style={
                    "font-family": "serif",
                    "color": "white !importtant",
                }
            ),

        ]),
        
    ]
)


list_group = dbc.ListGroup(
    [
        dbc.ListGroupItem(children=[
                html.A(className="text-decoration-none", href="/", children=[
                    html.H5("Global Trend Of Natural Disasters", className="mb-1"),
                    html.P("Global Trend of Natural Disasters: Analyzing Evolutions and Impacts Worldwide", className="text-muted"),
                ])
            ]
        ),
        
        dbc.ListGroupItem(children=[
            html.A(className="text-decoration-none", href="/climate-change-and-natural-disaster", children=[
                    html.H5("Climate Change And Natural Disasters", className="mb-1"),
                    html.P("How does climate change accentuate natural disasters?", className="text-muted"),
                ])
            ]
        ),
        
        dbc.ListGroupItem(children=[
            html.A(className="text-decoration-none", href="/Non-Climate-Related-Natural-Disasters", children=[
                    html.H5("Non-Climate-Related Natural Disasters", className="mb-1"),
                    html.P("Namely, Geophysical Natural Disasters", className="text-muted"),
                ])
            ]
        ),
        
        dbc.ListGroupItem(children=[
            html.A(className="text-decoration-none", href="/Internal-displacement-due-to-natural-disasters", children=[
                    html.H5("Internal Displacement Due To Natural Disasters", className="mb-1"),
                    html.P("Internal Displacement: A Consequence of Natural Disasters", className="text-muted"),
                ])
            ]
        )
    ]
)



offcanvas = html.Div(
    [
        dbc.Offcanvas(
            id="offcanvas",
            scrollable=True,
            placement="end",
            title="Navigation SideBar",
            backdrop=False,
            is_open=False,
            
            children=[
                html.Div(children=[
                    dcc.Markdown(
                        "Dive into the data, uncover trends, and comprehend the significant impact of these events on populations, the global economy, and worldwide population displacements. Welcome to a visual exploration of nature's forces and their humanitarian consequences. Join us on a captivating journey where each point on the map tells a story, each graph reveals a pattern, and each piece of data opens a window into resilience in the face of the unpredictable", className="about"
                    )
                ]),
                
                html.Hr(),
                
                html.Div(className="mt-3", children=[
                    list_group
                ])
            ]
        ),
    ]
)

button_filter = dmc.Affix(
    dbc.Button(
        "filter option",
        id="positioned-toast-toggle",
        color="danger",
        n_clicks=1,
        className="btn-light btn-sm button px-3"
    ),
    position={"bottom": 110, "right": 20}
)


def hovercard_country(hovercardTarget, hovercardDropdown):
    hovercard = dmc.HoverCard(
        className="HoverCard_map",
        position="bottom",
        returnFocus=True,
        closeDelay=100,
        transition="rotate-right",
        withinPortal=True,
        withArrow=False,
        shadow="xl",
        zIndex=9999999999,
        children=[
            dmc.HoverCardTarget(hovercardTarget),
            dmc.HoverCardDropdown(
                hovercardDropdown, unstyled=True, className="crossfilter-style")
        ])

    return hovercard