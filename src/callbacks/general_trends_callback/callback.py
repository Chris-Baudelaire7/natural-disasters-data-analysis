import json
from dash import Input, Output, callback, html, dcc
from plotly.subplots import make_subplots
from data_preparation import *
from utils import *
from .graph_func import *



@callback(
    Output('hoverdata', 'figure'), 
    Output('fig_country', 'children'), 
    Input("geo-map", 'hoverData'),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
    Input("choice-dropdown", "value"),
)
def display_hover_data(hoverData, metric, category, choice):
    list_casualties = ["Total Deaths", "No Injured", "Total Affected", "Total Damages ('000 US$)", "No Homeless"]
    
    if hoverData: country = hoverData["points"][0]["customdata"][1]
    else: country = "France"
        
    d = df[df["Country"] == country]
    data = data_filter(d, category, choice)

    if metric == "size": 
        data = data.groupby(["Year"], as_index=False).size()
        data2 = d.groupby(category, as_index=False).size()
        x = data["size"].sum()
    else: 
        data = data.groupby(["Year"], as_index=False)[list_casualties].sum()
        data2 = d.groupby(category, as_index=False)[list_casualties].sum()
        x = data[metric].sum()
    
    title_mapping = {
        "size": ("Evolution of the Number of natural<br>disasters occured", "Events occured"),
        "Total Deaths": ("Evolution of the Number of<br>people dead", "People deaths"),
        "No Injured": ("Evolution of the Number of<br>people injured", "People injured"),
        "Total Affected": ("Evolution of the Number of total<br>people affected", "people affected"),
        "Total Damages ('000 US$)": ("Evolution of the Number of<br>economic damages", "Economic damages ($)"),
        "No Homeless": ("Evolution of the Number of people<br>left homeless", "People left homeless")
    }

    title, title2 = title_mapping.get(metric)
        
    fig = px.line(data, x="Year", y=metric)
    
    fig.update_traces(line=dict(width=1.3, color="firebrick"))

    fig.update_layout(
        **update_layout_simple,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False, dtick=15),
        yaxis=dict(title=None, showgrid=False),
        margin=dict(l=0, r=0, b=43, t=0),
        font=dict(family="serif", color="white", size=10),
        height=190,
        width=360,
        title={
            "text": (
                f"{title}: 1900 - 2023"
            ),
            "font": {"family": "serif", "size": 10, "color": "#f3f2f3"},
            "x": 1,
            "y": 0.88,
            "xanchor": "right",
            "yanchor": "top",
        },
    )
    
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.03, y=0.9,
        xanchor="left",
        showarrow=False,
        text=f"{country}<br><span style='font-size: 13px'>{title2}: {int(x):,}</span>",
        font=dict(size=17, family="serif")
    )
    
    
    
    fig2 = px.bar(data2, y=metric, x=category, color=metric, color_continuous_scale="reds", orientation="v")
    fig2.update_coloraxes(showscale=False)
    fig2.update_xaxes(categoryorder='total ascending')

    fig2.update_traces(
        text=data2[metric],
        texttemplate="%{y:.2s}",
        textposition="auto",
        textfont=dict(size=11, family="serif"),
        hoverinfo="skip"
    )
    
    fig2.update_layout(
        **update_layout_simple,
        height=140,
        yaxis=dict(visible=False, showgrid=False),
        xaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),
        font=dict(family="serif", color="white", size=10)
    )
    
    disaster = "Disasters group" if category == "Disasters Subgroup" else "Disaster type"
    
    fig2.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        x=0, y=1,
        xanchor="left",
        showarrow=False,
        text=f"{disaster}",
        font=dict(size=12, family="serif")
    )
    
    children=[
        html.Div(className="row", children=[
            html.Div(className="col", children=[
                dcc.Graph(config=dict(displayModeBar=False), figure=fig2), 
            ])
        ])
    ]
    
    return fig, children



@callback(
    Output("geo-map", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
)
def update_choropleth_graph(range_date, geo, metric):
    data = data_date_filter(df, range_date)
    data = data_geo_filter(data, geo)

    data_attack = data.groupby(["ISO", "Country"], as_index=False).size()
    data_casualty = data.groupby(["ISO", "Country"], as_index=False)[list_casualties].sum()
    data = pd.merge(data_attack, data_casualty, on=["ISO", "Country"])
    
    title_mapping = {
        "size": "Natural disasters occurrence per country",
        "Total Deaths": "Number of deaths from natural disasters per country",
        "No Injured": "Number of injured from natural disasters per country",
        "Total Affected": "Number of total people affected from natural disasters per country",
        "Total Damages ('000 US$)": "Economic damages (in $) from natural disasters per country",
        "No Homeless": "Number of people left homeless from natural disasters per country"
    }
    
    title = title_mapping.get(metric)


    fig = go.Figure(
        go.Choropleth(
            z=data[metric],
            locations=data["ISO"],
            colorscale=px.colors.sequential.Reds,
            marker=dict(line=dict(width=.3, color="black")),
            zmin=0, zmax=data[metric].max(),
            customdata=data,
            showscale=False
        )
    )

    fig.update_layout(**choroplath_layout(400))
    
    fig.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        y=1,
        xanchor="center",
        showarrow=False,
        text=f"<b style='font-size: 15px; color:white'>{title}</b><br>"
        "<b>Data source:</b> <a style='color:silver' href='https://www.emdat.be'>EM-DAT</a> "
        "<b>Author:</b> <span style='color:silver'>Chris Baudelaire .K</span>",
        font=dict(size=11, family="serif")
    )

    return fig


@callback(
    Output("timeseries-world", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
    Input("choice-dropdown", "value"),
    Input("type-graph", "value")
)
def global_incidence_timeseries(range_date, geo, metric, category, choice, graph):
    # Data filter
    data = data_date_filter(df, range_date)
    data = data_geo_filter(data, geo)
    data = data_filter(data, category, choice)

    # Title Mapping
    title_mapping = {
        "size": "Evolution of the Number of natural<br>disasters occured",
        "Total Deaths": "Evolution of the Number of<br>people dead",
        "No Injured": "Evolution of the Number of<br>people injured",
        "Total Affected": "Evolution of the Number of total<br>people affected",
        "Total Damages ('000 US$)": "Evolution of the Number of<br>economic damages",
        "No Homeless": "Evolution of the Number of people<br>left homeless"
    }

    if metric == "size":
        data = data.groupby(["Year"], as_index=False).size()
    else:
        data = data.groupby(["Year"], as_index=False)[list_casualties].sum()

    title = title_mapping.get(metric, f"Evolution of {metric}<br>Due to Terrorist Activity")
    subtitle = f"{geo}: {range_date[0]} - {range_date[1]}"

    data["cumsum"] = data[metric].cumsum()

    if graph == "bar":
        fig = px.bar(data, x="Year", y=metric, color=metric, color_continuous_scale="reds")
    elif graph == "line":
        fig = px.line(data, x="Year", y=metric)
        fig.update_traces(
            mode="lines", line=dict(color="firebrick"),
        )
    else:
        fig = px.area(data, x="Year", y=metric)
        fig.update_traces(
            mode="none", line=dict(color="firebrick"), fillcolor="firebrick", opacity=1
        )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        **update_layout_simple,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title=None, showgrid=False),
        margin=dict(l=0, r=0, b=43),
        font=dict(family="serif", color="white", size=10),
        height=350,
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>{subtitle}</sup>"
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


@callback(
    Output("timeseries-category", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
    Input("type-serie", "value"),
)
def region_timerseries(range_date, geo, metric, category, type_serie):
    # fiter data
    data_date = data_date_filter(df, range_date)
    filter_data = data_geo_filter(data_date, geo)
    
    custom_colors = px.colors.sequential.Blues[::-2] + px.colors.sequential.Reds[4:]

    colors = custom_colors if category == "Disaster Type" else \
        ['rgb(252,187,161)', 'rgb(251,106,74)',
         'rgb(203,24,29)', 'rgb(103,0,13)']
    
    cat = "group" if category == "Disaster Group" else "type"
        
    # Title Mapping
    title_mapping = {
        "size": f"Evolution by {cat} of the number<br>of natural disasters",
        "Total Deaths": f"Evolution by {cat} of the<br>number of people deaths",
        "No Injured": f"Evolution by {cat} of the<br>number of people injured",
        "Total Affected": f"Evolution by {cat} of the number<br>of total people affected",
        "Total Damages ('000 US$)": f"Evolution by {cat} of<br>economic damages",
        "No Homeless": f"Evolution by {cat} of the number<br>of people left homeless"
    }

    title = title_mapping.get(metric)
    subtitle = f"{geo}: {range_date[0]} - {range_date[1]}"

    if metric == "size":
        data = filter_data.groupby(["Year", category], as_index=False).size()
        columns = list(filter_data.groupby([category], as_index=False).size().sort_values(by=metric)[category].values)

    else:              
        data = filter_data.groupby(["Year", category], as_index=False)[list_casualties].sum()
        columns = list(filter_data.groupby([category], as_index=False)[metric].sum().sort_values(by=metric)[category].values)

    data = data.pivot_table(index="Year", columns=category, values=metric)
    data = data[columns]
    data = data.fillna(0).reset_index()

    fig = absolute_relative_figure(data, colors, type_serie, title, subtitle, 350)

    return fig


@callback(
    Output("rate", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
    Input("choice-dropdown", "value")
)
def rate_func(range_date, area, metric, category, choice):
    # fiter data
    data = data_date_filter(df, range_date)
    data = data_geo_filter(data, area)
    data = data_filter(data, category, choice)

    if metric == "size": 
        data = data.groupby(["Year"], as_index=False).size()
        title = "Rate of Growth in the Number of Natural Disasters"
    else:
        data = data.groupby(["Year"], as_index=False)[list_casualties].sum()
        title = "Rate of Growth in the Number of Deaths" if metric == "nkill" else "Rate of Growth in the Number of Injured"

    data["rate"] = round((data[metric].pct_change(10)) * 100, 2)
    data["relative_rate"] = (data[metric].diff().fillna(0).astype(int)).apply(lambda x: "+" + str(x) if x > 0 else str(x))
    data['text'] = data.apply(lambda row: f"{row['rate']}%", axis=1)

    data_rate = data.copy().iloc[1:, :]

    fig = px.bar(data_rate.iloc[10:, :], x="Year", y="rate", color="rate", color_continuous_scale="reds")

    fig.update_traces(
        #text=data["relative_rate"],
        textposition="outside",
        textfont=dict(size=14, family="Lora")
    )

    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        **update_layout_simple,
        margin=dict(l=0, r=0, b=50),
        yaxis=dict(showgrid=False, ticksuffix="%"),
        xaxis=dict(title=None, showgrid=False),
        font=dict(family="serif", color="white", size=10),
        height=350,
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>Percentage Change per Decade: {range_date[0]} - {range_date[1]}"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.8,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -.15)

    return fig


@callback(
    Output("share", "children"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
    Input("choice-dropdown", "value")
)
def share_of(range_date, geo, metric, category, choice):
    colors = ['rgb(239,59,44)', 'rgb(103,0,13)',]
    rel_abs = "relative"
    
    
    def group_data(df):
        mapping = {
            "size": (f"Share of natural disasters in {geo} in<br>the Total Number of disasters", 
                     "Proportion of Number of<br>Natural Disasters"),
            "Total Deaths": (f"Share of deaths in {geo} in<br>the Total number of deaths", 
                             "Proportion of Number<br>of Deaths"),
            "No Injured": (f"Share of injured in {geo} in<br>the Total number of injured", 
                           "Proportion of Number<br>of Injured"),
            "Total Affected": (f"Share of total affected in {geo} in<br>the Total number of affected",
                               "Evolution of the Number of total<br>people affected"),
            "Total Damages ('000 US$)": (f"Share of economic damages in {geo} in<br>the Total number of economic damages",
                                         "Evolution of the Number of<br>economic damages"),
            "No Homeless": (f"Share of people left homeless in {geo} in<br>the Total Number of people homeless",
                            "Evolution of the Number of people<br>left homeless")
        }

        title, title_pie = mapping.get(metric, ("Unknown Metric", "Unknown Metric"))

        if metric == "size":
            df = df.groupby(["Year"], as_index=False).size()
        else:              
            df = df.groupby(["Year"], as_index=False)[metric].sum()
            
        return df, title, title_pie


    data = data_date_filter(df, range_date)
    data = data_geo_filter(data, geo)
    data = data_filter(data, category, choice)

    if geo == "World":
        children = []
    else:

        if geo in list(df.Continent.unique()):
            dfr = df[df.Continent != geo]
        if geo in list(data.Region.unique()):
            dfr = df[df.Region != geo]

        data, title, title_pie = group_data(data)
        data.rename(columns={metric: geo}, inplace=True)
        dfr, _, _ = group_data(df)
        dfr.rename(columns={metric: "The Rest of the World"}, inplace=True)

        merged_data = pd.merge(data, dfr, on="Year")
        fig = absolute_relative_figure(
            merged_data, colors, rel_abs, title, "In Comparison to the Rest of the World", 330)

        dframe = merged_data.set_index("Year").sum().reset_index()

        fig2 = go.Figure(go.Pie(
            labels=dframe["index"], values=dframe[0],
            textposition="outside", textinfo="label+percent",
            textfont=dict(size=13.6, family="Lato"),
            marker=dict(colors=colors),
            insidetextorientation='radial',
            pull=[.2]+[0] * 10,  # hole=.5
        ))

        fig2.update_layout(
            height=420,
            template="plotly_dark",
            showlegend=False,
            margin=dict(autoexpand=True, l=0, r=0),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            title={
                "text": (
                    f"<b>{title_pie}</b><br />"
                    f"<sup style='color:silver'>In Comparison to the Rest of the World"
                ),
                "font": {"family": "serif", "size": 20, "color": "white"},
                "x": 0.93,
                "y": 0.86,
                "xanchor": "right",
                "yanchor": "top",
            },
        )

        legend(fig2, 1, -.15)

        children = [
            html.Div(className="col-lg-7", children=[
                dcc.Loading(dcc.Graph(id="share-graph", figure=fig), color="firebrick", type="dot"),
            ]),

            html.Div(className="col-lg-5", children=[
                dcc.Loading(dcc.Graph(id="share-dist", figure=fig2), color="firebrick", type="dot"),
            ])

        ]

    return children



@callback(
    Output("proportion-by-contnent", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
)
def graph(range_date, geo, metric, category):  
    # fiter data
    data_date = data_date_filter(df, range_date)
    filter_data = data_geo_filter(data_date, geo)
    
    if metric == "size":
        val, aggfunc = category, "count"
    else:
        val, aggfunc = metric, "sum"
        
    colors =['rgb(255,245,240)','rgb(252,187,161)','rgb(251,106,74)','rgb(203,24,29)','rgb(103,0,13)'][::-1]
    
    data = pd.crosstab(
        index=filter_data[category], 
        columns=filter_data["Continent"], 
        values=filter_data[val] , 
        aggfunc=aggfunc, 
        normalize="index"
    )
    
    data = data * 100
    data = round(data, 1)
    data = data[["Asia", "Americas", "Europe", "Africa", "Oceania"]]
    
    cat = "group" if category == "Disaster Group" else "type"
    title = f"Rate of Natural Disasters<br>{cat} by Continent"
    subtitle = f"Year: {range_date[0]} - {range_date[1]}"
        
    fig = dist_fig(data, colors, title, subtitle)
    
    return fig




@callback(
    Output("decadal_avg", "figure"),
    Input("filter-geo", "value"),
)
def decadal_and_share(area):
    # fiter data
    data = data_geo_filter(df, area)
    
    data = data.groupby(["Year"], as_index=False)[["Total Deaths"]].sum()
    data['Decade'] = (data['Year'] // 10) * 10
    decade_avg = data.groupby('Decade')['Total Deaths'].mean().reset_index()
    
    fig = px.bar(decade_avg, x="Decade", y="Total Deaths", color="Total Deaths", color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(
        **update_layout_simple,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, b=43),
        font=dict(family="serif", color="white"),
        height=350,
        title={
            "text": (
                f"<b>Decadal Average of the Number of Deaths</b><br />"
                f"<sup style='color:silver'>Average Calculated Over a 10-Year Period </sup>"
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



@callback(
    Output("div-deaths", "children"),
    Output("div-events", "children"),
    Input("metric", "value"),
    Input("filter-geo", "value"),
)
def div_death_callack(metric, geo):
    if metric == "Total Deaths":
        div_deaths = [
            html.Div(className="row align-items-center mt-5", children=[

                html.Div(className="col-md-6", children=[
                    dcc.Graph(config=dict(displayModeBar=False), id="decadal_avg"),
                ]),

                html.Div(className="col-md-6", children=[
                    dcc.Graph(config=dict(displayModeBar=False), figure=disaster_deaths_rate()),
                ])

            ]),
            
            
            html.Div(className="row align-items-center mt-5 card-deaths-evolution", children=[

                html.Div(className="col-12", children=[
                    html.H5("Historical Record of Deaths (overall and by type)"),
                    dcc.Graph(config=dict(displayModeBar=False), figure=death_func()),
                ])

            ]),


        ]
        
        div_events = []
        
    elif (metric == "size" and geo == "World"):
        div_events = [
            html.Div(className="row align-items-center mt-5", children=[

                html.Div(className="col-md-7", children=[
                    dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=heatmap_season()), color="red")
                ]),

                html.Div(className="col-md-5", children=[
                    dcc.Loading(dcc.Graph(config=dict(displayModeBar=False), figure=month_events()), color="red")
                ])
            ])
        ]
        
        div_deaths = []
        
    else:
        div_events, div_deaths = [], []
        
    return div_deaths, div_events



# --------------------------------------------------------------------------------------------------------

@callback(
    Output("ranking-graph", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
)
def update_ranking_graph(range_date, geo, metric, category):
    # fiter data
    data_date = data_date_filter(df, range_date)
    filter_data = data_geo_filter(data_date, geo)

    sub_category = "Disaster Type" if category == "Disaster Subgroup" else "Disaster Subtype"

    if metric == "size":
        data2 = filter_data.groupby([sub_category], as_index=False).size()
    else:
        data2 = filter_data.groupby([sub_category], as_index=False)[metric].sum()
        
    data2 = data2.fillna(0)

    data2["percent"] = (data2[metric] / data2[metric].sum()) * 100
    data2 = data2.sort_values(by=metric, ascending=False)
    data2["percent_cum"] = round(data2["percent"].cumsum(), 1)
    data2["color"] = np.where(data2[metric] > data2[metric].mean(), 'firebrick', 'rgb(100, 100, 100)')
    data2["percent_cum_bis"] = data2["percent_cum"]

    for i, item in enumerate(data2["color"]):
        if item == "firebrick":
            data2.iat[i, 4] = px.colors.sequential.Reds_r[i]
            data2.iat[i, 5] = str(data2.iat[i, 5]) + "%"
        else:
            if data2.iat[i, 5] != float(100):
                data2.iat[i, 5] = ""
            else:
                data2.iat[i, 5] = str(data2.iat[i, 5]) + "%"
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_bar(
        x=data2[sub_category],
        y=data2[metric],
        marker=dict(color=data2["color"]),
        text=data2[metric],
        texttemplate="%{y:.2s}",
        textposition="outside",
        textfont=dict(size=16, family="Lora"),
    )

    # fig = px.bar(data2, y=metric, x=sub_category, color=metric, color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)

    fig.add_scatter(
        x=data2[sub_category],
        y=data2["percent_cum"],
        mode="lines+markers+text",
        text=data2["percent_cum_bis"],
        # texttemplate="%{text}%",
        textposition="top center",
        textfont=dict(size=12, family="serif"),
        secondary_y=True
    )

    fig.add_hline(
        y=data2[metric].mean(),
        line=dict(dash="dot"),
        annotation_text=f"Average of All<br>Subtypes: <br> Moy={round(data2[metric].mean(), 2)}"
    )

    fig.update_layout(
        **update_layout_simple,
        height=390,
        showlegend=False,
        yaxis=dict(visible=False, showgrid=False),
        yaxis2=dict(visible=False, showgrid=False),
        xaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Ranking by Disaster {sub_category}</b><br />"
                f"<sup style='color:silver'>{geo}: ({range_date[0]} - {range_date[1]}) "
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.88,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -1.3)

    return fig



@callback(
    Output("region-country-vbar", "figure"),
    Input("date-range-slider", "value"),
    Input("chip-region-country", "value"),
    Input("metric", "value"),
)
def update_ranking_graph(range_date, geo, metric):
    
    data = data_date_filter(df, range_date)

    if metric == "size":
        data2 = data.groupby([geo], as_index=False).size()
    else:
        data2 = data.groupby([geo], as_index=False)[metric].sum()
        

    data2["percent"] = (data2[metric] / data2[metric].sum()) * 100
    data2 = data2.sort_values(by=metric, ascending=False)
    
    if geo == "Country":
        data2 = data2.iloc[:20, :]
    
    data2["percent_cum"] = round(data2["percent"].cumsum(), 1)
    data2["color"] = np.where(
        data2[metric] > data2[metric].mean(), 'firebrick', 'rgb(100, 100, 100)')
    data2["percent_cum_bis"] = data2["percent_cum"]

    for i, item in enumerate(data2["color"]):
        if item == "firebrick":
            data2.iat[i, 4] = px.colors.sequential.Reds_r[i]
            data2.iat[i, 5] = str(data2.iat[i, 5]) + "%"
        else:
            if data2.iat[i, 5] != float(100):
                data2.iat[i, 5] = ""
            else:
                data2.iat[i, 5] = str(data2.iat[i, 5]) + "%"

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_bar(
        x=data2[geo],
        y=data2[metric],
        marker=dict(color=data2["color"]),
        text=data2[metric],
        texttemplate="%{y:.2s}",
        textposition="outside",
        textfont=dict(size=16, family="serif"),
    )

    # fig = px.bar(data2, y=metric, x=sub_category, color=metric, color_continuous_scale="reds")
    fig.update_coloraxes(showscale=False)

    fig.add_scatter(
        x=data2[geo],
        y=data2["percent_cum"],
        mode="lines+markers+text",
        text=data2["percent_cum_bis"],
        # texttemplate="%{text}%",
        textposition="top center",
        textfont=dict(size=12, family="serif"),
        secondary_y=True
    )


    fig.add_hline(
        y=data2[metric].mean(),
        line=dict(dash="dot"),
        annotation_text=f"Average of All<br>Subtypes: <br> Moy={round(data2[metric].mean(), 2)}"
    )

    fig.update_layout(
        **update_layout_simple,
        height=390,
        showlegend=False,
        yaxis=dict(visible=False, showgrid=False),
        yaxis2=dict(visible=False, showgrid=False),
        xaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        font=dict(family="serif", color="white", size=10),
        title={
            "text": (
                f"<b>Ranking by region</b><br />"
                f"<sup style='color:silver'>{metric}: {range_date[0]} - {range_date[1]}"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.88,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -1.3)

    return fig




@callback(
    Output("hbar-disaster-group-and-type", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
)
def hbar_disaster_group_and_type(range_date, geo, metric, category):
    # fiter data
    data_date = data_date_filter(df, range_date)
    filter_data = data_geo_filter(data_date, geo)

    if category == "Disaster Subgroup":
        title = "Distribution by Disaster Group"
    else:
        title = "Distribution by Disaster Type"

    if metric == "size":
        data = filter_data.groupby(category, as_index=False).size()
    else:
        data = filter_data.groupby(category, as_index=False)[list_casualties].sum()

    fig = px.bar(data, x=metric, y=category, color=metric, color_continuous_scale="reds", orientation="h")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(categoryorder='total ascending')

    fig.update_traces(
        text=data[metric],
        texttemplate="%{x:.2s}",
        textposition="auto",
        textfont=dict(size=13, family="serif")
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
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>{geo}: ({range_date[0]} - {range_date[1]}) "
            ),
            "font": {"family": "serif", "size": 17, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -1.3)

    return fig


@callback(
    Output("hbar-continent", "figure"),
    Input("date-range-slider", "value"),
    Input("metric", "value"),
)
def region_timerseries(range_date, metric):
    # fiter data
    data = data_date_filter(df, range_date)

    if metric == "size":
        subtitle = "Events"
        data = data.groupby("Continent", as_index=False).size()
    else:
        subtitle = metric
        data = data.groupby("Continent", as_index=False)[
            list_casualties].sum()

    fig = px.bar(data, x=metric, y="Continent", color=metric, color_continuous_scale="reds", orientation="h")
    fig.update_coloraxes(showscale=False)
    fig.update_yaxes(categoryorder='total ascending')

    fig.update_traces(
        text=data[metric],
        texttemplate="%{x:.2s}",
        textposition="auto",
        textfont=dict(size=13, family="serif")
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
                f"<b>Ranking by continent</b><br />"
                f"<sup style='color:silver'>{subtitle}: {range_date[0]} - {range_date[1]}"
            ),
            "font": {"family": "serif", "size": 17, "color": "white"},
            "x": 0.98,
            "y": 0.93,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -1.3)

    return fig




@callback(
    Output("group-repartition", "figure"),
    Input("date-range-slider", "value"),
    Input("filter-geo", "value"),
    Input("metric", "value"),
    Input("dropdown-category", "value"),
)
def graph(range_date, geo, metric, category):
    # fiter data
    data_date = data_date_filter(df, range_date)
    filter_data = data_geo_filter(data_date, geo)

    sub_category = "Disaster Type" if category == "Disaster Subgroup" else "Disaster Subtype"

    if metric == "size":
        data = filter_data.groupby([category, sub_category]).size(
        ).reset_index().rename(columns={0: metric})
    else:
        data = filter_data.groupby([category, sub_category])[
            list_casualties].sum().reset_index()

    title = "Distribution Type and Subtype"
    data = data.set_index([category, sub_category])

    xlabels = [list(data.index.get_level_values(0)),
               list(data.index.get_level_values(1)),
               data.index]

    unique_types = data.index.get_level_values(0).unique()
    color_scale = px.colors.qualitative.Plotly[:len(unique_types)]
    type_to_color = {type: color for type,
                     color in zip(unique_types, color_scale)}
    sub_type_colors = [type_to_color[type]
                       for type in data.index.get_level_values(0)]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=data[metric],
            x=xlabels,
            name=metric,
            showlegend=False,
            width=.9,
            marker=dict(color=sub_type_colors),
            text=data[metric],
            texttemplate="%{y:.2s}",
            textposition='outside',
        )
    )

    fig.update_layout(
        **update_layout_simple,
        showlegend=False,
        xaxis=dict(title=None, showgrid=False),
        yaxis=dict(title=None, showgrid=False),
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=43),
        font=dict(family="serif", color="white", size=10),
        height=390,
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>Évolution de {range_date[0]} à {range_date[1]}</sup>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.94,
            "xanchor": "right",
            "yanchor": "top",
        },
    )

    legend(fig, 1, -1.3)

    return fig
