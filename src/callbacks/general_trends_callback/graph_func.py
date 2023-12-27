import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from data_preparation import *
from constants import *
from utils import *


def disaster_deaths_rate():
    data = pd.read_csv("data/share-deaths-from-natural-disasters.csv")

    data = data[data.Entity == "World"]

    fig = go.Figure(
        go.Scatter(
            x=data["Year"], y=data[
                "Deaths - Exposure to forces of nature - Sex: Both - Age: All Ages (Percent)"],
            mode="lines+markers",
            marker=dict(color="firebrick")
        )
    )

    fig.update_layout(
        height=350,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        hovermode="x",
        margin=dict(autoexpand=True, l=0, r=0, t=80, b=43),
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(ticksuffix="%", title=None, showgrid=False),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Share of Deaths Due to Natural Disasters<br>in the Total Death Rate in the World</b><br />"
                f"<sup style='color:silver'>Time Series: 1990 - 2020"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    legend(fig, 1, -.15)

    return fig


def death_func():

    l_r = []
    l = ['Drought', 'Earthquake', 'Flood', 'Storm', 'Volcanic activity',
         'Landslide', 'Wildfire', 'Extreme temperature ']
    for i in l[::-1]:
        l_r.append(i)

    data_deaths_evolution = df.groupby("Year")["Total Deaths"].sum().reset_index()

    r = df.groupby(["Year", "Disaster Type"])["Total Deaths"].sum().reset_index()
    r = r[r["Disaster Type"].isin(["Drought", "Flood", "Earthquake", "Storm",
                                  "Volcanic activity",  "Extreme temperature ", "Landslide", "Wildfire"])]
    r = r.set_index("Disaster Type")

    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = px.scatter(r, x="Year", y=r.index, size="Total Deaths", color=r.index, size_max=55)
    fig2 = px.bar(data_deaths_evolution, x="Year", y="Total Deaths", color="Total Deaths",
                  color_continuous_scale=px.colors.sequential.RdBu_r)
    
    fig2.update_traces(yaxis="y2")

    subfig.add_traces(fig2.data+fig.data)
    subfig.update_coloraxes(showscale=False)
    subfig.update_traces(marker=dict(opacity=1))

    subfig.update_yaxes(categoryorder='array', categoryarray=l_r)

    subfig.update_layout(
        height=396,
        template="simple_white",
        showlegend=False,
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showline=False, nticks=20),
        yaxis=dict(showline=False),
        yaxis2=dict(showline=False),
        font=dict(family="serif", color="white", size=10)
    )
    
    legend(fig, 1, -.15)

    return subfig




def heatmap_season():
    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z = data_period_count["count"],
            y = data_period_count["Month"],
            x = data_period_count["Year"],
            colorscale = "inferno",
            showscale=False
        ), 
    )
    
    list_months = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]
    
    # fig.update_yaxes(categoryorder='array', categoryarray=list_months)

    fig.update_layout(
        update_layout_simple,
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=45),
        height=350,
        xaxis=dict(
            showgrid=False,
            showticklabels=True,
            ticks="outside",
            tickfont=dict(
                color="white",
            )
        ),
        
        yaxis=dict(
            showticklabels=True,
            ticks="inside",
            ticklen=5,
            tickcolor="white"
        ),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Monthly Trend of Natural Disasters</b><br />"
                f"<sup style='color:silver'>All natural disasters occurred: 1970 - 2023"
                ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    legend(fig, 1, -.15)
    
    return fig




def month_events():
    data_period_count = df.groupby(["Year", "Start Month"], as_index=False).size()
    data_period_count['Month'] = data_period_count['Start Month'].apply(lambda x: pd.to_datetime(x, format='%m').month_name())
    month_data = data_period_count_pivot.sum().to_frame().rename(columns={0: "value"}).reset_index()
    
    order = ["Winter", "Spring", "Summer", "Autumn"]

    month_data["saison"] = month_data["Month"].apply(get_season)
    month_data = month_data.sort_values(by="saison", key=lambda col: col.map({v: k for k, v in enumerate(order)}))
    months = month_data
    month_data = month_data.set_index(["saison", "Month"])

    xlabels = [list(month_data.index.get_level_values(0)),
                list(month_data.index.get_level_values(1)),
                month_data.index]

    color_map = {
        "Winter": "#fefefe",
        "Spring": "royalblue",
        "Summer": "orangered",
        "Autumn": "yellow"
    }

    sub_type_colors = [color_map[type] for type in months["saison"]]
    
    fig = go.Figure(
            go.Bar(
                y=xlabels,
                x=month_data["value"],
                marker=dict(color=sub_type_colors),
                orientation="h",
                text=month_data["value"],
                textposition='auto',
            )
        )
    fig.update_layout(
        height=350,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=45),
        yaxis=dict(
                showline=True,
                linecolor="whitesmoke",
                linewidth=.2,
                ticks="outside",
                ticklen=8,
                tickcolor="white",
            ),
        xaxis=dict(visible=False),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Distribution by Month and Season</b><br />"
                f"<sup style='color:silver'>Occurrence of natural disasters by month and season"
                ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    legend(fig, 1, -.15)
    
    return fig