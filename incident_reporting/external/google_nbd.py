"""Contains code relating to the Google Cloud Platform Datastore service."""
import json
from datetime import datetime, timedelta

import polars as pl
import streamlit as st
from google.cloud.datastore.helpers import GeoPoint
from google.cloud.ndb import Client, GeoPtProperty, Model, StringProperty
from google.oauth2 import service_account

from incident_reporting.utils.constants import (
    ENV_GCP_CREDENTIALS,
    ENV_GCP_PROJECT_ID,
    FILE_TYPE_JSON,
    INCIDENT_KEY_TYPE,
    UCPD_MDY_DATE_FORMAT,
)


# Incidents of these types have been excluded from the list for the sake of
# victim's privacy and due to the nature the incidents included in this list.
EXCLUDED_INCIDENT_TYPES = [
    "Fondling",
    "Medical Call",
    "Luring a Minor",
    "Lost Property",
    "Stalking",
    "Sexual Assault",
    "Dating",
    "Stalking",
    "Domestic",
    "Sex",
    "Found Property",
    "Mental Health",
    "Harassment by Electronic Means",
    "Well-Being",
    "Threatening Phone Call",
]


class Incident(Model):
    """Standard data structure for recovered UCPD incidents."""

    ucpd_id = StringProperty(indexed=True)
    incident = StringProperty(indexed=True)
    reported = StringProperty()
    reported_date = StringProperty(indexed=True)
    occurred = StringProperty()
    comments = StringProperty()
    disposition = StringProperty()
    location = StringProperty()
    validated_address = StringProperty()
    validated_location = GeoPtProperty()


class GoogleNBD:
    """Create the client and access GCP NBD functionality."""

    ENTITY_TYPE = "Incident"

    def __init__(self):
        if ENV_GCP_CREDENTIALS.endswith(FILE_TYPE_JSON):
            self.client = Client(ENV_GCP_PROJECT_ID)
        else:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(ENV_GCP_CREDENTIALS)
            )
            self.client = Client(
                credentials=credentials,
                project=ENV_GCP_PROJECT_ID,
            )

    @staticmethod
    def _list_to_parsed_list(unparsed_list: [str]) -> [str]:
        parsed_set = set()
        for element in unparsed_list:
            if "/" in element:
                for p in element.split("/"):
                    fmt_element = p.strip()
                    if p:
                        parsed_set.add(fmt_element.title())
            else:
                fmt_element = element.strip()
                parsed_set.add(fmt_element.title())
        return list(parsed_set)

    @staticmethod
    def _process_incidents(incidents: [Incident]) -> pl.DataFrame:
        incident_list = []
        for i in incidents:
            record = {}
            for key, value in i.to_dict().items():
                if isinstance(value, GeoPoint):
                    record[key] = [value.latitude, value.longitude]
                    continue
                record[key] = value
                incident_list.append(record)
        df = pl.DataFrame(incident_list)
        df = df.filter(
            ~pl.col(INCIDENT_KEY_TYPE).str.contains(
                "|".join(EXCLUDED_INCIDENT_TYPES)
            )
        )
        return df

    def _get_incidents_back_x_days(self, days_back: int) -> pl.DataFrame:
        with self.client.context():
            date_str = (datetime.today() - timedelta(days=days_back)).strftime(
                UCPD_MDY_DATE_FORMAT
            )
            query = (
                Incident.query(Incident.reported_date >= date_str)
                .order(-Incident.reported_date)
                .fetch()
            )
            return self._process_incidents(query)

    @st.cache_data(ttl=timedelta(days=2))
    def get_last_90_days_of_incidents(self) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(90)
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())

    @st.cache_data(ttl=timedelta(days=2))
    def get_last_year_days_of_incidents(self) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(365)
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())

    @st.cache_data(ttl=timedelta(days=2))
    def get_all_incidents(self) -> (pl.DataFrame, [str]):
        query = Incident.query().order(-Incident.reported).fetch()
        df = self._process_incidents(query)
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())
