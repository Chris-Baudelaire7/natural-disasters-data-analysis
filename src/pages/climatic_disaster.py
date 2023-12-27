import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

from components import *
from apps.header_page.header2 import *
from callbacks.climate_change_and_disasters_callback.map import *
from callbacks.climate_change_and_disasters_callback.graph import *
from .text import text


dash.register_page(__name__, path="/climate-change-and-natural-disaster", order=2, 
                   name="climate change and natural disaster")

layout = html.Div(className="row g-0 overview", children=[


    html.Div(className="col-xl-5 left_content", children=[
        
        html.Div(className="row mt-2 mt-xl-0", children=[

            html.Div(className="col-12 col-lg-6 col-xl-12", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=temp_anomaly(path_1970, 1970))
            ]),

            html.Div(className="col-12 col-lg-6 col-xl-12 mt-5 mt-lg-0", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=temp_anomaly(path_2023, 2023))
            ]),
        ])

    ]),


    html.Div(className="col-xl-7 right_content p-1 p-md-3 p-lg-5 p-xl-4", id="content-disaster-world", children=[
        
        html.Div(className="text-center", children=[
            html.H4("Climate Change And Natural Disasters", className="mt-4 fw-bold"),
            html.Span("How does climate change accentuate natural disasters ?",className="text-center subtitle fw-bold text-dark"),
        ]),

        html.Div(className="mt-3", children=[

            dcc.Markdown(className="Introduction", children=[
                """
                            Climate change acts as a catalyst, exponentially amplifying extreme weather events. Natural disasters are multiplied due to rising temperatures on land and in the seas. Cyclones, hurricanes, droughts, heatwaves, torrential rains, floods, and storms have experienced significant growth in both number and intensity since the 1980s. This escalation is directly attributed to global warming, according to the unanimous conclusions of climatologists from the Intergovernmental Panel on Climate Change (IPCC).

                            Global climate changes exacerbate extreme weather events, thereby increasing the risk of climate-related disasters. The rise in air and water temperatures leads to a sea level increase, reinforcing the intensity and duration of storms, winds, droughts, and fires, as well as prolonging periods of precipitation and flooding. The facts are staggering:

                            - The number of climate-related disasters has tripled in the last thirty years.
                            - Between 2006 and 2016, the rate of sea level rise was 2.5 times faster than that recorded throughout almost the entire 20th century.
                            - Climate change-related disasters force over 20 million people to relocate each year.

                        """
            ]),

        ]),
        
        
        html.Div(className="row align-items-center mt-5 pt-3", children=[
            
            html.H4("A Brief Overview of Climate Change", className="mb-3"),
            
            html.Div(className="col-12 mt-2", children=[
                dcc.Markdown(
                    """
                    Both globes depict a glaring increase in temperature between 1970 and 2023.
                    
                    November 2023 was the warmest November on record globally, with an average surface air temperature of 14.22°C, 0.85°C above the 1991-2020 average for November and 0.32°C above the temperature of the previous warmest November, in 2020. The global temperature anomaly for November 2023 was on a par with October 2023, and only lower than the September 2023 anomaly of 0.93°C. The month as a whole was about 1.75°C warmer than an estimate of the November average for 1850-1900, the designated pre-industrial reference period.
                    
                    - Copernicus
                    """
                )
            ]),

            html.Div(className="col-md-7", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), id="global-temperature-graph"), color="red"),

                html.Div(className="d-flex justify-content-center", children=[
                    dmc.ChipGroup(value="Bar", id="global-temperature-radio", children=[
                        dmc.Chip(x, value=y, size="sm", color="red")
                        for x, y in zip(["Line chart", "Bar chart",], ["Bar", "Ligne"])
                    ]),
                ]),
            ]),

            html.Div(className="col-md-5", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=histogram_global_warm()), color="red"),
            ]),
            
            html.Div(className="col-12 mt-2", children=[
                dcc.Markdown(
                    """
                    The term temperature anomaly means a departure from a reference value or long-term average. A positive anomaly indicates that the observed temperature was warmer than the reference value, while a negative anomaly indicates that the observed temperature was cooler than the reference value.
                    
                    Except for a leveling off between the 1940s and 1970s, the surface temperature of our planet has
                    increased since 1880. The last decade has sen global temperatures rise to the highest levels ever
                    recorded. This graph illustrates the change in global surface temperature relative to 1951-1980 average
                    temperatures.
                    """
                )
            ])

        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[
                    
            html.Div(className="col-md-7", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=Mean_Surface_Air_Temperature_over_Ocean_or_Land_Areas()),
            ]),
            
            html.Div(className="col-md-5", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=distribution_land_ocean()),
            ]),
            
            html.Div(className="col-12", children=[
                dcc.Markdown(
                    "Global sea surface temperature has increased in a similar trend as the global mean temperature. However, temperatures over land have increased more rapidly than those over the oceans. Water has a high heat capacity, which means that it takes more heat energy to raise water’s temperature than it does to raise most other substances. Hence, water can absorb or release a lot of heat with little temperature change. This means that over time, the temperature of water varies less than land."
                )
            ])
        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[

            html.Div(className="col-md-6", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=seasonal_cycle_charts()),
            ]),

            html.Div(className="col-md-6", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=seasonal_year()),
            ]),
            
            html.Div(className="col-12", children=[
                dcc.Markdown(
                    """
                    The left graph shows the global daily surface air temperature (°C) from January 1, 1940 to September 30, 2023, plotted as a time series for each year. 
                    the daily average global mean surface air temperature surpassed the record set in August 2016, making it the hottest day on record, with 5 July and 7 July shortly behind. The first three weeks of July have been the warmest three-week period on record. Global mean temperature temporarily exceeded the 1.5° Celsius threshold above the preindustrial level during the first and third week of the month (within observational error)
                    """
                )
            ])

        ]),
        
        
        
        html.Div(className="row align-items-center mt-5 pt-3", children=[

            html.H4("Natural Disasters Linked to Climate Change", className="mb-3"),

            html.Div(className="col-md-6", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=natural_disaster_and_global_warm_evolution()),
            ]),

            html.Div(className="col-md-6", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=lingress()),
            ]),
            
            html.Div(className="mt-3", children=[
                dcc.Markdown(className="text", children=[text])
            ])
        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[
            
            html.H4("Comparative Analysis", className="mb-3"),

            html.Div(className="col-md-7", children=[
                dcc.Graph(config=dict(displayModeBar=False),
                          figure=clim_vs_no_clim()),
            ]),
            
            html.Div(className="col-md-5", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=clim_vs_non_clim_rate()),
            ]),

            html.Div(className="col-12", children=[
                dcc.Markdown(
                    "Over 80% of natural disasters are climate-related."
                )
            ])

        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[

            html.H4("Temperature Anomaly: Situation by Country", className="mb-3"),

            html.Div(className="row align-items-center", children=[

                html.Div(className="col", children=[

                    html.Div(className="mt-4", children=[
                        html.Span("Select Multiple Countries",
                                  className="subtitle"),
                        dcc.Dropdown(
                            id="dropdown",
                            options=[
                                {"label": country, "value": country} for country in sorted(list(temp_country_data.Entity.unique()))
                            ],
                            value=l2,
                            placeholder="Select Multiple Countries",
                            multi=True
                        )
                    ]),

                    html.Div(className="my-4", children=[
                        dbc.Tabs(id="tabs", active_tab="heatmap", children=[
                            dbc.Tab(label="Heatmap",
                                    tab_id="heatmap"),
                            
                            dbc.Tab(label="Map", tab_id="map"),
                        ]),
                        html.Div(id="content"),
                    ])

                ])
            ]),

        ])
    ])

])
