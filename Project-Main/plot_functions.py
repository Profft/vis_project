## Imports

import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

from cfg import Data, states_geojson, Data_dummy, null_graph, choose_state_graph

method_color_discrete_map = {'Firing Squad': '#1b9e77', 'Electrocution': '#7570b3', 'Gas': '#e7298a',
                             'Lethal Injection': '#66a61e', 'Hanging': '#e6ab02'}
gender_color_discrete_map = {'Male': '#15617b', 'Female': '#d47100'}
transparent = "rgba(0,0,0,0)"
darker = "rgba(0,0,0,0.19)"

# Graph Colors
inside_graph_color = darker
inside_txt_color = "green"
outside_txt_color = "#686a6d"
axis_txt_color = "pink"

# Legend Colors
legend_font_color = "white"
legend_bg = "rgba(0,0,0,0.6)"

# Line Chart Style

graph_style01 = dict(
    paper_bgcolor=transparent,
    plot_bgcolor=transparent,
    dragmode=False,
)

xaxis_style01 = dict(
    showline=False,
    gridcolor=inside_graph_color,
    zeroline=False,
    tickfont=dict(color=outside_txt_color),
    title_font=dict(color=outside_txt_color)
)

yaxis_style01 = dict(
    showline=False,
    linewidth=4,
    linecolor='black',
    gridcolor=inside_graph_color,
    tickfont=dict(color=outside_txt_color),
    title_font=dict(color=outside_txt_color),
    title_standoff=0,
    tickangle=-90
)

legend_style01 = dict(
    legend_font=dict(color=legend_font_color),
    legend=dict(bgcolor=legend_bg, title="")
)

# Map Style

map_style01 = dict(
    hoverlabel_align="auto",
    hoverlabel_bgcolor="#fff",
    hoverlabel_bordercolor="#000",
    paper_bgcolor="rgba(0,0,0,0)",
    geo=dict(bgcolor=transparent, lakecolor=transparent, landcolor=darker, subunitcolor=inside_graph_color)
)

# Table Style

table_header_bgcolor = "Orange"
table_cell_bgcolor = "LightBlue"

# https://plotly.com/python/reference/table/#table
table_style01 = dict(
    header=dict(
        align="center",
        fill_color=table_header_bgcolor,
        height=35,
    ),
    cells=dict(
        align="center",
        fill_color=table_cell_bgcolor,
        height=30,
    ),

)


## Aux Functions
def set_globals(set_year_var, accumulating_var):
    global accumulating
    if accumulating_var == [1]:
        accumulating = True
    else:
        accumulating = False
    global set_year
    set_year = set_year_var


def filter_out(filter_out_list):
    df = Data.copy()
    # Remove rows that match the filters
    for element in filter_out_list:
        df = df.drop(element, axis=1)
    # Remove years (taking into account if accu)
    if accumulating == True:
        df = df[df["Execution Year"] <= set_year]
    else:
        df = df[df["Execution Year"] == set_year]
    return df

def filter_out_w_past(filter_out_list):
    df = Data.copy()
    # Remove rows that match the filters
    for element in filter_out_list:
        df = df.drop(element, axis=1)
        df = df[df["Execution Year"] <= set_year]
    return df

def user_filters(df, filter_gender, filter_race, filter_methods):
    df = df[df['Sex'].isin(filter_gender)]
    df = df[df['Race'].isin(filter_race)]
    df = df[df['Execution Method'].isin(filter_methods)]
    return df


######################################
#
#        Overview Plots & Data
#
######################################

def overview_map(filter_gender, filter_race, filter_methods):
    print("Running.. overview_map")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    # Count executions and put into new col.
    df = df["State"].value_counts().rename_axis('State').reset_index(name='Executions')
    # Remove states with no executions.
    df = df[df["Executions"] != 0]
    # Log() execution kills
    df["log_Executions"] = np.log(df["Executions"])
    # Make sure it's never "empty" to avoid errors.
    if df.empty:
        df_gen = pd.DataFrame([[None, 0, 0]], columns=["State", "Executions", "log_Executions"])
        df = df_gen.copy()

    # Create new Map
    # https://plotly.com/python/reference/choropleth/
    fig = px.choropleth(
        data_frame=df,
        geojson=states_geojson,
        color="log_Executions",
        locations="State",
        scope="usa",
        featureidkey="properties.name",
        color_continuous_scale=px.colors.sequential.Redor,
        center={"lat": 38.856820, "lon": -101.636240},
        hover_name="State",
        hover_data={'Executions': True, 'State': False, 'log_Executions': False, }

    )
    fig.update(layout_coloraxis_showscale=False)
    # Hover Design
    fig.update_layout(map_style01)
    # Map Design
    fig.update_layout(
        margin_autoexpand=True,
        margin=dict(l=0, r=0, t=0, b=0),
        clickmode='event',
    )

    return fig


def overview_plot01(filter_gender, filter_race, filter_methods):
    #   Figure 01 - Line Chart when Accu, Plot bar when not.
    print("Running.. overview_plot01")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    df = user_filters(df, filter_gender, filter_race, filter_methods)

    df = df[["Execution Method", "Execution Year"]].value_counts().rename_axis(
        ["Execution Method", "Execution Year"]).reset_index(name='Executions')
    df = df.sort_values("Execution Year")

    if accumulating:
        fig = px.line(
            data_frame=df,
            x="Execution Year",
            y="Executions",
            color="Execution Method",
            color_discrete_map=method_color_discrete_map,
            markers=True, )
        color_discrete_map = {
            "Firing Squad": "red",
            "Electrocution": "#147852",
        }
        fig.update_layout(height=320, margin=dict(l=40, r=10, t=0, b=0),
                            legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05))
        fig.update_layout(graph_style01)
        fig.update_xaxes(xaxis_style01)
        fig.update_yaxes(yaxis_style01)
        fig.update_layout(legend_style01)
        fig.update_xaxes(title="")
    else:
        fig = px.bar(
            data_frame=df,
            x="Execution Method",
            y="Executions",
            color="Execution Method",
            color_discrete_map=method_color_discrete_map,
        )
        fig.update_layout(graph_style01)
        fig.update_xaxes(xaxis_style01)
        fig.update_yaxes(yaxis_style01)
        fig.update_layout(height=320, bargap=0.2, margin=dict(l=40, r=1, t=0, b=0), paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)', showlegend=False)

    if df.empty:
        return null_graph
    return fig


######################################
#
#        State Plots & Data
#
######################################

def state_zoom(state_name, filter_gender, filter_race, filter_methods,):
    print("Running.. state_zoom")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    #Run filters
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    # Count executions and put into new col.
    df = df["State"].value_counts().rename_axis('State').reset_index(name='Executions')
    # Remove states with no executions.
    df = df[df["Executions"] != 0]
    # Log execution kills
    df["log_Executions"] = np.log(df["Executions"])

    # Removing all state names to normalize colors on heatmap
    # Get index of selected state
    df_temp01 = df.loc[df.loc[df.State == state_name, 'State'].index.values]
    if df_temp01.empty:
        df_temp01 = pd.DataFrame([[state_name, 0, 0]], columns=["State", "Executions", "log_Executions"])
        df = df_temp01
        # Create new Map
        # https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html
        fig = px.choropleth(
            data_frame=df,
            geojson=states_geojson,
            color="log_Executions",
            locations="State",
            scope="usa",
            featureidkey="properties.name",
            color_continuous_scale=px.colors.sequential.Greys,
            hover_name="State",
            hover_data={'Executions': False, 'State': False, 'log_Executions': False},

        )
        fig.update(layout_coloraxis_showscale=False)
        # Hover Design
        fig.update_layout(map_style01)
        # Map Design
        fig.update_layout(
            margin_autoexpand=True,
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig.update_geos(fitbounds="locations")
    else:
        i = df[(df.State == state_name)].index
        # Remove from main df
        df.drop(i)
        # Set all other states to None.
        df = df.assign(State=None)
        # Add state back, now as the only name.
        df = df.append(df_temp01)
        # Create new Map
        # https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html
        fig = px.choropleth(
            data_frame=df,
            geojson=states_geojson,
            color="log_Executions",
            locations="State",
            scope="usa",
            featureidkey="properties.name",
            color_continuous_scale=px.colors.sequential.Redor,
            center={"lat": 38.856820, "lon": -101.636240},
            hover_name="State",
            hover_data={'Executions': False, 'State': False, 'log_Executions': False}

        )
        fig.update(layout_coloraxis_showscale=False)
        # Hover Design
        fig.update_layout(map_style01)
        # Map Design
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
        )
        fig.update_geos(fitbounds="locations")

    return fig


def exec_counter(filter_gender, filter_race, filter_methods, state_name):
    print("Running.. exec_counter")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    if state_name != None:
        df = df[df['State'] == state_name]
    # Remove Methods with no executions.
    df = df[df["Sex"] != 0]
    amount = int(len(df.index))

    return amount


def execute_list(filter_gender, filter_race, filter_methods, state_name):
    print("Running.. execute_list")

    # Create new dataframe
    filter_out_list = []
    df = filter_out(filter_out_list)
    if state_name != None:
        df = df[df['State'] == state_name]
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    # Create new columns
    df["Name"] = df["First Name"] + " " + df["Last Name"]
    # col_list for table (Data that is shown)
    # Data["Execution Method"] = Data["Execution Method"].astype("str")
    col_header = ("Execution Year", "Execution Method", "Name", "Sex", "Race", "Number of Victims",)
    # Rearrange
    df = df[["Execution Year", "Execution Method", "Name", "Sex", "Race", "Number of Victims"]]
    # https://plotly.com/python/table/
    for cols in df:
        if cols not in col_header:
            df = df.drop(cols, axis=1)

    table = dbc.Table.from_dataframe(df=df,
                                     striped=True,
                                     bordered=True,
                                     hover=True
                                     )

    return table


def state_plot01(filter_gender, filter_race, filter_methods, state_name):
    print("Running.. state_plot01")
    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    if state_name != None:
        df = df[df['State'] == state_name]
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    df = df[["Race", "Sex"]].value_counts().rename_axis(["Race", "Sex"]).reset_index(name='Executions')
    # Remove Methods with no executions.
    df = df[df["Sex"] != 0]

    fig = px.bar(
        data_frame=df,
        x="Race",
        y="Executions",
        color="Sex",
        color_discrete_map=gender_color_discrete_map,
    )
    fig.update_layout(graph_style01)
    fig.update_xaxes(xaxis_style01)
    fig.update_yaxes(yaxis_style01)
    fig.update_layout(height=273, margin=dict(l=40, r=10, t=0, b=0))
    # https://plotly.com/python/reference/layout/#layout-showlegend
    fig.update_layout(legend=dict(yanchor="bottom",
                                    y=0.7,
                                    xanchor="right",
                                    x=1,
                                    title="",
                                    bgcolor=legend_bg),
                        legend_font=dict(color=legend_font_color))
    fig.update_xaxes(title="")
    # https://plotly.com/python/reference/layout/yaxis/


    if df.empty:
        return null_graph
    return fig


def state_plot02(filter_gender, filter_race, filter_methods, state_name):
    #   Figure 01 - Line Chart when Accu, Plot bar when not.
    print("Running.. state_plot02")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]
    df = filter_out(filter_out_list)
    df = df[df['State'] == state_name]
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    df = df[["Execution Method"]].value_counts().rename_axis(["Execution Method"]).reset_index(
        name='Executions')
    # Remove Methods with no executions.
    df = df[df["Executions"] != 0]
    # Create Pie Chart
    # https://plotly.com/python-api-reference/generated/plotly.express.line
    fig = px.pie(
        data_frame=df,
        names="Execution Method",
        values="Executions",
        color="Execution Method",
        color_discrete_map=method_color_discrete_map,
    )
    fig.update_layout(graph_style01)
    fig.update_xaxes(xaxis_style01)
    fig.update_yaxes(yaxis_style01)
    fig.update_layout(height=230, margin=dict(l=10, r=10, t=0, b=50),
                        legend_font=dict(color=legend_font_color),
                        legend=dict(bgcolor=legend_bg, yanchor="bottom", y=1, xanchor="center", x=1))

    if df.empty:
        return null_graph
    return fig

def state_plot03(filter_gender, filter_race, filter_methods, state_name):
    print("Running.. state_plot03")

    # Create new dataframe
    filter_out_list = ["Execution#", "First Name", "Last Name", "Middle Name(s)", "Suffix", "Foreign National",
                       "Execution Volunteer", "Number of Victims", "Number of White Male Victims",
                       "Number of Black Male Victims", "Number of Latino Male Victims", "Number of Asian Male Victims",
                       "Number of Native American Male Victims", "Number of Other Race Male Victims",
                       "Number of White Female Victims", "Number of Black Female Victims",
                       "Number of Latino Female Victims", "Number of Asian Female Victims",
                       "Number of Native American Female Victims", "Number of Other Race Female Victims"]

    df = filter_out_w_past(filter_out_list)
    if state_name != None:
        df = df[df['State'] == state_name]
    df = user_filters(df, filter_gender, filter_race, filter_methods)
    df = df[["Execution Year"]].value_counts().rename_axis(["Execution Year"]).reset_index(name='Executions')
    # Add years without executions as 0.
    df_zeroYears = pd.DataFrame({'Execution Year': range(1977, set_year),
                                 'Executions': 0})
    df = (
        df.merge(df_zeroYears,
                 on=['Execution Year'],
                 how='right',
                 indicator=False)
    )
    # Merge is a mess, rebuild Dataframe to specifications.
    df = df.drop("Executions_y", axis=1)
    df = df.rename(columns={"Executions_x": "Executions"})
    df["Executions"] = df["Executions"].fillna(0.0)
    df["Executions"] = df["Executions"].astype(int)
    df = df.sort_values("Execution Year")

    fig = px.line(
        data_frame=df,
        x="Execution Year",
        y="Executions",
        markers=True,
    )
    fig.update_layout(graph_style01)
    fig.update_xaxes(xaxis_style01)
    fig.update_yaxes(yaxis_style01)
    fig.update_layout(height=250, margin=dict(l=40, r=10, t=0, b=0))
    fig.update_xaxes(title="")

    if df.empty:
        return null_graph
    return fig


