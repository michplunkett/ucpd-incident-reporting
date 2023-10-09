"""Contains code relating to the Google Cloud Platform Datastore service."""
import gzip
import json
import os
from datetime import date, datetime, timedelta

import polars as pl
from google.cloud.datastore.helpers import GeoPoint
from google.cloud.ndb import Client, GeoPtProperty, Model, StringProperty
from google.oauth2 import service_account

from incident_reporting.utils.constants import (
    ENV_GCP_CREDENTIALS,
    ENV_GCP_PROJECT_ID,
    FILE_OPEN_MODE_READ,
    FILE_TYPE_JSON,
    INCIDENT_KEY_REPORTED,
    INCIDENT_KEY_REPORTED_DATE,
    INCIDENT_KEY_TYPE,
    INCIDENT_KEY_VALIDATED_LOCATION,
    TIMEZONE_CHICAGO,
    UCPD_MDY_KEY_DATE_FORMAT,
    UTC_DATE_TIME_FORMAT,
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
    "Medical Transport",
    "Warrant",
    "Lost Wallet",
    "Fire Alarm",
    "Chemical Spill",
    "Suspicious Mail",
    "Eavesdropping",
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
                        parsed_set.add(fmt_element.replace("\n", " "))
            else:
                fmt_element = element.strip()
                parsed_set.add(fmt_element.replace("\n", " "))
        return list(parsed_set)

    @staticmethod
    def _standardize_df(df: pl.DataFrame) -> pl.DataFrame:
        return df.with_columns(
            pl.col(INCIDENT_KEY_REPORTED)
            .str.strptime(pl.Datetime, format=UTC_DATE_TIME_FORMAT)
            .dt.convert_time_zone(TIMEZONE_CHICAGO),
            pl.col(INCIDENT_KEY_REPORTED_DATE).str.strptime(
                pl.Date, format=UCPD_MDY_KEY_DATE_FORMAT
            ),
            pl.col(INCIDENT_KEY_VALIDATED_LOCATION)
            .str.split(",")
            .cast(pl.List(pl.Float64)),
        )

    @staticmethod
    def _process_incidents(incidents: [Incident]) -> pl.DataFrame:
        incident_list = []
        for i in incidents:
            record = {}
            for key, value in i.to_dict().items():
                if isinstance(value, GeoPoint):
                    record[key] = f"{value.latitude},{value.longitude}"
                    continue
                record[key] = value
                incident_list.append(record)
        df = pl.DataFrame(incident_list)
        df = df.filter(
            ~pl.col(INCIDENT_KEY_TYPE).str.contains(
                "|".join(EXCLUDED_INCIDENT_TYPES)
            )
        )

        return GoogleNBD._standardize_df(df)

    @staticmethod
    def _get_stored_incidents():
        file_path = (
            os.getcwd().replace("\\", "/")
            + "/incident_reporting/data/incident_dump.csv.gz"
        )

        with gzip.open(file_path, FILE_OPEN_MODE_READ) as f:
            df = pl.read_csv(f.read())

        return df

    def _get_incidents_back_x_days(
        self, date_limit: date = None
    ) -> pl.DataFrame:
        if not date_limit:
            date_limit = date(2000, 1, 1)
        stored_df = GoogleNBD._standardize_df(
            self._get_stored_incidents()
        ).filter(pl.col(INCIDENT_KEY_REPORTED_DATE) >= date_limit)

        with self.client.context():
            query = (
                Incident.query(
                    Incident.reported_date
                    >= stored_df[INCIDENT_KEY_REPORTED_DATE]
                    .max()
                    .strftime(UCPD_MDY_KEY_DATE_FORMAT)
                )
                .order(-Incident.reported_date)
                .fetch()
            )
            df = self._process_incidents(query)

        return pl.concat([stored_df, df]).sort(
            [INCIDENT_KEY_REPORTED_DATE, INCIDENT_KEY_REPORTED], descending=True
        )

    def get_last_90_days_of_incidents(self) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(
            (datetime.today() - timedelta(days=90)).date()
        )
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())

    def get_last_year_days_of_incidents(self) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(
            (datetime.today() - timedelta(days=365)).date()
        )
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())

    def get_all_incidents(self) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days()
        return df, self._list_to_parsed_list(df[INCIDENT_KEY_TYPE].to_list())
