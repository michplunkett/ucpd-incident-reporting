from datetime import datetime


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
