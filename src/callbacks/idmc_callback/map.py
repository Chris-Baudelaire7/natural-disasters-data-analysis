import plotly.graph_objs as go
from constants import *
from utils import *
from data_preparation import *


def map_idps_km():
    idps_country = idps_data_raw.groupby(
        ["ISO3", "Country / Territory"], as_index=False)["Disaster Internal Displacements"].sum()

    fig = go.Figure(
        go.Choropleth(
            z=idps_country["Disaster Internal Displacements"],
            locations=idps_country["ISO3"],
            colorscale="reds",
            showscale=False,
            marker=dict(line=dict(width=.3, color="black")),
            customdata=idps_country
        )
    )

    fig.update_layout(**choroplath_layout(400))
    
    fig.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        y=1,
        xanchor="center",
        showarrow=False,
        text="<b style='font-size: 17px; color:white'>People displaced due to natural disaster</b><br>"
        "<b>Data source:</b> <a style='color:silver' href='https://www.internal-displacement.org/database/displacement-data'>IDMC Data Portal </a> "
        "<b>Author: </b> Chris Baudelaire .K",
        font=dict(size=11, family="serif")
    )

    return fig


def map_idps_events():

    idps_occurrence_data = idps_data_raw.groupby(
        ["ISO3", "Country / Territory"], as_index=False).size()

    fig = go.Figure(
        go.Choropleth(
            z=idps_occurrence_data["size"],
            locations=idps_occurrence_data["ISO3"],
            colorscale="ylorrd",
            showscale=False,
            marker=dict(line=dict(width=.3, color="black")),
            customdata=idps_occurrence_data
        )
    )

    fig.update_layout(**choroplath_layout(400))
    
    fig.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        y=1,
        xanchor="center",
        showarrow=False,
        text="<b style='font-size: 17px; color:white'>Total number of IDPs by natural disasters as of 31 December 2022</b><br>"
        "<b>Data source:</b> <a style='color:silver' href='https://www.internal-displacement.org/database/displacement-data'>IDMC Data Portal </a> "
        "<b>Author: </b> Chris Baudelaire .K",
        font=dict(size=11, family="serif")
    )

    return fig
