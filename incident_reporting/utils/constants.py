import os


# Date/Time Constants
TIMEZONE_CHICAGO = "America/Chicago"
UCPD_DATE_FORMAT = "%m/%d/%y %I:%M %p"
UCPD_MDY_DATE_FORMAT = "%m/%d/%Y"
UCPD_MDY_KEY_DATE_FORMAT = "%Y-%m-%d"
UTC_DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z"

# Environment Constants
ENV_GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
ENV_GCP_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# File Constants
FILE_ENCODING_UTF_8 = "utf-8"
FILE_OPEN_MODE_READ = "r"
FILE_TYPE_JSON = "json"

# Incident Constants
INCIDENT_KEY_TYPE = "incident"
INCIDENT_KEY_REPORTED = "reported"
INCIDENT_KEY_REPORTED_DATE = "reported_date"
INCIDENT_KEY_VALIDATED_LOCATION = "validated_location"
