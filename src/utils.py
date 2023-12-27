import plotly.graph_objects as go
import numpy as np
from scipy.io import netcdf_file
import warnings
import pandas as pd
from plotly.subplots import make_subplots
from plotly.express.colors import sample_colorscale
from constants import *

import plotly.express as px


def choroplath_layout(height):
    return dict(
        **update_layout_geo,
        height=height,
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(autoexpand=True, l=0, r=0, t=0, b=0),

    )



update_layout_simple = {
    "template": "plotly_dark",
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "hovermode": "x",
}


def get_season(month):
    if month in ["December", "January", "February"]:
        return "Winter"
    elif month in ["March", "April", "May"]:
        return "Spring"
    elif month in ["June", "July", "August"]:
        return "Summer"
    else:
        return "Autumn"


def sorted_by(df, column, list_order):
    df_sorted = df.sort_values(by=column, key=lambda col: col.map({v: k for k, v in enumerate(list_order)}))
    return df_sorted



def legend(fig, x, y):
    return fig.add_annotation(
        xref="paper", yref="paper",
        name="Data source",
        x=x, y=y,
        xanchor="right",
        showarrow=False,
        text="<b>Data source:</b> <a style='color:silver' href='https://www.emdat.be'>EM-DAT </a> "
        "<b>Author:</b> Chris Baudelaire .K",
        opacity=0.5,
        font=dict(size=9, family="serif")
    )


def calculate_percentage(df):
    total = df.sum()
    return (df / total) * 100


def absolute_relative_figure(df, list_colors, choice_graph, title, subtitle, height):

    if choice_graph == "absolue":
        fig = px.area(df, x="Year", y=df.columns, color_discrete_sequence=list_colors)

        for trace, color in zip(fig.data, list_colors):
            trace.update(fill='tonexty', mode='lines', line=dict(color="black", width=.8), fillcolor=color, opacity=1)

        y_axis = dict(title=None, showgrid=False)
        legende = dict(orientation="v", title=None, x=.03, y=.95)

    elif choice_graph == "relative":
        df[df.columns[1:]] = df[df.columns[1:]].apply(calculate_percentage, axis=1)
        fig = px.area(df, x="Year", y=df.columns, color_discrete_sequence=list_colors)

        for trace, color in zip(fig.data, list_colors):
            trace.update(fill='tonexty', mode='lines', line=dict(color="black", width=3), fillcolor=color, opacity=1)

        y_axis = dict(ticksuffix="%", title=None, showgrid=False)
        legende = dict(orientation="h", title=None)

        for trace in fig.data:
            trace.update(line=dict(shape="spline", smoothing=.5, width=0))

    else:
        df[df.columns[1:]] = df[df.columns[1:]].apply(calculate_percentage, axis=1)
        fig = px.bar(df, x="Year", y=df.columns, barmode="stack", color_discrete_sequence=list_colors)
       
        y_axis = dict(ticksuffix="%", title=None, showgrid=False)
        legende = dict(orientation="h", title=None)

    fig.update_layout(
        hovermode="x",
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font={"family": "Lato", "size": 10},
        margin=dict(autoexpand=True, l=0, r=0, t=60, b=43),
        legend=legende,
        height=height,
        xaxis=dict(title=None, showgrid=False),
        yaxis=y_axis,
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>{subtitle}</sup>"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.91,
            "xanchor": "right",
                "yanchor": "top",
        }
    )

    legend(fig, 1, -.15)

    return fig



def get_colorscale(series: pd.Series):
    """
    Calculate colorscale for a given series of values.
    """

    # Get difference between year's value and mean of reference period
    diff = series.copy().to_numpy()

    # Create masks for above and below mean
    mask_above = diff > 0
    mask_below = diff < 0

    # Get absolute value of difference
    diff = abs(diff)

    # Create array of zeros with same shape as diff
    diff_norm = np.zeros_like(diff)

    # Calculate min and max for values above the mean
    if len(diff[mask_above]) > 0:
        max_above = np.nanmax(diff[mask_above])
        min_above = np.nanmin(diff[mask_above])

        # Normalize to 0-1
        diff_norm[mask_above] = (
            diff[mask_above] - min_above) / (max_above - min_above)

    # Calculate min and max for values below the mean
    if len(diff[mask_below]) > 0:
        max_below = np.nanmax(diff[mask_below])
        min_below = np.nanmin(diff[mask_below])

        # Normalize to 0-1
        diff_norm[mask_below] = (
            diff[mask_below] - min_below) / (max_below - min_below)

    # Create array of white colors with same shape as diff
    colors = np.full_like(diff, "rgb(255, 255, 255)", dtype="object")

    # Sample colors from colormaps, using normalized values
    colors[mask_above] = sample_colorscale("YlOrRd", diff_norm[mask_above])
    colors[mask_below] = sample_colorscale("YlGnBu", diff_norm[mask_below])

    return colors


# Fonction utilitaires pour la construction d'une carte de chaleur avec plotly et basemap de matplotlib

def load_netcdf_data(path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        netcdf_data = netcdf_file(path, 'r')
    return netcdf_data


def longitude_and_nd_variable(lon, var_nd):
    tmp_lon = np.array([lon[n]-360 if l >= 180 else lon[n]
                       for n, l in enumerate(lon)])

    i_east, = np.where(tmp_lon >= 0)
    i_west, = np.where(tmp_lon < 0)
    lon = np.hstack((tmp_lon[i_west], tmp_lon[i_east]))

    var_nd_array = np.array(var_nd)
    var_nd = np.hstack((var_nd_array[:, i_west], var_nd_array[:, i_east]))

    return lon, var_nd


def polygons_to_traces(poly_paths, N_poly, m):
    '''
    Functions converting coastline/country polygons to lon/lat traces

    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    # initialize plotting list
    data = dict(x=[], y=[], mode='lines', line=dict(color="black"), name=' ')

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]

        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0], vertex[1])
             for (vertex, _) in poly_path.iter_segments(simplify=False)]
        )

        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:, 0], coords_cc[:, 1], inverse=True)

        # add plot.ly plotting options
        data['x'] = data['x'] + lon_cc.tolist() + [np.nan]
        data['y'] = data['y'] + lat_cc.tolist() + [np.nan]

        # traces.append(make_scatter(lon_cc,lat_cc))

    return [data]


def get_coastline_traces(m):
    """
    Function generating coastline lon/lat traces
    """
    poly_paths = m.drawcoastlines().get_paths()  # coastline polygon paths
    N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
    return polygons_to_traces(poly_paths, N_poly, m)


def get_country_traces(m):
    """
    Function generating country lon/lat traces
    """
    poly_paths = m.drawcountries().get_paths()  # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    return polygons_to_traces(poly_paths, N_poly, m)


def trace(ndim_var, lon, lat, colorscale):
    trace = go.Contour(
        z=ndim_var, x=lon, y=lat,
        zauto=False,
        # zmin=-5, zmax=5,
        colorscale=colorscale,
        contours=contours,
        colorbar=colorbar
    )

    return trace


def figure(m, trace):
    traces_cc = get_coastline_traces(m)+get_country_traces(m)
    data = [trace] + traces_cc
    fig = go.Figure(data=data)
    return fig


def update_layout(fig, lon):
    return fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, l=0, t=100, r=0, b=0),
        showlegend=False,
        hovermode="closest",
        xaxis=dict(axis_style, range=[lon[0], lon[-1]]),
        yaxis=dict(axis_style),

        autosize=True,
        height=400,
    )


# Fonction utilitaires pour la construction d'un Globe 3D

def degree2radians(degree):
    """convert degrees to radians"""
    return degree*np.pi/180


def mapping_map_to_sphere(lon, lat, radius=1):
    """this function maps the points of coords (lon, lat) to points onto the  sphere of radius radius"""
    lon = np.array(lon, dtype=np.float64)
    lat = np.array(lat, dtype=np.float64)
    lon = degree2radians(lon)
    lat = degree2radians(lat)
    xs = radius*np.cos(lon)*np.cos(lat)
    ys = radius*np.sin(lon)*np.cos(lat)
    zs = radius*np.sin(lat)
    return xs, ys, zs


def polygons_to_traces_globe(poly_paths, N_poly, m):
    '''
    Functions converting coastline/country polygons to lon/lat traces

    pos arg 1. (poly_paths): paths to polygons
    pos arg 2. (N_poly): number of polygon to convert
    '''
    # init. plotting list
    lons = []
    lats = []

    for i_poly in range(N_poly):
        poly_path = poly_paths[i_poly]

        # get the Basemap coordinates of each segment
        coords_cc = np.array(
            [(vertex[0], vertex[1])
             for (vertex, code) in poly_path.iter_segments(simplify=False)]
        )

        # convert coordinates to lon/lat by 'inverting' the Basemap projection
        lon_cc, lat_cc = m(coords_cc[:, 0], coords_cc[:, 1], inverse=True)

        lats.extend(lat_cc.tolist()+[None])
        lons.extend(lon_cc.tolist()+[None])

    return lons, lats


def get_coastline_traces_globe(m):
    """Function generating coastline lon/lat """
    poly_paths = m.drawcoastlines().get_paths()  # coastline polygon paths
    N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
    cc_lons, cc_lats = polygons_to_traces_globe(poly_paths, N_poly, m)
    return cc_lons, cc_lats


def get_country_traces_globe(m):
    """Function generating country lon/lat"""
    poly_paths = m.drawcountries().get_paths()  # country polygon paths
    N_poly = len(poly_paths)  # use all countries
    country_lons, country_lats = polygons_to_traces_globe(
        poly_paths, N_poly, m)
    return country_lons, country_lats


def boundaries(xs, ys, zs):
    return dict(
        type='scatter3d',
        x=xs, y=ys, z=zs,
        mode='lines',
        line=dict(color='black', width=1)
    )


def ndim_var_array(clons, ncolumns, ndim_var):
    NDIM_VAR = np.zeros(clons.shape, dtype=np.float64)
    NDIM_VAR[:, :ncolumns-1] = np.copy(np.array(ndim_var,  dtype=np.float64))
    NDIM_VAR[:, ncolumns-1] = np.copy(ndim_var[:, 0])
    return NDIM_VAR


def sphere(XS, YS, ZS, nd_var, text=None):
    return dict(
        type='surface',
        x=XS, y=YS, z=ZS,
        colorscale="jet",
        surfacecolor=nd_var,
        cmin=-5, cmax=5,
        colorbar=dict(thickness=10, len=0.6, ticklen=2, title='Temp'),
        text=text,
        hoverinfo='text'
    )


def layout3d(year):
    noaxis = dict(
        showbackground=False,
        showgrid=False,
        showline=False,
        showticklabels=False,
        ticks='',
        title='',
        zeroline=False
    )

    return dict(
        template="plotly_dark",
        height=400,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(autoexpand=True, t=0, l=0, r=0, b=0),
        font=dict(family='serif', size=14),
        scene=dict(
            xaxis=noaxis,
            yaxis=noaxis,
            zaxis=noaxis,
            aspectratio=dict(x=1.45, y=1.45, z=1.45),
            camera=dict(eye=dict(x=1.1, y=1.1, z=1.1))
        ),
        
        annotations=[
            dict(
                text=f"<b style='font-size:16px'>November {year}</b><br>Surface Temperature Anomaly <br>"
                "<b>Source:</b> <a href='https://data.giss.nasa.gov/gistemp/maps/'>GISS-NASA</a>",
                xref='paper', yref='paper',
                y=0.1, x=1,
                yanchor='bottom',
                showarrow=False,
                font=dict(size=11, family="serif")
            )
        ]
    )


# ---------------------------------------------------------------------------------------------------------

def dist_fig(data, colorscale, title, subtitle):

    top_labels = data.columns.tolist()
    x_data = data.values.tolist()
    y_data = data.index.tolist()

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colorscale[i],
                    line=dict(color="rgb(27, 27, 27)", width=3)
                )
            ))

    fig.update_layout(
        height=330,
        font=dict(family='serif', size=10, color='white'),
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.14, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        autosize=True,
        template='plotly_dark',
        margin=dict(l=0, b=0, r=0, t=110),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        title={
            "text": (
                f"<b>{title}</b><br />"
                f"<sup style='color:silver'>{subtitle}"
            ),
            "font": {"family": "serif", "size": 20, "color": "white"},
            "x": 0.98,
            "y": 0.89,
            "xanchor": "right",
            "yanchor": "top",
        },
    ),

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='serif', size=12,
                                          color='white'),
                                showarrow=False, align='right'))
       
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='serif', size=12,
                                              color='white'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):

            if yd == y_data[-1]:
                annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='serif', size=12,
                                                      color='white'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig



def horizontal_bar_labels(df, key, value, color):
    data = df.to_dict("records")

    fig = make_subplots(
        rows=len(data),
        cols=1,
        subplot_titles=[x[key] for x in data],
        shared_xaxes=True,
        print_grid=False,
        vertical_spacing=(0.45 / len(data)),
    )

    # add bars for the categories
    for k, x in enumerate(data):
        fig.add_trace(dict(
            type='bar',
            orientation='h',
            y=[x[key]],
            x=[x[value]],
            text=["{:,.0f}".format(x[value])],
            hoverinfo='text',
            textposition='outside',
            marker=dict(color=color),
        ), k+1, 1)

    for x in fig["layout"]['annotations']:
        x['x'] = 0
        x['xanchor'] = 'left'
        x['align'] = 'left'
        x['font'] = dict(
            size=14,
        )

    for axis in fig['layout']:
        if axis.startswith('yaxis') or axis.startswith('xaxis'):
            fig['layout'][axis]['visible'] = False

    fig.update_layout(
        template='plotly_dark',
        margin=dict(l=0, b=0, r=0, t=90),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )

    return fig
