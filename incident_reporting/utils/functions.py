from datetime import datetime

import polars as pl

from incident_reporting.utils.constants import KEY_REPORTED, KEY_TYPE


def create_or_increment_type(
    hour_dict: {int: {str: int}}, i_type: str, reported_dt: datetime
) -> None:
    if i_type in hour_dict[reported_dt.hour]:
        hour_dict[reported_dt.hour][i_type] += 1
    else:
        hour_dict[reported_dt.hour][i_type] = 1


def create_seasonal_incident_totals(
    df: pl.DataFrame,
    types: [str],
) -> (
    {int: {str: int}},
    {int: {str: int}},
    {int: {str: int}},
    {int: {str: int}},
    {int: {str: int}},
):
    fall_hours: {int: {str: int}} = {}
    spring_hours: {int: {str: int}} = {}
    summer_hours: {int: {str: int}} = {}
    total_hours: {int: {str: int}} = {}
    winter_hours: {int: {str: int}} = {}
    for i in range(0, 24):
        fall_hours[i] = {}
        spring_hours[i] = {}
        summer_hours[i] = {}
        total_hours[i] = {}
        winter_hours[i] = {}

    df_dict = df.to_dicts()
    for i in range(len(df_dict)):
        incident = df_dict[i]
        season = determine_season(df_dict[i][KEY_REPORTED])
        for t in types:
            if t in incident[KEY_TYPE].split(" / "):
                create_or_increment_type(total_hours, t, incident[KEY_REPORTED])
                match season:
                    case "Fall":
                        create_or_increment_type(
                            fall_hours, t, incident[KEY_REPORTED]
                        )
                    case "Spring":
                        create_or_increment_type(
                            spring_hours, t, incident[KEY_REPORTED]
                        )
                    case "Summer":
                        create_or_increment_type(
                            summer_hours, t, incident[KEY_REPORTED]
                        )
                    case "Winter":
                        create_or_increment_type(
                            winter_hours, t, incident[KEY_REPORTED]
                        )

    return fall_hours, spring_hours, summer_hours, total_hours, winter_hours


def determine_season(test_date: datetime) -> str:
    test_date_tuple = (test_date.month, test_date.day)
    if (3, 1) <= test_date_tuple < (5, 31):
        return "Spring"
    elif (6, 1) <= test_date_tuple < (8, 31):
        return "Summer"
    elif (9, 1) <= test_date_tuple < (12, 1):
        return "Fall"
    else:
        return "Winter"
