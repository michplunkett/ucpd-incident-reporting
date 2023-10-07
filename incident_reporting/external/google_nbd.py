"""Contains code relating to the Google Cloud Platform Datastore service."""
import json
from datetime import datetime, timedelta

import polars as pl
from google.cloud.datastore.helpers import GeoPoint
from google.cloud.ndb import Client, GeoPtProperty, Model, StringProperty
from google.oauth2 import service_account

from incident_reporting.utils.constants import (
    ENV_GCP_CREDENTIALS,
    ENV_GCP_PROJECT_ID,
    FILE_TYPE_JSON,
    UCPD_MDY_DATE_FORMAT,
)


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

    def get_incidents_back_x_days(self, days_back: int) -> pl.DataFrame:
        with self.client.context():
            date_str = (datetime.today() - timedelta(days=days_back)).strftime(
                UCPD_MDY_DATE_FORMAT
            )
            query = (
                Incident.query(Incident.reported_date >= date_str)
                .order(-Incident.reported_date)
                .fetch()
            )
            incident_list = []
            for i in query:
                record = {}
                for key, value in i.to_dict().items():
                    if isinstance(value, GeoPoint):
                        record[key] = [value.latitude, value.longitude]
                        continue
                    record[key] = value
                    incident_list.append(record)
            df = pl.DataFrame(incident_list)
            return df
