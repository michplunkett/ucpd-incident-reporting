"""Initialize and set the logging defaults."""

import logging
import sys

import google.cloud.logging as gcp_logging
from google.oauth2 import service_account

from incident_reporting.utils.constants import (
    ENV_GCP_CREDENTIALS,
    FILE_TYPE_JSON,
)


def init_logger():
    """Set logger defaults."""
    if ENV_GCP_CREDENTIALS.endswith(FILE_TYPE_JSON):
        logging_client = gcp_logging.Client()
    else:
        logging_client = gcp_logging.Client(
            credentials=service_account.Credentials.from_service_account_info(
                ENV_GCP_CREDENTIALS
            )
        )

    logging_client.setup_logging(log_level=logging.INFO)
    logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
