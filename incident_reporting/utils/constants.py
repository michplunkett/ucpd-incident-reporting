import os


# Date/Time Constants
UCPD_DATE_FORMAT = "%m/%d/%y %I:%M %p"
UCPD_MDY_DATE_FORMAT = "%m/%d/%Y"
UCPD_MDY_KEY_DATE_FORMAT = "%Y-%m-%d"

# Environment Constants
ENV_GCP_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
ENV_GCP_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

# File Type Constants
FILE_TYPE_JSON = "json"
