import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import dcc, html

from components import *
from apps.header_page.header2 import *
from callbacks.idmc_callback.graph import *
from callbacks.idmc_callback.map import *



dash.register_page(__name__, path="/Internal-displacement-due-to-natural-disasters", order=4,
                   name="Internal displacement due to natural disasters")

layout = html.Div(className="row g-0 idmc", children=[


    html.Div(className="col-xl-5 left_content", children=[        
        
        html.Div(className="row mt-2 mt-xl-0", children=[

            html.Div(className="col-12 col-lg-6 col-xl-12", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=map_idps_events()), color="firebrick", type="cube"),
            ]),

            html.Div(className="col-12 col-lg-6 col-xl-12 mt-5 mt-lg-0", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=map_idps_km()), color="firebrick", type="cube"),
            ])
        ])

    ]),


    html.Div(className="col-xl-7 right_content p-1 p-md-3 p-lg-5 p-xl-4", id="content-disaster-world", children=[
        
        html.Div(className="text-center", children=[
            html.H4("Internal Displacement Due To Natural Disasters", className="mt-4 fw-bold"),
            html.Span("Internal Displacement: A Consequence of Natural Disasters",className="text-center subtitle fw-bold text-dark"),
        ]),
        
        html.Div(className="mt-3", children=[

            dcc.Markdown(className="Introduction", children=[
                """
                            Weather-related hazards and the adverse effects of climate change are causing displacement in all regions of the globe. Each year, millions of people are displaced in the context of disasters caused by environmental hazards such as floods, volcanic eruptions, tropical storms, earthquakes, landslides, droughts, and flooding, with most of this disaster displacement taking place within countries. In 2020 alone there were an estimated 30.7 million new internal displacements associated with disasters, the vast majority of them linked to weather and climate-related hazards
                        """
            ]),

        ]),
        
        
        
        html.Div(className="row align-items-center mt-5", children=[
            
            html.Div(className="col-lg-4", children=[
                dcc.Markdown(className="Introduction mt-4", children=[
                    """
                    The number of internally displaced people continues to rise. Natural disasters displaced more than 25 million people within their country each year.

                    In 2022, the number of people in internal displacement has reached a record high of 71.1 million individuals across 110 countries and territories, of which 32.6 million displacements have been associated with disasters, according to the Internal Displacement Monitoring Centre (IDMC).
                    
                    Since 2008 until 2022, more than 13k disaster events have been reported, resulting in over 376 million internal displacements
                """
                ])
            ]),

            html.Div(className="col-lg-8", children=[
                dcc.Loading(dcc.Graph(
                    id="idps-season", config=dict(displayModeBar=False), figure=idps_occurrence())),
            ])
        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[
            
            html.Div(className="col-lg-8", children=[
                dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=weather_related_vs_geophysic())),
            ]),

            html.Div(className="col-lg-4", children=[
                dcc.Markdown(className="Introduction mt-4", children=[
                    """
                    As we compared in the **[Climate Change and Natural Disasters](/climate-change-and-natural-disaster)** section, over 86% of natural disasters are climate-related disasters.
                    
                    The primary cause of nature-based displacement were floods and extreme storms, events that have gotten worse in recent years due to climate change. As temperatures warm and sea levels rise, these figures will only rise, putting tremendous pressure on countries to curb greenhouse gas emissions and take climate action
                """
                ])
            ])

        ]),


        html.Div(className="row align-items-center mt-5", children=[
            
            html.H4("From a seasonal perspective"),
            
            html.Div(className="col-lg-8", children=[
                dcc.Loading(dcc.Graph(
                    id="idps-season", config=dict(displayModeBar=False), figure=season_func()))
            ]),
            
            html.Div(className="col-lg-4", children=[
                dcc.Loading(dcc.Graph(
                    id="idps-season", config=dict(displayModeBar=False), figure=idps_season()))
            ]),
            
            # html.Div(className="col-12 mt-3", children=[
            #     dcc.Markdown(children=[
            #         """
            #         According to the Intergovernmental Panel on Climate Change, “Extreme weather events provide the most direct pathway from climate change to migration"
            #     """
            #     ])
            # ]),

        ]),
        
        
        html.Div(className="row align-items-center mt-5", children=[
            html.H4("High Level Trends"),
            
            html.Div(className="col-12 mt-3", children=[
                dcc.Markdown(children=[
                    """
                    Countries on all continents were affected by the increase in natural disasters, including many smaller nations in which disasters displaced a large proportion of the population. However, Asia is by far the worst hit region, and countries in south and south-east Asia, including India, the Philippines, Bangladesh and Indonesia as well as China and Pakistan, had among the largest numbers displaced.
                    
                    Seven out of the ten countries with the highest risk of internal displacement by disasters and climate change are in southern and south-eastern Asia.

                    This year, floods killed over 1,200 people on the continent. Millions have fled their homes in India, Nepal and Bangladesh. As global temperatures rise, floods in these countries are likely to displace millions of people in the coming years.

                    India, regularly burdened with severe flooding, is especially at risk. According to the report, over 2.3 million people are already losing their homes to disasters every year.
                """
                ])
            ]),
            
            html.Div(className="col-lg-5", children=[
                dcc.Loading(dcc.Graph(
                    id="idps-season", config=dict(displayModeBar=False), figure=idps_by_natural_hazards()))
            ]),

            html.Div(className="col-lg-7", children=[
                dcc.Loading(dcc.Graph(
                    id="idps-season", config=dict(displayModeBar=False), figure=country_ranking()))
            ]),

        ]),




    ])

])
