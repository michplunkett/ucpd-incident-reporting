import logging
from http import HTTPMethod
from pathlib import Path

import polars as pl
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    KEY_COMMENTS,
    KEY_REPORTED,
    KEY_REPORTED_DATE,
    KEY_TYPE,
    KEY_VALIDATED_ADDRESS,
    LOGGING_FORMAT,
    TYPE_INFORMATION,
    UCPD_DATE_FORMAT,
    UCPD_MDY_DATE_FORMAT,
)
from incident_reporting.utils.season_functions import (
    create_hour_and_breakdown_counts,
    create_seasonal_incident_totals,
)


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://0.0.0.0:8000",
        "https://0.0.0.0:8000",
        "https://ucpd-incident-reporter-7cfdc3369124.herokuapp.com/",
    ],
    allow_credentials=True,
    allow_methods=[HTTPMethod.GET],
    allow_headers=["*"],
)


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

    # Remove any incidents without valid addresses
    df = df.filter(pl.col(KEY_VALIDATED_ADDRESS) != "")

    # Convert date and datetime objects to strings
    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        df_dict[i][KEY_REPORTED] = df_dict[i][KEY_REPORTED].strftime(
            UCPD_MDY_DATE_FORMAT
        )
        df_dict[i][KEY_REPORTED_DATE] = df_dict[i][KEY_REPORTED_DATE].strftime(
            UCPD_DATE_FORMAT
        )
        del df_dict[i][KEY_COMMENTS]

    return JSONResponse(content={"incidents": df_dict})


@app.get("/hourly_summation", response_class=HTMLResponse)
def hourly_summation(request: Request) -> Response:
    return templates.TemplateResponse(
        "hourly_summation.html", {"request": request}
    )


@app.get("/incidents/hourly", response_class=JSONResponse)
def get_hourly_incidents() -> JSONResponse:
    # There's likely a more efficient way to do this, but I'm in a bit of a
    # rush. Here's hoping I address it later on.
    # Create incident type totals by hour per season.
    (
        fall_hours,
        spring_hours,
        summer_hours,
        total_hours,
        winter_hours,
    ) = create_seasonal_incident_totals(*client.get_all_incidents())

    # Break those totals down to counts by hour and breakdowns per hour.
    fall_hour_counts, fall_breakdown_counts = create_hour_and_breakdown_counts(
        fall_hours
    )
    (
        spring_hour_counts,
        spring_breakdown_counts,
    ) = create_hour_and_breakdown_counts(spring_hours)
    (
        summer_hour_counts,
        summer_breakdown_counts,
    ) = create_hour_and_breakdown_counts(summer_hours)
    (
        total_hour_counts,
        total_breakdown_counts,
    ) = create_hour_and_breakdown_counts(total_hours, True)
    (
        winter_hour_counts,
        winter_breakdown_counts,
    ) = create_hour_and_breakdown_counts(winter_hours)

    return JSONResponse(
        content={
            "fall_hour_counts": fall_hour_counts,
            "fall_breakdown_counts": fall_breakdown_counts,
            "spring_hour_counts": spring_hour_counts,
            "spring_breakdown_counts": spring_breakdown_counts,
            "summer_hour_counts": summer_hour_counts,
            "summer_breakdown_counts": summer_breakdown_counts,
            "total_hour_counts": total_hour_counts,
            "total_breakdown_counts": total_breakdown_counts,
            "winter_hour_counts": winter_hour_counts,
            "winter_breakdown_counts": winter_breakdown_counts,
        }
    )


@app.get("/yearly_summation", response_class=HTMLResponse)
def yearly_summation(request: Request) -> Response:
    return templates.TemplateResponse(
        "yearly_summation.html", {"request": request}
    )


@app.get("/incidents/yearly", response_class=JSONResponse)
def get_yearly_incidents() -> JSONResponse:
    df, types = client.get_last_year_of_incidents(True)

    type_counts: {str: int} = {}
    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        incident = df_dict[i]
        for t in types:
            if t in incident[KEY_TYPE]:
                if t in type_counts:
                    type_counts[t] += 1
                else:
                    type_counts[t] = 1

    # Since there are a LARGE number of incident types, I want to limit it to
    # types that have a frequency higher than 20 and aren't 'Information'.
    type_counts_list = [
        (k, type_counts[k])
        for k in sorted(type_counts, key=type_counts.get, reverse=True)
        if type_counts[k] > 20 and k != TYPE_INFORMATION
    ]

    return JSONResponse(
        content={
            "counts": [tc[1] for tc in type_counts_list],
            "types": [tc[0] for tc in type_counts_list],
        }
    )
