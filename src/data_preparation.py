import pandas as pd
import json


def data_date_filter(df, range_date):
    data = df[(df["Year"] >= range_date[0]) & (df["Year"] <= range_date[1])]
    return data


def data_geo_filter(dataframe, area):
    if area == "World":
        data = dataframe.copy()
    elif area in list(dataframe.Continent.unique()):
        data = dataframe[dataframe.Continent == area]
    elif area in list(dataframe.Region.unique()):
        data = dataframe[dataframe.Region == area]
    else:
        data = dataframe[dataframe.Country == area]

    return data


def data_filter(df, category, choice):
    elements = list_category if category == "Disaster Subgroup" else list_group
    data = df[
        df[category] == choice if choice in elements else df[category] == df[category]
    ]
    return data


data_country_geojson_path = "data/countries.geojson"
data_country_geojson = json.load(open(data_country_geojson_path, "r"))

df = pd.read_csv("data/data.csv", low_memory=False)

df_country_geojson_path = "data/countries.geojson"
df_country_geojson = json.load(open(df_country_geojson_path, "r"))

state_id_map = {}

for feature in data_country_geojson["features"]:
    feature["id"] = feature["properties"]["ISO_A3"]
    state_id_map[feature["properties"]["ADMIN"]] = feature["id"]    
    
    
# analyse saisonnière

data_world_event = df.groupby("Year")["Year"].count().to_frame()
data_world_event["pct_change"] = data_world_event["Year"].pct_change(20).fillna(0)
data_world_event = data_world_event.loc[1970:, :]
data_world_event['ews'] = data_world_event['Year'].ewm(span=10, adjust=False).mean()
data_world_event['ma'] = data_world_event['Year'].transform(lambda x: x.rolling(1, 1).mean())
data_world_event['cumsum'] = data_world_event['Year'].cumsum()
data_world_event = data_world_event.rename(columns={"Year": "number"}).reset_index()

data_period_count = df.groupby(["Year", "Start Month"]).size().reset_index().rename(columns={0: "count"})

data_period_count['Month_abb'] = data_period_count['Start Month'] \
                                 .apply(lambda x: pd.to_datetime(x, format='%m').strftime('%b'))
                                 
data_period_count['Month'] = data_period_count['Start Month'].apply(lambda x: pd.to_datetime(x, format='%m').month_name())
data_period_count = data_period_count.set_index("Year")
data_period_count = data_period_count.loc[1970:, :].reset_index()

data_period_count_pivot = data_period_count.pivot_table( index="Year", columns="Month", values="count")
month_data = data_period_count_pivot.sum().to_frame().rename(columns={0: "value"}).reset_index()


path = "data/hadcrut-surface-temperature-anomaly.csv"
temp_country_data = pd.read_csv(path)

file_path = '/Users/new/Dash_App/data/graph.txt'
df_temp_anomaly = pd.read_csv(file_path, skiprows=4, delim_whitespace=True, names=[
                              'Year', 'No_Smoothing', 'Lowess'])
df_temp_anomaly.dropna(inplace=True)
df_temp_anomaly["Year"] = df_temp_anomaly["Year"].astype(int)

l2 = ["Canada", "Colombia", "China", "France", "Germany", "India", "Iran", "Mali",
      'United Kingdom', 'United States', "Russia", "Egypt", "Saudi Arabia", "Spain",
      "Uzbekistan", "Somalia", "Algeria", "Turkey"]

temp_country_data = pd.read_csv(path)


list_continent = list(df["Continent"].unique())
list_region = list(df["Region"].unique())
list_category = list(df["Disaster Subgroup"].unique())
list_group = list(df["Disaster Type"].unique())
list_type = list(df["Disaster Subtype"].unique())
list_type.remove(list_type[4])


list_casualties = ["Total Deaths", "No Injured", "Total Affected", "Total Damages ('000 US$)", "No Homeless"]


idps_path = "data/IDMC_GIDD_Disasters_Internal_Displacement_Data (1).xlsx"
idps_data_raw = pd.read_excel(idps_path)
idps_data_raw['Month'] = idps_data_raw['Date of Event (start)'].apply(lambda x: pd.to_datetime(x, format='%m').month_name())

path_land_ocean = "data/land_ocean.csv"