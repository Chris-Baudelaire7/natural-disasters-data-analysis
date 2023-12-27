import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

from image_urls import *


def render_hovercard(hovercardTarget, hovercardDropdown):
    hovercard = dmc.HoverCard(
        className="HoverCard",
        position="bottom",
        returnFocus=True,
        closeDelay=100,
        transition="rotate-right",
        withinPortal=True,
        withArrow=False,
        shadow="xl",
        zIndex=99999,
        children=[
            dmc.HoverCardTarget(hovercardTarget),
            dmc.HoverCardDropdown(
                hovercardDropdown, unstyled=True, className="crossfilter-style")
        ])

    return hovercard



# ------------------------------------------------------------------------------

carousel_ec = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(earthquake_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_ec = dbc.Card(
    [
        carousel_ec,
        dbc.CardBody(
            [
                html.P(
                    "An earthquake – also called a quake, tremor, or temblor – is the shaking of the surface of Earth resulting from a sudden release of energy in the lithosphere that creates seismic waves. Earthquakes can range in intensity, from those that are so weak that they cannot be felt, to those violent enough to propel objects and people into the air, damage critical infrastructure, and wreak destruction across entire cities",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)



# ------------------------------------------------------------------------------------------

carousel_v = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(volcanic_activity_)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_v = dbc.Card(
    [
        carousel_v,
        dbc.CardBody(
            [
                html.P(
                    "A volcano is an opening in the earth’s surface that allows magma (hot liquid and semi-liquid rock), volcanic ash and gases to escape. They are generally found where tectonic plates come together or separate, but they can also occur in the middle of plates due to volcanic hotspots. A volcanic eruption is when gas and/or lava are released from a volcano—sometimes explosively",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)

# ------------------------------------------------------------------------------

carousel_drought = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(drought_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_drought = dbc.Card(
    [
        carousel_drought,
        dbc.CardBody(
            [
                html.P(
                    "A drought is defined as drier than normal conditions. This means that a drought is a moisture deficit relative to the average water availability at a given location and season. A drought can last for days, months or years. Drought often exerts substantial impacts on the ecosystems and agriculture ",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)

# ------------------------------------------------------------------------------

carousel_flood = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(flood_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_flood = dbc.Card(
    [
        carousel_flood,
        dbc.CardBody(
            [
                html.P(
                    "A flood is an overflow of water (or rarely other fluids) that submerges land that is usually dry.[1] In the sense of flowing water, the word may also be applied to the inflow of the tide. Floods are an area of study of the discipline hydrology and are of significant concern in agriculture, civil engineering and public health. Human changes to the environment often increase the intensity and frequency of flooding",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)

# ------------------------------------------------------------------------------

carousel_storm = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(storm_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_storm = dbc.Card(
    [
        carousel_storm,
        dbc.CardBody(
            [
                html.P(
                    "A storm is any disturbed state of the natural environment or the atmosphere of an astronomical body.[citation needed] It may be marked by significant disruptions to normal conditions such as strong wind, tornadoes, hail, thunder and lightning (a thunderstorm), heavy precipitation (snowstorm, rainstorm), heavy freezing rain (ice storm), strong winds (tropical cyclone, windstorm), wind transporting some substance through the atmosphere such as in a dust storm, among other forms of severe weather.",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)


# ------------------------------------------------------------------------------------------


carousel_wf = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(wildfire_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_wf = dbc.Card(
    [
        carousel_wf,
        dbc.CardBody(
            [
                html.P(
                    "Wildfires (also known as bushfires, brush fires or forest fires) are large, uncontrolled and potentially destructive fires that can affect both rural and urban areas. They can spread quickly, change direction and even 'jump' across large distances when embers and sparks are carried by the wind. They are caused by a range of natural causes (such as lightning) or by human carelessness (such as a discarded cigarette). The spread of a wildfire depends on the arrangement of land, available fuel (vegetation or dead wood) and weather conditions (wind and heat). They can start in just seconds and turn into infernos in a matter of minutes",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)

# ------------------------------------------------------------------------------------------------


carousel_ld = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(landslide_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_ld = dbc.Card(
    [
        carousel_ld,
        dbc.CardBody(
            [
                html.P(
                    "Landslides, also known as landslips,[1][2][3] are several forms of mass wasting that may include a wide range of ground movements, such as rockfalls, mudflows, shallow or deep-seated slope failures and debris flows.[4] Landslides occur in a variety of environments, characterized by either steep or gentle slope gradients, from mountain ranges to coastal cliffs or even underwater,[5] in which case they are called submarine landslides.",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)

# ------------------------------------------------------------------------------------------------


carousel_et = dbc.Carousel(
    items=[
        {"key": key, "src": src} for key, src in enumerate(extreme_temperature_disaster_url)
    ],
    controls=True,
    indicators=False,
    class_name="K",
)

card_et = dbc.Card(
    [
        carousel_et,
        dbc.CardBody(
            [
                html.P(
                    "A drought is defined as drier than normal conditions. This means that a drought is a moisture deficit relative to the average water availability at a given location and season. A drought can last for days, months or years. Drought often exerts substantial impacts on the ecosystems and agriculture ",
                    className="card-text",
                ),
                html.Div(className="d-flex justify-content-end", children=[
                    DashIconify(
                        icon="carbon:overflow-menu-horizontal", width=20)
                ])
            ]
        ),
    ],
    style={"width": "19rem"},
    className="card-overview",
)


header = html.Div(children=[
    
    html.Span(className="d-inline-block", children=[
        html.Span(
            "A natural disaster is the highly harmful impact on a society or community following a natural hazard event. Some examples of natural hazard events include: ", className="d-inline"
        ),
        
        html.Span(render_hovercard("Drought", card_drought), className="type"), ", ",
        html.Span(render_hovercard("Earthquake", card_ec),className="type"), ", ",
        html.Span(render_hovercard("Volcanic activity", card_v), className="type"), ", ",
        html.Span(render_hovercard("Storm", card_storm), className="type"), ", ",
        html.Span(render_hovercard("Flood", card_flood), className="type"), ", ",
        html.Span(render_hovercard("Landslide", card_ld), className="type"), ", ",
        html.Span(render_hovercard("Wildfire", card_wf), className="type"), ", ",
        html.Span(render_hovercard("Extreme temperature", card_et), className="type"), ", ",
        
        html.Span(
            "A natural disaster can cause loss of life or damage property, and typically leaves economic damage in its wake. The severity of the damage depends on the affected population's resilience and on the infrastructure available. Scholars have been saying that the term natural disaster is unsuitable and should be abandoned. Instead, the simpler term disaster could be used, while also specifying the category (or type) of hazard. A disaster is a result of a natural or human-made hazard impacting a vulnerable community. It is the combination of the hazard along with exposure of a vulnerable society that results in a disaster.. ", className="d-inline"
        ),
    ])
    
])

