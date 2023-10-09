import streamlit as st

from incident_reporting.external.google_nbd import GoogleNBD


def get_spreadsheet():
    df = GoogleNBD().get_last_year_of_incidents()
    st.dataframe(df.to_pandas(), hide_index=True)
