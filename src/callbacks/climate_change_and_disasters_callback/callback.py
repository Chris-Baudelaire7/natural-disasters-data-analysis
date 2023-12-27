from dash import html, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from .graph import *
from .map import *
from .tabs import *



@callback(
    Output("global-temperature-graph", "figure"),
    Input("global-temperature-radio", "value")
)
def update_graph(value):
    chemin_vers_fichier = 'data/graph.txt'
    df = pd.read_csv(chemin_vers_fichier, skiprows=4, delim_whitespace=True, names=[
                     'Year', 'No_Smoothing', 'Lowess'])
    df.dropna(inplace=True)
    df["Year"] = df["Year"].astype(int)

    x = df.Year.tolist()
    y_no_smoothing = df["No_Smoothing"].tolist()
    y_lowess = df["Lowess"].tolist()

    fig = go.Figure()

    if value == "Ligne":
        fig.add_scatter(
            x=x, y=y_no_smoothing,
            mode='lines+markers',
            name='Anomalie de temperature',
            line=dict(color='orangered'),
        )
    else:
        color_palette = "reds"
        fig.add_bar(x=x, y=y_no_smoothing, marker=dict(
            color=y_no_smoothing, colorscale=color_palette))

    fig.add_scatter(x=x, y=y_lowess, mode='lines',
                    name='Lowess', line=dict(color='red', width=3))

    fig.add_shape(go.layout.Shape(type="line", x0=min(x), x1=max(
        x), y0=0, y1=0, line=dict(color="grey", dash="dash")))

    fig.update_layout(
        height=390,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="serif", size=11),
        margin=dict(autoexpand=True, l=0, r=0, t=80, b=43),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        title={
            "text": (
                f"<b>Global-scale Surface Air Temperature<br>Change Estimates</b><br />"
                f"<sup style='color:silver'>Land and Oceanic Data: 1880 - 2022</sup>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


@callback(
    Output("heatmap-temperature-by-country", "figure"),
    Input("dropdown", "value"),
)
def heatmap_temperature_by_country(value):
    temp_country_data = pd.read_csv(path)
    temp_country_data = temp_country_data[temp_country_data["Year"] >= 1960]

    temp_country_data = temp_country_data[temp_country_data["Entity"].isin(
        value)]

    data = (temp_country_data.pivot_table(index="Year",
            columns="Entity", values="Surface temperature anomaly"))
    data.fillna(0, inplace=True)
    data = (data.T)

    fig = go.Figure(data=go.Heatmap(
        z=data,
        y=data.index,
        x=data.columns,
        colorscale='rdbu_r', 
        colorbar=dict(title='Temp'),
        text=data,
        texttemplate="%{text}",
        showscale=False
    ))

    fig.update_layout(
        height=300,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="serif", color="white", size=10),
        margin=dict(autoexpand=True, l=0, t=0, r=0, b=0),
    )

    return fig


@callback(
    Output("global-temperature-country", "figure"),
    Input("global-temperature-country-select", "value"),
)
def global_temperature_by_country(year):
    temp_country_data = pd.read_csv(path)
    data = temp_country_data[temp_country_data.Year == year]
    
    fig = go.Figure(
        go.Choropleth(
            z=data["Surface temperature anomaly"],
            locations=data["Code"],
            colorscale="rdbu_r",
            showscale=False,
            marker=dict(line=dict(width=.3, color="black")),
            customdata=data
        )
    )

    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=0, b=0, r=0, t=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        geo=dict(
            showframe=False,
            bgcolor="rgba(0,0,0,0)",
            showcoastlines=False,
            showlakes=False,
            resolution=50,
            projection=dict(type='natural earth'),
            lataxis={"range": [-50, 68]},
            lonaxis={"range": [-130, 150]},
            showcountries=True,
        )
    )

    return fig
