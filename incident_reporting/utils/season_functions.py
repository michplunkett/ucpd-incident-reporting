from datetime import datetime

import polars as pl

from incident_reporting.utils.constants import (
    KEY_REPORTED,
    KEY_SEASON,
    KEY_TYPE,
    TYPE_INFORMATION,
)


def create_or_increment_type(
    hour_dict: {int: {str: int}}, i_type: str, reported_dt: datetime
) -> None:
    if i_type in hour_dict[reported_dt.hour]:
        hour_dict[reported_dt.hour][i_type] += 1
    else:
        hour_dict[reported_dt.hour][i_type] = 1


def type_counts_to_sorted_list(
    d: {int: {str: int}},
) -> {int: [tuple[str, int]]}:
    for k in d.keys():
        type_counts = [(sub_k, d[k][sub_k]) for sub_k in d[k].keys()]
        d[k] = sorted(type_counts, key=lambda tc: tc[1], reverse=True)
    return d


def create_seasonal_incident_totals(
    df: pl.DataFrame,
    types: [str],
) -> (
    {int: [tuple[str, int]]},
    {int: [tuple[str, int]]},
    {int: [tuple[str, int]]},
    {int: [tuple[str, int]]},
    {int: [tuple[str, int]]},
):
    types.remove(TYPE_INFORMATION)

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
        for t in types:
            if t in incident[KEY_TYPE].split(" / "):
                create_or_increment_type(total_hours, t, incident[KEY_REPORTED])
                match incident[KEY_SEASON]:
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

    return (
        type_counts_to_sorted_list(fall_hours),
        type_counts_to_sorted_list(spring_hours),
        type_counts_to_sorted_list(summer_hours),
        type_counts_to_sorted_list(total_hours),
        type_counts_to_sorted_list(winter_hours),
    )


def create_hour_and_breakdown_counts(
    season_count: {int: [tuple[str, int]]}, is_total: bool = False
) -> ([dict], [dict]):
    breakdown_counts: [dict] = []
    hour_counts: [dict] = []
    # If we are looking at all seasons, we want to raise the threshold.
    incident_threshold = 20 if is_total else 4

    for i in range(24):
        total_incidents = 0
        other_incidents = 0
        key = f"{i}:00"
        breakdown_obj = {"name": key, "id": key, "data": []}
        for tc in season_count[i]:
            _, i_count = tc
            total_incidents += i_count
            # Only incident counts >= the threshold get individually added to
            # the breakdown, all others get grouped as 'Other'.
            if i_count >= incident_threshold:
                breakdown_obj["data"].append(tc)
            else:
                other_incidents += i_count
        breakdown_obj["data"].append(("Other", other_incidents))
        breakdown_counts.append(breakdown_obj)
        hour_counts.append(
            {"name": key, "y": total_incidents, "drilldown": key}
        )

    return hour_counts, breakdown_counts
