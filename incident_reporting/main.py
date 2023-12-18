import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    KEY_REPORTED,
    KEY_REPORTED_DATE,
    LOGGING_FORMAT,
    TYPE_INFORMATION,
    UCPD_DATE_FORMAT,
    UCPD_MDY_DATE_FORMAT,
)
from incident_reporting.utils.functions import create_seasonal_incident_totals


logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
logger = logging.getLogger()

app = FastAPI(debug=True)
base_dir = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=str(Path(base_dir, "static"))),
    name="static",
)
templates = Jinja2Templates(directory=str(Path(base_dir, "templates")))

client = GoogleNBD()


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> Response:
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/thirty_day_map", response_class=HTMLResponse)
def thirty_day_map(request: Request) -> Response:
    _, types = client.get_last_30_days_of_incidents(True)
    if TYPE_INFORMATION in types:
        types.remove(TYPE_INFORMATION)
    types.sort()

    return templates.TemplateResponse(
        "thirty_day_map.html", {"request": request, "types": types}
    )


@app.get("/incidents/map", response_class=JSONResponse)
def get_map_incidents() -> JSONResponse:
    df, _ = client.get_last_30_days_of_incidents(True)

    # Convert date and datetime objects to strings
    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        df_dict[i][KEY_REPORTED] = df_dict[i][KEY_REPORTED].strftime(
            UCPD_MDY_DATE_FORMAT
        )
        df_dict[i][KEY_REPORTED_DATE] = df_dict[i][KEY_REPORTED_DATE].strftime(
            UCPD_DATE_FORMAT
        )

    return JSONResponse(content={"incidents": df_dict})


@app.get("/hourly_summation", response_class=HTMLResponse)
def hourly_summation(request: Request) -> Response:
    return templates.TemplateResponse(
        "hourly_summation.html", {"request": request}
    )


@app.get("/incidents/hourly", response_class=JSONResponse)
def get_hourly_incidents() -> JSONResponse:
    (
        fall_hours,
        spring_hours,
        summer_hours,
        total_hours,
        winter_hours,
    ) = create_seasonal_incident_totals(*client.get_all_incidents())

    return JSONResponse(
        content={
            "fall": fall_hours,
            "spring": spring_hours,
            "summer": summer_hours,
            "total": total_hours,
            "winter": winter_hours,
        }
    )


@app.get("/yearly_summation", response_class=HTMLResponse)
def yearly_summation(request: Request) -> Response:
    return templates.TemplateResponse(
        "yearly_summation.html", {"request": request}
    )
