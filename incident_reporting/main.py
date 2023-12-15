import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from incident_reporting.external.google_nbd import GoogleNBD
from incident_reporting.utils.constants import (
    KEY_REPORTED,
    KEY_REPORTED_DATE,
    LOGGING_FORMAT,
    UCPD_DATE_FORMAT,
    UCPD_MDY_DATE_FORMAT,
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
    df, types = client.get_last_30_days_of_incidents(True)

    # Convert date and datetime objects to strings
    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        for key, value in df_dict[i].items():
            if key == KEY_REPORTED:
                df_dict[i][KEY_REPORTED] = value.strftime(UCPD_MDY_DATE_FORMAT)
            elif key == KEY_REPORTED_DATE:
                df_dict[i][KEY_REPORTED_DATE] = value.strftime(UCPD_DATE_FORMAT)

    return JSONResponse(content={"incidents": df_dict, "types": types})


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
