## Data Import and Transformation

import pandas as pd
import json
from urllib.request import urlopen
from plotly.validator_cache import ValidatorCache
from plotly.graph_objects import Layout

# Execution Data
Data = pd.read_csv('DPIC Execution Database - U.S. Executions.csv', encoding='utf-8', sep=',')

# Convert columns to correct types
Data = Data.rename(columns={"Execution Date": "Execution Year"})
Data["Execution Year"] = pd.DatetimeIndex(Data['Execution Year']).year
Data["Suffix"] = Data["Suffix"].astype("category")
Data.loc[(Data.Race == 'American Indian or Alaska Native'),'Race']='Other Race'
Data.loc[(Data.Race == 'Other Race'),'Race']='Other'
Data["Race"] = Data["Race"].astype("category")
Data["Sex"] = Data["Sex"].astype("category")
Data["State"] = Data["State"].astype("category")
Data["County"] = Data["County"].astype("category")
Data["Foreign National"] = Data["Foreign National"].astype("category")
Data["Execution Method"] = Data["Execution Method"].astype("category")
Data["Execution Volunteer"] = Data["Execution Volunteer"].astype("category")

Data_dummy  = {'ERROR': ["You", "NOT"], 'ERROR': ["Should", "see this"]}
Data_dummy = pd.DataFrame(data=Data_dummy)

# Data = Data.drop("Region", axis=1)
# Data = Data.drop("County", axis=1)


# State FIPS Data
with urlopen(
        'https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
    states_geojson = json.load(response)

#"No data availiable" Graph
null_graph = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "height": "250",
        "annotations": [
            {
                "text": "No data for <br> selected period",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}

#n1.update_layout(height=250, margin=dict(l=40, r=10, t=0, b=0))

#"Shown before state is chosen" Graph
choose_state_graph = {
    "layout": {
        "xaxis": {
            "visible": False
        },
        "yaxis": {
            "visible": False
        },
        "height": "250",
        "valign": "middle",
        "margin": dict(l=0, r=0, t=0, b=35),
        "annotations": [
            {
                "text": "Choose a state",
                "xref": "paper",
                "yref": "paper",
                "yanchor": "middle",
                "xanchor": "middle",
                "showarrow": False,
                "font": {
                    "size": 28
                }
            }
        ]
    }
}