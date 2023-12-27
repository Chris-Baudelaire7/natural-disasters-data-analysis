from mpl_toolkits.basemap import Basemap
import plotly.graph_objs as go
import numpy as np

from constants import *
from utils import *


path_2023 = "data/amaps-2023.nc"
path_1970 = "data/amaps-1970.nc"



def temp_anomaly(path, year):
    netcdf_data = load_netcdf_data(path)

    lon = netcdf_data.variables['lon'][::]
    lat = netcdf_data.variables['lat'][::-1]
    ndim_var = netcdf_data.variables['TEMPANOMALY'][::-1]
    lon, ndim_var = longitude_and_nd_variable(lon, ndim_var)

    m = Basemap()
    cc_lons, cc_lats = get_coastline_traces_globe(m)
    country_lons, country_lats = get_country_traces_globe(m)
    lons = cc_lons+[None]+country_lons
    lats = cc_lats+[None]+country_lats

    xs, ys, zs = mapping_map_to_sphere(lons, lats, radius=1.01)
    clons = np.array(lon.tolist()+[180], dtype=np.float64)
    clats = np.array(lat, dtype=np.float64)
    clons, clats = np.meshgrid(clons, clats)
    XS, YS, ZS = mapping_map_to_sphere(clons, clats)

    _, ncolumns = clons.shape
    NDIM_VAR = ndim_var_array(clons, ncolumns, ndim_var)
    fig = go.Figure(data=[sphere(XS, YS, ZS, NDIM_VAR), boundaries(xs, ys, zs)], layout=layout3d(year))

    return fig
