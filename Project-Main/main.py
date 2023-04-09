## Imports

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

from plot_functions import *
from cfg import Data, Data_dummy, null_graph, choose_state_graph
import time

## Links

# https://dash-bootstrap-components.opensource.faculty.ai/

# https://plotly.com/python/

# How to fix rows with different heights:
# https://github.com/facultyai/dash-bootstrap-components/issues/286

# LEGEND styling (All Plots)
# https://plotly.com/python/legend/

# All Plotly charts docus
# https://plotly.com/python-api-reference/plotly.express.html
## CSS

# styling the navbar
NAVBAR_STYLE = {
    "position": "fixed",
    "bottom": 0,
    "width": "100%",
    "padding": "1rem 1rem",
    "background-color": "#f8f9fa",
    "z-index": "2000",
    "height": "100px",
    "border-top": "1px solid rgba(0,0,0,.125)",
}
PIP_STYLE = {
    "position": "relative",
    "bottom": 215,
    "width": "20%",
    "padding": "1rem 1rem",
    "z-index": "2000",
    "height": "100px",
}



## Dash
# Init the app
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY,
                                      "assets/custom.css",
                                      "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap"])

# Main filters (NavBar)
navbar = html.Div(
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Interval(id="animate", disabled=True),
                    dcc.Slider(
                        id="filter_slct_year",
                        min=1977,
                        max=2021,
                        step=1,
                        value=2005,
                        included=False,
                        tooltip={"placement": "top", "always_visible": True},
                        marks={
                            1977: "1977",
                            1980: "1980",
                            1990: "1990",
                            2000: "2000",
                            2010: "2010",
                            2021: "2021"}
                    ), ]
                , md=10),
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Button("Play", id="play", color="primary", className="me-1", outline=True,
                                           n_clicks=0)
                                , md=3),
                            dbc.Col(
                                html.Div(dbc.Checklist(
                                    options=[
                                        {"label": "Accumulate Years", "value": 1},
                                    ],
                                    value=[1],
                                    id="filter_slct_year_acc",
                                    switch=True,
                                ), style={"margin-top": "7px"}, ), md=9),
                        ]),
                ]
                , md=2),
        ],
        align="center",
    ),
    style=NAVBAR_STYLE,
)

# Overview Components (sidebar)
# Sidebar has the components that filter the map, as well as plots.
# First, we declare each individual plot as a variable.

overview_method_filters = html.Div(dbc.Card(
    [
        dbc.CardHeader("Filters", style={"text-align": "left"}),
        dbc.CardBody(
            [
                html.H6("Gender"),
                dbc.Checklist(
                    options=[
                        {'label': 'Male', 'value': 'Male'},
                        {'label': 'Female', 'value': 'Female'},
                    ],
                    value=['Male', 'Female'],
                    id="filter_gender",
                    inline=True,
                    switch=True
                ),
                html.H6("Race"),
                dbc.Checklist(
                    options=[
                        {'label': 'Asian', 'value': 'Asian'},
                        {'label': 'Black', 'value': 'Black'},
                        {'label': 'Latino', 'value': 'Latino'},
                        {'label': 'White', 'value': 'White'},
                        {'label': 'Other', 'value': 'Other'}
                    ],
                    value=['Asian', 'Black', "Latino", "White", "Other"],
                    id="filter_race",
                    inline=True,
                    switch=True
                ),
                html.H6("Execution Methods"),
                dbc.Checklist(
                    options=[
                        {'label': 'Firing Squad', 'value': 'Firing Squad'},
                        {'label': 'Electrocution', 'value': 'Electrocution'},
                        {'label': 'Gas', 'value': 'Gas'},
                        {'label': 'Hanging', 'value': 'Hanging'},
                        {'label': 'Lethal Injection', 'value': 'Lethal Injection'}
                    ],
                    value=['Firing Squad', 'Electrocution', "Gas", "Hanging", "Lethal Injection"],
                    id="filter_methods",
                    inline=True,
                    switch=True
                ),
            ]
        , style={"padding":"0rem 1rem 1rem 1rem"})
    ],
    style={"margin-top": "15px"}))

overview_sidebar_plot_01 = html.Div(dbc.Card(
    [
        dbc.CardHeader(id="nationalTitle", style={"text-align": "left"}),
        dbc.CardBody(
            dcc.Graph(
                id="overview_sidebar_plot_01", figure={},
                style={'width="100%", margin': 'auto auto'},
            ))
    ],
    style={"margin-top": "15px"}))

# State Components (sidebar)

state_map = html.Div(dcc.Graph(
                id="state_map", figure={},
                style={'width="100%", margin': 'auto auto'},
            ), id="pip_map", style=PIP_STYLE, hidden=True)


# Overview Components (Data)
# Has a graph map, year slider and accumulation activator.
overview_data = html.Div(
    [
        dbc.CardBody(dcc.Graph(id="execution_map", figure={}, style={'width': '100%', 'margin': 'auto auto'}, )),
        state_map
        ]
    )


# State Components (Data)
state_data_plot_01 = html.Div(dbc.Card(
    [
        dbc.CardHeader(id="stateRacialDataTitle", style={"text-align": "left"}),
        dbc.CardBody(
            dcc.Graph(
                id="state_data_plot_01", figure={},
                style={'width="100%", margin': 'auto auto'},
            ))
    ],
    style={"margin-top": "15px"}))

state_data_plot_02 = html.Div(dbc.Card(
    [
        dbc.CardHeader(id="stateMethodDataTitle", style={"text-align": "left"}),
        dbc.CardBody(
            dcc.Graph(
                id="state_data_plot_02", figure={},
                style={'width="100%", margin': 'auto auto'},
            ))
    ],
    style={"margin-top": "15px"}))

state_data_plot_03 = html.Div(dbc.Card(
    [
        dbc.CardHeader(id="stateTimelineTitle", style={"text-align": "left"}),
        dbc.CardBody(
            dcc.Graph(
                id="state_data_plot_03", figure={},
                style={'width="100%", margin': 'auto auto'},
            ))
    ],
    style={"margin-top": "15px"}))

state_data_list_table = html.Div(dbc.Card(
    [
        dbc.CardHeader(id="stateListDataTitle", style={"text-align": "left"}),
        dbc.CardBody(id="state_data_list02", style={"padding":"0px"})
    ],
    style={"margin-top": "15px", "max-height":"720px", "overflow":"auto"},))

# Layout :
# (Third), Layout adds the variables with the section parts ("sidebar"/"data") into an HTML page.
# For layout (dbc) see documentation:
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/

app.layout = dbc.Container(
    [
        navbar,
        # Overview Section
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader(html.H3("Executions in the United States", className="card-title",
                                                   style={"text-align": "left"})),
                            overview_data,
                        ]
                        , style={"margin-top": "15px", "min-height":"670px"}) ,align="start", md=8),
                dbc.Col(
                    [
                        overview_method_filters,
                        overview_sidebar_plot_01,
                    ]
                    , align="start", md=4),
            ],
            align="center",
        ),
        # State Section
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        [
                        dbc.Row(
                            [
                                dbc.Col(state_data_plot_01, md=8, align="start"),
                                dbc.Col(state_data_plot_02, md=4, align="start"),
                            ]
                        ),
                        dbc.Row(
                            dbc.Col(state_data_plot_03, md=12, align="start")
                        )
                        ]
                    , md=6),
                    dbc.Col(state_data_list_table, align="start", md=6)
                ],
                align="center",
            ),
            hidden=False,
            id="state_sidebar",
        ),
    ],
    fluid=True,
    style={"margin-bottom": "120px"}
)


## Animate Year


@app.callback(
    Output("filter_slct_year", "value"),
    [
        Input("animate", "n_intervals"),
        Input("filter_slct_year", "value"),
    ],
    prevent_initial_call=True,
)
def update_figure(n, selected_year):
    if n:
        years = range(1977, 2022, 1)
        index = years.index(selected_year)
        index = (index + 1) % len(years)
        year = years[index]
    else:
        year = selected_year
    return year


@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing


## Update Overview
@app.callback(
    [
        Output(component_id="execution_map", component_property="figure"),
        Output(component_id="overview_sidebar_plot_01", component_property="figure"),
    ],
    [
        Input(component_id="filter_slct_year", component_property="value"),
        Input(component_id="filter_slct_year_acc", component_property="value"),
        Input(component_id="filter_gender", component_property="value"),
        Input(component_id="filter_race", component_property="value"),
        Input(component_id="filter_methods", component_property="value"),

    ]
)
def overview_update(filter_slct_year, filter_slct_year_acc, filter_gender, filter_race, filter_methods,):
    set_globals(filter_slct_year, filter_slct_year_acc)

    return overview_map(filter_gender, filter_race, filter_methods), \
           overview_plot01(filter_gender, filter_race, filter_methods,)


## Update State view
@app.callback(
    [
        Output(component_id="state_data_plot_01", component_property="figure"),
        Output(component_id="state_data_plot_02", component_property="figure"),
        Output(component_id="state_data_plot_03", component_property="figure"),
        Output(component_id="state_data_list02", component_property="children"),
        Output(component_id="pip_map", component_property="hidden"),
        Output(component_id="state_sidebar", component_property="hidden"),
        Output(component_id="state_map", component_property="figure"),
        Output(component_id="stateRacialDataTitle", component_property="children"),
        Output(component_id="stateMethodDataTitle", component_property="children"),
        Output(component_id="stateTimelineTitle", component_property="children"),
        Output(component_id="stateListDataTitle", component_property="children"),

    ],
    [
        Input(component_id="execution_map", component_property="clickData"),
        Input(component_id="filter_gender", component_property="value"),
        Input(component_id="filter_race", component_property="value"),
        Input(component_id="filter_methods", component_property="value"),
        Input(component_id="filter_slct_year", component_property="value"),
        Input(component_id="filter_slct_year_acc", component_property="value"),
    ],
    prevent_initial_call=False,
)
def update_state_view(clickData, filter_gender, filter_race, filter_methods, filter_slct_year, filter_slct_year_acc):
    h_time = ["Error"]
    if clickData:
        set_globals(filter_slct_year, filter_slct_year_acc)
        clickData_state = clickData["points"][0]['location']
        map = state_zoom(clickData_state, filter_gender, filter_race, filter_methods)

        # Title Stuff
        num_exec = exec_counter(filter_gender, filter_race, filter_methods, clickData_state)
        if filter_slct_year_acc == [1]:
            h_Racial = f"Racial/Gender Distribution of Executions from 1977 - {filter_slct_year}"
            h_Method = f"Distribution of Execution Methods from 1977 - {filter_slct_year}"
            h_list = f"{num_exec} Executions from 1977 - {filter_slct_year}"
        else:
            h_Racial = f"Racial/Gender Distribution of Executions in {filter_slct_year}"
            h_Method = f"Distribution of Execution Methods in {filter_slct_year}"
            h_list = f"{num_exec} Executions in {filter_slct_year}"
        h_Racial = h_Racial + " in " + clickData["points"][0]['location']
        h_Method = h_Method + " in " + clickData["points"][0]['location']
        h_list = h_list + " in " + clickData["points"][0]['location']
        h_timeline = f"Executions per Year (1977 - {filter_slct_year}) in " + clickData["points"][0]['location']

        return state_plot01(filter_gender, filter_race, filter_methods, clickData_state), \
               state_plot02(filter_gender, filter_race, filter_methods, clickData_state), \
               state_plot03(filter_gender, filter_race, filter_methods, clickData_state), \
               execute_list(filter_gender, filter_race, filter_methods, clickData_state), False, False, map, h_Racial, h_Method, h_timeline, h_list
    else:
        h_none = ""
        list_null = "Choose a state to view executions"

        # Title Stuff
        num_exec = exec_counter(filter_gender, filter_race, filter_methods, None)
        if filter_slct_year_acc == [1]:
            h_Racial = f"Racial/Gender Distribution of Executions from 1977 - {filter_slct_year}"
            h_Method = f"Distribution of Execution Methods from 1977 - {filter_slct_year}"
            h_list = f"{num_exec} Executions from 1977 - {filter_slct_year}"
        else:
            h_Racial = f"Racial/Gender Distribution of Executions in {filter_slct_year}"
            h_Method = f"Distribution of Execution Methods in {filter_slct_year}"
            h_list = f"{num_exec} Executions in {filter_slct_year}"
        h_Racial = h_Racial + "  in the United States of America"
        h_Method = h_Method + "  in the United States of America"
        h_list = h_list + "  in the United States of America"
        h_timeline = f"Executions per Year (1977 - {filter_slct_year}) in the United States of America"

        return state_plot01(filter_gender, filter_race, filter_methods, None),\
               choose_state_graph, \
               state_plot03(filter_gender, filter_race, filter_methods, None), \
               execute_list(filter_gender, filter_race, filter_methods, None),\
               True, False, null_graph, h_Racial, list_null, h_timeline, h_list


## Update Titles

@app.callback(
    [
        Output(component_id="nationalTitle", component_property="children")
    ],
    [
        Input(component_id="execution_map", component_property="clickData"),
        Input(component_id="filter_slct_year", component_property="value"),
        Input(component_id="filter_slct_year_acc", component_property="value"),
    ]
)
def update_main_title(clickData, filter_slct_year, filter_slct_year_acc):
    h_time = ["Error"]
    if filter_slct_year_acc == [1]:
        h_time = f"Executions from 1977 - {filter_slct_year} in the USA"
    else:
        h_time = f"Executions in {filter_slct_year} in the USA"

    h_time = [h_time]

    return h_time


## Start Server
if __name__ == '__main__':
    app.run_server(debug=True)
