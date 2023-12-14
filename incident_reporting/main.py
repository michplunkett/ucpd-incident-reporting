import logging
from pathlib import Path

import polars as pl
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import EXCLUDED_TYPES, LOGGING_FORMAT


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
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/thirty_day_map", response_class=HTMLResponse)
def thirty_day_map(request: Request):
    return templates.TemplateResponse(
        "thirty_day_map.html", {"request": request}
    )


@app.get("/incidents/map", response_class=JSONResponse)
def get_map_incidents():
    df, types = client.get_last_30_days_of_incidents()

    # Remove certain event types from lists
    for no_show in EXCLUDED_TYPES:
        if no_show in types:
            types.remove(no_show)

    df = df.filter(~pl.col("incident").str.contains("|".join(EXCLUDED_TYPES)))

    return JSONResponse(
        content={"incidents": df.write_json(row_oriented=True), "types": types}
    )


@app.get("/hourly_summation", response_class=HTMLResponse)
def hourly_summation(request: Request):
    return templates.TemplateResponse(
        "hourly_summation.html", {"request": request}
    )


@app.get("/yearly_summation", response_class=HTMLResponse)
def yearly_summation(request: Request):
    return templates.TemplateResponse(
        "yearly_summation.html", {"request": request}
    )
