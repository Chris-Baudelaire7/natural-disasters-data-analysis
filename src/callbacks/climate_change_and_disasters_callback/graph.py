import plotly.graph_objs as go 
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from data_preparation import *
from constants import *
from utils import *


hot_color = "rgb(203,24,29)"
cold_color = "rgb(252,187,161)"


def histogram_global_warm():
    chemin_vers_fichier = 'data/graph.txt'
    df_temp_anomaly = pd.read_csv(chemin_vers_fichier, skiprows=4, delim_whitespace=True, names=['Year', 'No_Smoothing', 'Lowess'])
    df_temp_anomaly.dropna(inplace=True)
    df_temp_anomaly["Year"] = df_temp_anomaly["Year"].astype(int)
    
    x1 = df_temp_anomaly["No_Smoothing"].values
    x2 = df_temp_anomaly["Lowess"].values

    hist_data = [x2, x1]
    group_labels = ["Local Regression Smoothing", 'Temperature Anomaly']

    fig = ff.create_distplot(hist_data, group_labels, bin_size=.05, show_rug=False, histnorm="", colors=[cold_color, hot_color])


    fig.update_layout(
        height=380,
        bargap=0.1,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=0),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        font=dict(family="serif", color="white", size=10),
        showlegend=False,
        title={
            "text": (
                f"<b>Frequency of Temperature</b><br />"
                f"<sup style='color:silver'>Distribution</sup>"
                ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
        }
    )
    
    return fig



def Mean_Surface_Air_Temperature_over_Ocean_or_Land_Areas():
    # Mean Surface Air Temperature over Ocean or Land Areas (C)
    land_ocean_data = pd.read_csv(path_land_ocean, skiprows=1)

    fig = make_subplots(specs=[[{"secondary_y": True}]], shared_yaxes=True)
    
    x=land_ocean_data["Year"].tolist()

    fig.add_scatter(
            x=land_ocean_data["Year"], y=land_ocean_data["Land_Annual"],
            mode="lines+markers", marker=dict(size=3),
        marker_color=hot_color, name="land surface"
        )
        
    fig.add_scatter(
        x=land_ocean_data["Year"], y=land_ocean_data["Lowess(5)"],
        line=dict(width=3), name="land surface (lowess)",
        marker_color=hot_color
    )

    fig.add_scatter(
            x=land_ocean_data["Year"], y=land_ocean_data["Ocean_Annual"],
        mode="lines+markers", marker_color=cold_color, name="Ocean surface",
            marker=dict(size=3)
        )
        
    fig.add_scatter(
        x=land_ocean_data["Year"], y=land_ocean_data["Lowess(5).1"],
        line=dict(width=3), marker_color=cold_color, name="land surface (lowess)"
    )
    
    fig.add_shape(go.layout.Shape(type="line", x0=min(x), x1=max(x), y0=0, y1=0, line=dict(color="grey", dash="dash")))

    fig.update_layout(
        height=390,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        font=dict(family="serif", color="white", size=10),
        title={
                "text": (
                        f"<b>Global-scale Surface Air and Ocean<br>Temperature Change Estimates</b><br />"
                        f"<sup style='color:silver'>Time series: 1880 - 2022 </sup>"
                    ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.98,
                    "y": 0.93,
                    "xanchor": "right",
                    "yanchor": "top",
            }
    )
        
    return fig


def distribution_land_ocean():
    land_ocean_data = pd.read_csv(path_land_ocean, skiprows=1)
    
    x1 = land_ocean_data["Land_Annual"].values
    x2 = land_ocean_data["Ocean_Annual"].values

    hist_data = [x1, x2]
    group_labels = ["Ocean Temperature Anomaly", 'Land Temperature Anomaly']

    fig = ff.create_distplot(hist_data, group_labels, bin_size=.05, show_rug=False, histnorm="", colors=[cold_color, hot_color]) # curve_type='normal', 


    fig.update_layout(
        height=390,
        bargap=0.1,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        showlegend=False,
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Frequency of Temperature<br>(Land and Ocean)</b><br />"
                f"<sup style='color:silver'>Distribution</sup>"
                ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
        }
    )
        
    return fig



def season():
    season = pd.read_csv("data/season.csv", skiprows=1)
    season["Year"] = season["Year+Season"].astype(int)
    season = season.groupby("Year", as_index=False)[["Global", "Low_Latitudes"]].mean()
    
    x=season["Year"].tolist()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]], shared_yaxes=True)

    fig.add_scatter(
        x=season["Year"], y=season["Global"],
        mode="lines+markers", name="Globale",
        marker=dict(), secondary_y=False,
        marker_color=hot_color
    )
    
    fig.add_scatter(
        x=season["Year"], y=season["Low_Latitudes"],
        mode="lines+markers", name="Basses latitudes",
        marker=dict(), secondary_y=False,
        marker_color=hot_color,
    )
    
    fig.add_scatter(
        x=np.concatenate([list(season["Year"]), list(season["Year"])[::-1]]),
        y=np.concatenate([list(season["Low_Latitudes"]), list(season["Global"])[::-1]]),
        fill='tozeroy', 
        mode='none', name="surface",
        fillcolor='grey', 
    )
    
    fig.add_shape(go.layout.Shape(type="line", x0=min(x), x1=max(x), y0=0, y1=0, line=dict(color="grey", dash="dash")))

    fig.update_layout(
        height=340,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        legend=dict(x=0.03, y=.96, bgcolor="#222"),
        yaxis=dict(showgrid=False, gridcolor="#222"),
        xaxis=dict(showgrid=False, gridcolor="#222"),
        font=dict(family="serif", color="white", size=10),
        title={
                "text": (
                    f"<b>Frequency of Temperature</b><br />"
                    f"<sup style='color:silver'>Distribution: 1880 - 2022</sup>"
                    ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.98,
                    "y": 0.93,
                    "xanchor": "right",
                    "yanchor": "top",
            }
    )
        
    return fig


def seasonal_cycle_charts():
    path = "data/seasonal_cycle.csv"
    dict_month = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    
    fig = go.Figure()
    
    data = pd.read_csv(path, skiprows=1)
    data["Year"] = data["Year"].astype(int)
    data['Month'] = data.groupby('Year').cumcount().add(1).map(dict_month)

    x = data["Month"].tolist()
    fig.add_shape(go.layout.Shape(type="line", x0=x[0], x1="Dec", y0=0, y1=0, line=dict(color="grey", dash="dash")))

        
    for year in range(1880, 2023):
        if year != 2016:
            df = data[data["Year"] == year]
            fig.add_scatter(
                x=df["Month"],
                y=df["Anomaly"],
                mode="lines",
                marker=dict(color="grey"),
                line=dict(width=5), name=year
            )
        
    for year, color in zip([2016, 2023], [cold_color, hot_color]):
        seasonal_cycle_last_year = data[data["Year"] == year]

        fig.add_scatter(
            x=seasonal_cycle_last_year["Month"],
            y=seasonal_cycle_last_year["Anomaly"],
            mode="lines",
            marker=dict(color=color),
            line=dict(width=1.5)
        )

        fig.add_scatter(
            x=[list(seasonal_cycle_last_year["Month"])[-1]],
            y=[list(seasonal_cycle_last_year["Anomaly"])[-1]],
            mode="markers",
            marker=dict(color=color, size=10),
        )
    
    fig.update_layout(
        height=390,
        showlegend=False,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False, title=None),
        xaxis=dict(showgrid=False, title=None),
        font=dict(family="serif", color="white", size=10),
        title={
                "text": (
                    f"<b>Daily Average Temperatures (°C)<br>"
                    f"<sup style='color:silver'>from January 1, 1940</sup>"
                    ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.98,
                    "y": 0.93,
                    "xanchor": "right",
                    "yanchor": "top",
            }
    )
    
    return fig



def hhh():
    data = temp_country_data.groupby(["Entity", "Code"], as_index=False)["Surface temperature anomaly"].max()

    fig = go.Figure(
            go.Choropleth(
                z=data["Surface temperature anomaly"],
                locations=data["Code"],
                colorscale="reds",
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
        font=dict(family="serif", color="white", size=10),
            geo=dict(
                showframe=False,
                bgcolor="rgba(0,0,0,0)",
                showcoastlines=False,
                showlakes=False,
                resolution=50,
                projection = dict(type = 'natural earth'),
                lataxis={"range": [-50, 68]},
                lonaxis={"range": [-130, 150]},
                showcountries=True,
            )
        )
    
    return fig


def natural_disaster_and_global_warm_evolution():
    df_disaster = df.groupby("Year").size().reset_index().rename(columns={0: "natural disaster"})
    df_disaster = df_disaster[(df_disaster["Year"] <= 2022)]

    df_global_warm = df_temp_anomaly.copy()
    df_global_warm = df_global_warm[(df_global_warm["Year"] >= 1900) & (df_global_warm["Year"] <= 2022)]
    df_global_warm = df_global_warm.rename(columns={"No_Smoothing": "temperature anomaly"})

    data = pd.merge(df_global_warm, df_disaster, on='Year')
    
    x = data.Year.tolist()
    y_temperature_anomaly = data["temperature anomaly"].tolist()
    y_natural_disaster = data["natural disaster"].tolist()
    
    fig = make_subplots(specs=[[{"secondary_y": True}]], shared_yaxes=True)

    fig.add_scatter(
        x=x, y=y_natural_disaster,
        mode="lines", name="Natural Disasters",
        marker=dict(), secondary_y=True,
        marker_color=cold_color
    )
    
    fig.add_scatter(
        x=x, y=y_temperature_anomaly,
        mode="lines", name="Temperature Anomaly",
        marker=dict(), secondary_y=False,
        marker_color=hot_color
    )
    
    fig.add_shape(go.layout.Shape(type="line", x0=min(x), x1=max(x), y0=0, y1=0, line=dict(color="grey", dash="dash")))

    fig.update_layout(
        height=390,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False, title="Global Temperature"),
        yaxis2=dict(showgrid=False, title="Incidence of Natural Disasters"),
        xaxis=dict(showgrid=False, domain=[.03, .97]),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Evolution of Temperature and<br>Natural Disasters</b><br />"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        }
    )
        
    return fig



def lingress():
    df_disaster = df.groupby("Year").size().reset_index().rename(columns={0: "natural disaster"})
    df_disaster = df_disaster[(df_disaster["Year"] <= 2022)]

    df_global_warm = df_temp_anomaly.copy()
    df_global_warm = df_global_warm[(df_global_warm["Year"] >= 1900) & (df_global_warm["Year"] <= 2022)]
    df_global_warm = df_global_warm.rename(columns={"No_Smoothing": "temperature anomaly"})

    data = pd.merge(df_global_warm, df_disaster, on='Year')
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=data["temperature anomaly"], y=data["natural disaster"],
                             marker_color=cold_color, mode='markers', name="Data Points"))

    z = np.polyfit(data["temperature anomaly"], data["natural disaster"], 1)
    p = np.poly1d(z)
    fig.add_trace(
        go.Scatter(
            x=data["temperature anomaly"], 
            y=p(data["temperature anomaly"]), 
            mode='lines', 
            name="Regression Line",
            line=dict(color=hot_color)
        )
    )

    fig.update_layout(
        height=390,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Correlation Between Temperature<br>Anomaly and Natural Disasters</b><br />"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
        
    return fig



def seasonal_year():
    ff = pd.read_csv("data/HadCRUT.5.0.1.0.analysis.summary_series.global.monthly.csv")
    ff["Year"] = ff["Time"].apply(lambda x: int(x.split("-")[0]))
    ff['Time'] = pd.to_datetime(ff['Time'], format='%Y-%m')
    ff['Month'] = ff['Time'].dt.month_name()
    ff = ff.copy()[["Year", "Month", "Anomaly (deg C)", "Lower confidence limit (2.5%)", "Upper confidence limit (97.5%)"]]
    seasonal_year = (ff.pivot_table(index="Month", columns="Year", values="Anomaly (deg C)"))
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    seasonal_year = seasonal_year.reindex(months)

    fig = go.Figure(data=go.Heatmap(
        z=seasonal_year,
        y=seasonal_year.index,
        x=seasonal_year.columns,
        colorscale='rdbu_r',
        showscale=False
    ))

    fig.update_layout(
        height=340,
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, t=100, r=0, b=43),
        xaxis=dict(title=None),
        yaxis=dict(title=None),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Evolution of Seasonal<br>Temperature Cycles</b><br />"
                f"<sup style='color:silver'>Time Series: 1850 - 2023</sup>"
                ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
                "y": 0.93,
                "xanchor": "right",
                "yanchor": "top",
        }
    )
        
    return fig




def clim_vs_no_clim():
    df_geo = df[df["Disaster Subgroup"] == "Geophysical"]
    df_geo = df_geo.groupby("Year", as_index=False).size()
    df_clim = df[df["Disaster Subgroup"] != "Geophysical"]
    df_clim = df_clim.groupby("Year", as_index=False).size()
    
    fig = go.Figure()
    
    fig.add_scatter(
        x=df_clim["Year"], y=df_clim["size"],
        name="Climatic Natural Disasters",
        marker_color=hot_color
    )
    
    fig.add_scatter(
        x=df_geo["Year"], y=df_geo["size"],
        name="Non-climatic Natural Disasters",
        marker_color=cold_color
    )
    
    fig.update_layout(
        height=390,
        template="plotly_dark",
        hovermode="x",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        legend=dict(x=0.03, y=.96),
        yaxis=dict(showgrid=False),
        xaxis=dict(showgrid=False),
        font=dict(family="serif", color="white", size=10),
        title={
                "text": (
                    f"<b>Climatic vs. Non-climatic<br>Natural Disasters</b><br />"
                    ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.98,
                    "y": 0.93,
                    "xanchor": "right",
                    "yanchor": "top",
            }
    )
        
    return fig


def clim_vs_non_clim_rate():
    non_clim = len(df[df["Disaster Subgroup"] == "Geophysical"])
    clim = len(df[df["Disaster Subgroup"] != "Geophysical"])

    fig = go.Figure(go.Pie(
        labels=["Climatic natural<br>disasters", "Geophysic natural<br>disasters"], values=[clim, non_clim],
        textposition="outside", textinfo="label+percent",
        textfont=dict(size=11, family="Lato"),
        marker=dict(colors=[hot_color, cold_color]),
        insidetextorientation='radial',
        pull=[.2]+[0] * 10,  # hole=.5
    ))

    fig.update_layout(
        height=390,
        template="plotly_dark",
        #legend=dict(orientation="h"),
        showlegend=False,
        margin=dict(autoexpand=True, l=0, r=0, t=0),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Rate of Climatic vs. Non-Climatic<br>Natural Disasters</b>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.93,
            "y": 0.86,
            "xanchor": "right",
            "yanchor": "top",
        }
    )

    return fig
