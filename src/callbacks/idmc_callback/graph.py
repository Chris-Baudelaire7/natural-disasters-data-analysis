import plotly.graph_objs as go
from constants import *
from utils import *
from data_preparation import *


def idps_occurrence():
    liste = ["Disaster Internal Displacements", "Disaster Internal Displacements (Raw)"]
    
    data = idps_data_raw.copy()
    idps_occurrence_data = data.groupby("Year", as_index=False).size()
    
    idps_sum_data = data.groupby(["Year"], as_index=False)[liste].sum(); 
    fig = px.bar(idps_sum_data, x="Year", y="Disaster Internal Displacements", text="Disaster Internal Displacements",
                 color="Disaster Internal Displacements", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    fig.update_traces(
        texttemplate="%{y:.2s}",
        textposition="auto",
        textfont=dict(size=8.7, family="Lora")
    )
    
    fig.add_scatter(
        x=idps_occurrence_data["Year"], y=idps_occurrence_data["size"],
        marker_color="#4bbbe3", yaxis="y2",
        mode="lines+markers+text",
        marker=dict(size=12),
        text=idps_occurrence_data["size"],
        textposition="top center",
        textfont=dict(size=12, family="serif"),
        legend="legend2",
        name="Number of Displacement Cases"
    )
    
    fig.add_hline(
        y=idps_sum_data["Disaster Internal Displacements"].mean(),
        line=dict(color="lightgrey", width=3, dash="dot"),
        annotation_position="top left",
        annotation=dict(
            text=f"~{round(idps_sum_data['Disaster Internal Displacements'].mean()/1000000, 2)}Milion / year",
            font=dict(size=14)
        )
    )

    fig.update_layout(
        height=390,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(title="Number of people displaced", showgrid=False),
        yaxis2=dict(visible=False, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=43),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Number of reported internal displacement<br>cases and people displaced in million<b><br />"
                f"<sup style='color:silver'></sup>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.05,
            "y": 0.93,
            "xanchor": "left",
            "yanchor": "top",
        },
        legend2=dict(orientation="h", x=.3, y=.88)
    )
    
    return fig



def idps_season():
    idps_data_raw = pd.read_excel(idps_path)

    idps_data_raw['Date of Event (start)'] = pd.to_datetime(idps_data_raw['Date of Event (start)'])
    idps_data_raw['Month'] = idps_data_raw['Date of Event (start)'].dt.month
    idps_data_raw['Saison'] = idps_data_raw['Month'].map(saison_mapping)

    idps_season = idps_data_raw.groupby('Saison', as_index=False)['Disaster Internal Displacements'].sum()
    idps_season_count = idps_data_raw.groupby('Saison', as_index=False).size()

    fig = px.bar(idps_season, y="Disaster Internal Displacements", x="Saison",
                 color="Disaster Internal Displacements", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    fig.update_traces(
        text=idps_season["Disaster Internal Displacements"],
        texttemplate="%{y:.2s}",
        textposition="auto",
        textfont=dict(size=14, family="serif")
    )

    fig.add_scatter(
        x=idps_season_count["Saison"], y=idps_season_count["size"],
        marker_color="#4bbbe3", yaxis="y2",
        mode="lines+markers+text",
        marker=dict(size=12),
        text=idps_season_count["size"],
        textposition="top center",
        textfont=dict(size=12, family="serif"),
        legend="legend2",
        name="Number of<br>Displacement<br>Cases"
    )


    fig.update_layout(
        height=300,
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        yaxis2=dict(visible=False),
        legend=dict(x=.1, orientation="h"),
        font=dict(family="serif", color="white", size=10),
        legend2=dict(orientation="h", x=.02, y=.88)
    )

    return fig


def weather_related_vs_geophysic():
    data_geo = (idps_data_raw[idps_data_raw["Hazard Category"] == "Geophysical"])
    data_geo = data_geo.groupby("Year", as_index=False)["Disaster Internal Displacements"].sum()

    data_weather = (idps_data_raw[idps_data_raw["Hazard Category"] == "Weather related"])
    data_weather = data_weather.groupby("Year", as_index=False)["Disaster Internal Displacements"].sum()

    fig = go.Figure()

    fig.add_scatter(
        x=data_weather["Year"], y=data_weather["Disaster Internal Displacements"],
        mode="lines+text+markers",
        text=data_weather["Disaster Internal Displacements"],
        texttemplate="%{y:.2s}",
        textposition="top center",
        marker=dict(size=12),
        textfont=dict(size=12, family="serif"),
        name="Climatic Natural Disasters",
        marker_color="rgb(203,24,29)"
    )

    fig.add_scatter(
        x=data_geo["Year"], y=data_geo["Disaster Internal Displacements"],
        mode="lines+text+markers",
        text=data_geo["Disaster Internal Displacements"],
        texttemplate="%{y:.2s}",
        textposition="top center",
        marker=dict(size=12),
        textfont=dict(size=12, family="serif"),
        name="Non-climatic Natural Disasters",
        marker_color="rgb(252,187,161)",
    )

    fig.update_layout(
        height=360,
        template="plotly_dark",
        hovermode="x",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, r=0, t=70, b=43),
        legend=dict(x=0.4, y=.94),
        yaxis=dict(showgrid=False, visible=False),
        xaxis=dict(showgrid=False),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Climatic vs. Non-climatic<br>Natural Disasters</b><br />"
                f"<sup style='color:silver'>Natural disasters leading to internal displacement</sup>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def season_func():
    order = ['January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']

    data1 = idps_data_raw.groupby(["Month"], as_index=False)[["Disaster Internal Displacements"]].sum()
    data2 = idps_data_raw.groupby(["Month"], as_index=False).size()
    
    dframe = pd.merge(data1, data2, on="Month")
    dframe['Month'] = pd.Categorical(dframe['Month'], categories=order, ordered=True)
    dframe = dframe.sort_values(by='Month')

    fig = px.bar(dframe, y="Disaster Internal Displacements", x="Month",
                 color="Disaster Internal Displacements", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    fig.update_traces(
        text=dframe["Disaster Internal Displacements"],
        texttemplate="%{y:.2s}",
        textposition="auto",
        textfont=dict(size=12, family="Lora")
    )
    
    fig.add_scatter(
        x=dframe["Month"], y=dframe["size"],
        marker_color="#4bbbe3", yaxis="y2",
        mode="lines+markers+text",
        text=dframe["size"],
        textposition="top center",
        marker=dict(size=12),
        textfont=dict(size=13, family="serif"),
        legend="legend2",
        name="Number of Displacement Cases"
    )

    fig.update_layout(
        **update_layout_simple,
        height=340,
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(title="Number of people displaced", showgrid=False),
        yaxis2=dict(visible=False, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=30, b=43),
        font=dict(family="serif", color="white", size=10),
        legend2=dict(orientation="h", x=.5, y=.88)
    )

    return fig


def idps_by_natural_hazards():
    data = idps_data_raw.groupby(["Hazard Type"], as_index=False)[
        ["Disaster Internal Displacements"]].sum()
    data = data.sort_values(
        by="Disaster Internal Displacements", ascending=False).iloc[:-3, :]

    fig = px.bar(data, x="Disaster Internal Displacements", y="Hazard Type",
                 color="Disaster Internal Displacements", color_continuous_scale="reds", orientation="h")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(categoryorder='total ascending')

    fig.update_traces(
        text=data["Disaster Internal Displacements"],
        texttemplate="%{x:.2s}",
        textposition="auto",
        textfont=dict(size=12, family="Lora")
    )

    fig.update_layout(
        **update_layout_simple,
        height=340,
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=43),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Internal displacements<br>by natural dsasters</b><br />"
            ),
            "font": {"family": "serif", "size": 17, "color": "white"},
            "x": 0.98,
            "y": 0.9,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig


def country_ranking():
    dl = (idps_data_raw.groupby(["Country / Territory"], as_index=False)[["Disaster Internal Displacements"]].sum()) \
        .sort_values(by="Disaster Internal Displacements", ascending=False).head(20)

    fig = go.Figure(
        go.Bar(
            x=dl["Country / Territory"],
            y=dl["Disaster Internal Displacements"],
            marker=dict(color=px.colors.sequential.Reds_r),
            text=dl["Disaster Internal Displacements"],
            texttemplate="%{y:.2s}",
            textposition="outside",
            textfont=dict(size=14, family="serif")
        )
    )

    fig.update_layout(
        **update_layout_simple,
        height=300,
        showlegend=False,
        yaxis=dict(visible=False, showgrid=False),
        yaxis2=dict(visible=False, showgrid=False),
        xaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Top 20 Internal Displacement<br>by country</b><br />"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.88,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    return fig

