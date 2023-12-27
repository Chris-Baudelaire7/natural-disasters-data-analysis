mapbox_access_token = 'pk.eyJ1IjoiY2hyaXMtYmF1ZGVsYWlyZSIsImEiOiJjbGcybmhodXEwNzdtM2pvMWwyenV3bThnIn0.vgHUnOS_pSiOWwQOeXsFbA'

wrong_countries_name = [
    'Bolivia (Plurinational State of)', 'Brunei Darussalam', 'Cabo Verde', 'Comoros (the)', 'Hong Kong', 'Macedonia (the former Yugoslav Republic of)', 'Cayman Islands (the)', 'Czech Republic (the)',  'Congo (the Democratic Republic of the)', 'Dominican Republic (the)', 'Cook Islands (the)', 'Côte d’Ivoire',  'Gambia (the)',  'Guinea-Bissau',  'Iran (Islamic Republic of)', 'Micronesia (Federated States of)', 'Niger (the)', 'Philippines (the)', 'Serbia', 'Russian Federation (the)', 'Congo (the Democratic Republic of the)', 'Sudan (the)', 'Syrian Arab Republic', 'United States of America (the)', 'United Arab Emirates (the)', 'United Kingdom of Great Britain and Northern Ireland (the)', 'Venezuela (Bolivarian Republic of)', 'Viet Nam', 'Taiwan (Province of China)', 'Bahamas (the)', 'Netherlands (the)', 'Tanzania, United Republic of', 'Congo (the)', "Lao People's Democratic Republic (the)", "Germany Dem Rep", "Moldova (the Republic of)", "Korea (the Democratic People's Republic of)", 'Korea (the Republic of)'
]

right_countries_name = [
    "Bolivia", "Brunei", "Cape Verde", "Comoros", "Hong Kong S.A.R.", "Macedonia",  "Cayman Islands", "Czech Republic", "Democratic Republicof the Congo", "Dominican Republic", "Cook Islands", "Ivory Coast", "Gambia", "Guinea Bissau", "Iran", "Federated States of Micronesia", "Niger", "Philippines", "Republic of Serbia", "Russia", "Democratic Republic of the Congo", "Sudan", "Syria", "United States of America", "United Arab Emirates", "United Kingdom", "Venezuela", "Vietnam", "Taiwan", "The Bahamas", "Netherlands", "United Republic of Tanzania", "Republic of Congo", "Laos", "Germany", "Moldova", "North Korea", "South Korea"
]



saison_mapping = {
    12: 'Winter',
    1: 'Winter',
    2: 'Winter',
    3: 'Spring',
    4: 'Spring',
    5: 'Spring',
    6: 'Summer',
    7: 'Summer',
    8: 'Summer',
    9: 'Autumn',
    10: 'Autumn',
    11: 'Autumn'
}

update_layout_geo = {
    "geo": dict(
        showframe=False,
        showcoastlines=False,
        showlakes=False,
        bgcolor="rgba(0,0,0,0)",
        resolution=50,
        showcountries=False,
        projection=dict(type='natural earth'),

        lonaxis=dict(
            showgrid=True,
            gridcolor='rgb(40, 40, 40)',
            gridwidth=0.2,
            range=[-135, 155]
        ),
        lataxis=dict(
            showgrid=True,
            gridcolor='rgb(40, 40, 40)',
            gridwidth=0.2,
            range=[-55, 73]
        )

    )
}

contours = {
    "end": 4,
    "showlines": False,
    "size": 0.5,
    "start": -4
}

colorbar = {
    "borderwidth": 0,
    "outlinewidth": 0,
    "thickness": 15,
    "tickfont": {"size": 14},
    "title": "°C"
}

axis_style = dict(
    zeroline=False,
    showline=False,
    showgrid=False,
    ticks='',
    showticklabels=False,
)

