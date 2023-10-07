"""Contains code relating to the Google Cloud Platform Datastore service."""
import json
from datetime import date, datetime

from google.cloud.ndb import Client
from google.oauth2 import service_account

from incident_reporting.models.incident import Incident
from incident_reporting.utils.constants import (
    ENV_GCP_CREDENTIALS,
    ENV_GCP_PROJECT_ID,
    FILE_TYPE_JSON,
    UCPD_MDY_KEY_DATE_FORMAT,
)


def get_incident(ucpd_id: str):
    """Get Incident from datastore."""
    incident = Incident.get_by_id(ucpd_id)
    if incident:
        return incident
    else:
        return None


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

    def get_latest_date(self) -> date:
        """Get latest incident date."""
        with self.client.context():
            query = Incident.query().order(-Incident.reported_date).fetch(1)
            if query:
                return datetime.strptime(
                    query[0].reported_date, UCPD_MDY_KEY_DATE_FORMAT
                ).date()
            else:
                return datetime.now().date()
