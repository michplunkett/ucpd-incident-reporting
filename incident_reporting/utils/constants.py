import os


# Application Constants
LOGGING_FORMAT = "%(levelname)s:\t%(message)s"

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
KEY_COMMENTS = "comments"
KEY_DISPOSITION = "disposition"
KEY_ID = "ucpd_id"
KEY_REPORTED = "reported"
KEY_REPORTED_DATE = "reported_date"
KEY_TYPE = "incident"
KEY_VALIDATED_ADDRESS = "validated_address"
KEY_VALIDATED_LOCATION = "validated_location"

# List of incident types that we exclude from location graphics
EXCLUDED_TYPES = [
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
