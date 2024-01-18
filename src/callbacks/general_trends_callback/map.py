import plotly.graph_objs as go
import numpy as np
from data_preparation import *
from constants import *
from utils import *
from dash import Input, Output, callback, html


def mapbox():
    fig = go.Figure(
        go.Scattermapbox(
            lat=df.Latitude,
            lon=df.Longitude,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=5,
                color='rgb(225, 18, 18)',
            ),
            #hoverinfo='none'
        )
    )
    
    fig.update_traces(cluster=dict(enabled=True))


    fig.update_layout(
        autosize=True,
        height=400,
        hovermode='closest',
        margin=dict(autoexpand=True, l=0, r=0, b=0, t=0),
        mapbox=dict(
            accesstoken="pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbHB6dWYxb2wxOWdmMnJvOGtzaDVyb3Y2In0.pXQ81pAk9gRoUHXDnNsjJg",
            style="dark",
        ),
    )

    return fig



def scatter_mapbox_choropleth(): 

    # columns = ["Total Deaths", "No Injured", "Total Affected", "Total Damages ('000 US$)", "No Homeless"]
    
    # l = df.groupby(["Country"])["Country"].count().to_frame()
    
    # l = l.rename(
    #     {key: value for key, value in zip(
    #         wrong_countries_name, right_countries_name)}
    # )
    
    # l = l.rename(columns={"Country": "Occurence"}).reset_index()
    
    # a = set(state_id_map.keys())
    # b = set(l["Country"])
    # state = list(a.intersection(b))
    
    # l = l[l["Country"].isin(state)]
    
    # data = df.groupby(["Country"])[columns].sum()
    # data = data.rename(
    #     {key: value for key, value in zip(
    #         wrong_countries_name, right_countries_name)}
    # )
    
    # data = data.reset_index()
    
    # a = set(state_id_map.keys())
    # b = set(data["Country"])
    # states = list(a.intersection(b))
    
    #data = data[data["Country"].isin(states)]
    
    #data["id"] = data["Country"].apply(lambda x: state_id_map[x])
    #data["events"] = l["Occurence"].values

    
    dfr = df.copy().dropna(subset=['Total Deaths', 'Total Affected'])
    
    dfr["Latitude"] = pd.to_numeric(dfr["Latitude"], errors="coerce")
    dfr["Longitude"] = pd.to_numeric(dfr["Longitude"], errors="coerce")
    dfr["Total Deaths"] = pd.to_numeric(dfr["Total Deaths"], errors="coerce")
    dfr["Total Affected"] = pd.to_numeric(dfr["Total Affected"], errors="coerce")
    
    fig = px.scatter_mapbox(dfr, lat="Latitude", lon="Longitude", color="Disaster Type", 
                            template="plotly_dark", zoom=1.3)
    
    fig.update_traces(cluster=dict(enabled=True))
    
    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        height=400,
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),
        legend=dict(title=None, x=.01, y=.2, bgcolor="rgba(0,0,0,0)", font=dict(family="serif")),
        mapbox=dict(
            accesstoken="pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbHB6dWYxb2wxOWdmMnJvOGtzaDVyb3Y2In0.pXQ81pAk9gRoUHXDnNsjJg",
            style="dark"
        ),
        title={
            "text": (
                f"<b>All Natural Disasters occured since 1900 to 2023</b><br />"
                "<b>Data source:</b> <a style='color:silver' href='https://www.emdat.be'>EM-DAT</a>"
                "<span style='font-size:11px; font-weight:bold'>Author:</span> <span style='color:silver; font-size:11px'>Chris Baudelaire .K</span>"
            ),
            "font": {"family": "serif", "size": 13, "color": "white"},
            "x":0.5, "y": 0.97,
            "xref": "paper",
            "xanchor": "center",
            "yanchor": "top",
        },
        font=dict(family="serif")
    )

    return fig
