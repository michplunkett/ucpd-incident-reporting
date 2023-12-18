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
    KEY_SEASON,
    KEY_TYPE,
    LOGGING_FORMAT,
    TYPE_INFORMATION,
    UCPD_DATE_FORMAT,
    UCPD_MDY_DATE_FORMAT,
)
from incident_reporting.utils.functions import determine_season


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
def home(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/thirty_day_map", response_class=HTMLResponse)
def thirty_day_map(request: Request) -> templates.TemplateResponse:
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
def hourly_summation(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        "hourly_summation.html", {"request": request}
    )


@app.get("/incidents/hourly", response_class=JSONResponse)
def get_hourly_incidents() -> JSONResponse:
    df, types = client.get_all_incidents()

    season_summaries: {str: {str: int}} = {
        "Winter": {},
        "Summer": {},
        "Spring": {},
        "Fall": {},
    }

    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        df_dict[i][KEY_SEASON] = determine_season(df_dict[i][KEY_REPORTED])
        for t in types:
            if t in df_dict[i][KEY_TYPE]:
                if t in season_summaries[df_dict[i][KEY_SEASON]]:
                    season_summaries[df_dict[i][KEY_SEASON]] += 1
                else:
                    season_summaries[df_dict[i][KEY_SEASON]] = 1

    return JSONResponse(content={"season_summaries": season_summaries})


@app.get("/yearly_summation", response_class=HTMLResponse)
def yearly_summation(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse(
        "yearly_summation.html", {"request": request}
    )
