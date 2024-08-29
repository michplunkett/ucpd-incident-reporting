# UChicago Incident Page Reporter
This application makes use of scraped incidents from the UCPD Daily Incident Reports and displays them in a handful of ways.

## Article(s) Citing this Project
- UChicago Police Department Incident Reporter: [Link](https://chicagomaroon.com/uchicago-police-department-incident-reporter/)
- The Maroon Launches UChicago Police Department Incident Reporter: [Link](https://chicagomaroon.com/41255/grey-city/the-maroon-launches-uchicago-police-department-incident-reporter/)

## Project Requirements
- Python version: `^3.11`
- [Poetry](https://python-poetry.org/)
- Google Cloud Platform [service account](https://cloud.google.com/iam/docs/service-account-overview) with location of the `service_account.json` file stored in the environment variable: `GOOGLE_APPLICATION_CREDENTIALS`
- Google Cloud Platform project ID stored in the environment variable: `GOOGLE_CLOUD_PROJECT`

## Instructions to Run the Project
1. Go into the base directory of the repository and type `poetry shell` into the terminal.
2. Use the `make run` command.

## Technical Notes
- Any modules should be added via the `poetry add [module]` command.
  - Example: `poetry add black`

## Standard Commands
- `make`: Runs `create-requirements` and `lint`, respectively.
- `make create-requirements`: Runs the `Poetry` command that creates an up-to-date `requirements.txt` file.
- `make lint`: Runs `pre-commit` and creates the `requirements.txt` file.
- `make run`: Starts the `FastAPI` application.
