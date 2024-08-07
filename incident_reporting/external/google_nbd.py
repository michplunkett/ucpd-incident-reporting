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
    ENV_GCP_DEPLOY,
    FILE_OPEN_MODE_READ,
    FILE_TYPE_JSON,
    KEY_REPORTED,
    KEY_REPORTED_DATE,
    KEY_TYPE,
    KEY_VALIDATED_ADDRESS,
    KEY_VALIDATED_LOCATION,
    TIMEZONE_CHICAGO,
    UCPD_MDY_KEY_DATE_FORMAT,
    UTC_DATE_TIME_FORMAT,
)


# Incidents of these types have been excluded from the list for the sake of
# victim's privacy and due to the nature the incidents included in this list.
EXCLUDED_INCIDENT_TYPES = [
    "Aggravated Criminal Sexual Assault",
    "Aggravated Domestic Assault",
    "Aggravated Domestic Battery",
    "Attempted Sexual Assault",
    "Criminal Sexual Abuse",
    "Criminal Sexual Assault",
    "Dating Violence",
    "Domestic Aggravated Assault",
    "Domestic Aggravated Battery",
    "Domestic Assault",
    "Domestic Battery",
    "Domestic Dispute",
    "Domestic Disturbance",
    "Domestic Issue",
    "Domestic",
    "Eavesdropping",
    "Fondling",
    "Harassing Messages",
    "Harassment by Electronic Means",
    "Harassment",
    "Indecent Exposure",
    "Information Harassment",
    "Luring a Minor",
    "Medical Call",
    "Medical Transport",
    "Mental Health",
    "Order of Protection Arrest",
    "Order of Protection Notification",
    "Order of Protection",
    "Sex Crime",
    "Sex Offender",
    "Sex Offense",
    "Sex Related",
    "Sexual Abuse",
    "Sexual Assault",
    "Stalking",
    "Suspicious Mail",
    "Threatening Phone Call",
    "Violation of Order of Protection",
    "Warrant",
    "Well-Being",
]


class Incident(Model):
    """Standard data structure for recovered UCPD incidents."""

    ucpd_id = StringProperty(indexed=True)
    incident = StringProperty(indexed=True)
    predicted_incident = StringProperty()
    reported = StringProperty()
    reported_date = StringProperty(indexed=True)
    occurred = StringProperty()
    comments = StringProperty()
    disposition = StringProperty()
    location = StringProperty()
    season = StringProperty(indexed=True)
    validated_address = StringProperty()
    validated_location = GeoPtProperty()


class GoogleNBD:
    """Create the client and access GCP NBD functionality."""

    ENTITY_TYPE = "Incident"

    def __init__(self):
        if ENV_GCP_CREDENTIALS.endswith(FILE_TYPE_JSON) or ENV_GCP_DEPLOY:
            self.client = Client()
        else:
            credentials = service_account.Credentials.from_service_account_info(
                json.loads(ENV_GCP_CREDENTIALS)
            )
            self.client = Client(credentials=credentials)

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
            pl.col(KEY_REPORTED)
            .str.strptime(pl.Datetime, format=UTC_DATE_TIME_FORMAT)
            .dt.convert_time_zone(TIMEZONE_CHICAGO),
            pl.col(KEY_REPORTED_DATE).str.strptime(
                pl.Date, format=UCPD_MDY_KEY_DATE_FORMAT
            ),
            pl.col(KEY_VALIDATED_LOCATION)
            .str.split(",")
            .cast(pl.List(pl.Float64)),
            pl.col(KEY_VALIDATED_ADDRESS).str.to_titlecase(),
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

        return GoogleNBD._standardize_df(pl.DataFrame(incident_list))

    @staticmethod
    def _get_stored_incidents() -> pl.DataFrame:
        file_path = (
            os.getcwd().replace("\\", "/")
            + "/incident_reporting/data/incident_dump.csv.gz"
        )

        if not os.path.exists(file_path):
            return pl.DataFrame()

        with gzip.open(file_path, FILE_OPEN_MODE_READ) as f:
            return GoogleNBD._standardize_df(pl.read_csv(f.read()))

    @staticmethod
    def _includes_excluded(i_type: str) -> bool:
        i_type = i_type.split(" / ")
        for i in i_type:
            if i in EXCLUDED_INCIDENT_TYPES:
                return True
        return False

    def _get_incidents_back_x_days(
        self, date_limit: date = None, exclude: bool = False
    ) -> pl.DataFrame:
        if not date_limit:
            date_limit = date(2000, 1, 1)

        stored_df = self._get_stored_incidents()

        with self.client.context():
            # Check if the data frame has any rows.
            if stored_df.shape[0]:
                stored_df = stored_df.filter(
                    pl.col(KEY_REPORTED_DATE) >= date_limit
                )

                query = (
                    Incident.query(
                        Incident.reported_date
                        > stored_df[KEY_REPORTED_DATE]
                        .max()
                        .strftime(UCPD_MDY_KEY_DATE_FORMAT)
                    )
                    .order(-Incident.reported_date)
                    .fetch()
                )

                if len(query):
                    query = self._process_incidents(query)

                result = (
                    pl.concat([stored_df, query]) if len(query) else stored_df
                )
            else:
                result = (
                    Incident.query(
                        Incident.reported_date
                        > date_limit.strftime(UCPD_MDY_KEY_DATE_FORMAT)
                    )
                    .order(-Incident.reported_date)
                    .fetch()
                )
                result = self._process_incidents(result)

            if exclude:
                result = result.filter(
                    ~pl.col(KEY_TYPE).apply(self._includes_excluded)
                )

            return result.sort(
                [KEY_REPORTED_DATE, KEY_REPORTED], descending=True
            )

    def get_last_30_days_of_incidents(
        self, exclude: bool = False
    ) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(
            (datetime.today() - timedelta(days=30)).date(), exclude
        )
        return df, self._list_to_parsed_list(df[KEY_TYPE].to_list())

    def get_last_90_days_of_incidents(
        self, exclude: bool = False
    ) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(
            (datetime.today() - timedelta(days=90)).date(), exclude
        )
        return df, self._list_to_parsed_list(df[KEY_TYPE].to_list())

    def get_last_year_of_incidents(
        self, exclude: bool = False
    ) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(
            (datetime.today() - timedelta(days=365)).date(), exclude
        )
        return df, self._list_to_parsed_list(df[KEY_TYPE].to_list())

    def get_all_incidents(self, exclude: bool = False) -> (pl.DataFrame, [str]):
        df = self._get_incidents_back_x_days(exclude=exclude)
        return df, self._list_to_parsed_list(df[KEY_TYPE].to_list())
