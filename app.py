"""Serves as the entry point for the project module."""
import streamlit as st

from incident_reporting.pages.map import get_map
from incident_reporting.pages.table import get_spreadsheet
from incident_reporting.pages.time_histogram import get_time_histogram


def introduction():
    st.write("# UCPD Incident Tracking")
    st.markdown(
        """
        This project was undertaken with the goal of showing a more granular
        picture of incidents are posted on the
        [UCPD Incident Report](https://incidentreports.uchicago.edu/) page.

        The code for this project is stored in two places:
        - The UCPD incident web-scraper:
            [Link](https://github.com/michplunkett/ucpd-incident-scraper)
        - The Starlit application for data display:
            [Link](https://github.com/michplunkett/ucpd-incident-reporting)

        For more information on this project, or any inquiries related to the
        author, please reach out to me over email at
        **michplunkett[at]gmail[dot]com**.
    """
    )


page_names_to_funcs = {
    "—": introduction,
    "Map of the Last 90 Days": get_map,
    "Spreadsheet of the last 365 Days": get_spreadsheet,
    "Histogram of Incidents by Season": get_time_histogram,
}

demo_name = st.sidebar.selectbox("Choose a Visual", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()
