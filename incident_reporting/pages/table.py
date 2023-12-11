from dash import dash_table, register_page

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    KEY_COMMENTS,
    KEY_DISPOSITION,
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

layout = dash_table.DataTable(
    data=df.to_dict("records"),
    columns=[
        {"name": "ID", "id": KEY_ID, "type": "text"},
        {
            "name": "Reported",
            "id": KEY_REPORTED,
            "type": "datetime",
        },
        {"name": "Incident", "id": KEY_TYPE, "type": "text"},
        {"name": "Disposition", "id": KEY_DISPOSITION, "type": "text"},
        {"name": "Address", "id": KEY_VALIDATED_ADDRESS, "type": "text"},
        {"name": "Comments", "id": KEY_COMMENTS, "type": "text"},
    ],
    style_header={
        "fontWeight": "bold",
    },
    style_cell={
        "textAlign": "left",
        "font-family": "HCo_Verlag, sans-serif",
        "overflowX": "auto",
    },
    style_data={"whiteSpace": "normal", "height": "auto", "lineHeight": "15px"},
    style_cell_conditional=[
        {"if": {"column_id": KEY_ID}, "min-width": "110px"},
        {"if": {"column_id": KEY_DISPOSITION}, "min-width": "95px"},
    ],
    page_action="native",
    filter_action="native",
    filter_options={"placeholder_text": "Filter Values"},
    page_current=0,
    page_size=10,
    cell_selectable=False,
)
