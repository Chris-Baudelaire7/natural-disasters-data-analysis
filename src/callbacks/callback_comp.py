from dash import Input, Output, callback, State
from data_preparation import *
from callbacks.climate_change_and_disasters_callback.tabs import *


@callback(
    Output("positioned-toast", "is_open"),
    Input("positioned-toast-toggle", "n_clicks"),
)
def open_toast(n):
    if n:
        return True
    return False


@callback(
    Output('choice-dropdown', 'options'),
    Output('title-dropdown', 'children'),
    Input('dropdown-category', 'value'))
def set_options(selected_category):
    return [
        {'label': i, 'value': i} for i in ["All groups"] + sorted(list_category)
    ] if selected_category == "Disaster Subgroup" else \
        [
        {'label': i, 'value': i} for i in ["All types"] + sorted(list_group)
    ], selected_category


@callback(
    Output('choice-dropdown', 'value'),
    Input('choice-dropdown', 'options'))
def set_value(available_options):
    return available_options[0]['value']


@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas", "is_open"),
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@callback(
    Output("content", "children"),
    Input("tabs", "active_tab")
)
def switch_tab(at):
    if at == "heatmap":
        return heatmap_content_div
    elif at == "map":
        return map_content_div
    return html.P("This shouldn't ever be displayed...")
