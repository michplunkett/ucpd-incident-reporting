import dash_ag_grid as dag
from dash import html, register_page

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    KEY_COMMENTS,
    KEY_ID,
    KEY_REPORTED,
    KEY_TYPE,
    KEY_VALIDATED_ADDRESS,
    KEY_VALIDATED_LOCATION,
)


register_page(__name__)

df, categories = GoogleNBD().get_last_year_of_incidents()
df.drop_in_place(KEY_VALIDATED_LOCATION)
df = df.to_pandas()

layout = html.Div(
    [
        dag.AgGrid(
            rowData=df.to_dict("records"),
            columnDefs=[
                {"field": KEY_ID, "headerName": "ID"},
                {"field": KEY_TYPE, "headerName": "Category"},
                {
                    "field": KEY_REPORTED,
                    "headerName": "Reported Time",
                    "sortable": True,
                },
                {"field": KEY_VALIDATED_ADDRESS, "headerName": "Location"},
                {"field": KEY_COMMENTS, "headerName": "Comments"},
            ],
        )
    ]
)
