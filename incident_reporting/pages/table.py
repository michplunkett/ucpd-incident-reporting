import streamlit as st

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    INCIDENT_KEY_COMMENTS,
    INCIDENT_KEY_DISPOSITION,
    INCIDENT_KEY_ID,
    INCIDENT_KEY_REPORTED_DATE,
    INCIDENT_KEY_TYPE,
    INCIDENT_KEY_VALIDATED_ADDRESS,
)


def get_spreadsheet():
    df, incident_types = GoogleNBD().get_last_year_of_incidents()
    st.dataframe(
        df.to_pandas(),
        column_order=[
            INCIDENT_KEY_ID,
            INCIDENT_KEY_TYPE,
            INCIDENT_KEY_REPORTED_DATE,
            INCIDENT_KEY_COMMENTS,
            INCIDENT_KEY_VALIDATED_ADDRESS,
        ],
        column_config={
            INCIDENT_KEY_DISPOSITION: "Disposition",
            INCIDENT_KEY_COMMENTS: "Description",
            INCIDENT_KEY_TYPE: "Incident Category",
            INCIDENT_KEY_VALIDATED_ADDRESS: st.column_config.TextColumn(
                "Validated Address"
            ),
            INCIDENT_KEY_ID: "UCPD ID",
            INCIDENT_KEY_REPORTED_DATE: st.column_config.DateColumn(
                "Reported Date", format="YYYY-MM-DD"
            ),
        },
        hide_index=True,
    )
