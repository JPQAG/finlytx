import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List

def calculate_years_between_dates(
    start_date: datetime.datetime,
    end_date: datetime.datetime
) -> float:
    """Calculate the number of years between two dates.

    Args:
        start_date (datetime.datetime): The starting date.
        end_date (datetime.datetime): The ending date.

    Returns:
        float: The number of years between two dates.
    """
    return relativedelta(end_date, start_date).years

def convert_date_series_to_years(
    series: List[Dict],
    relative_date: datetime.datetime
) -> List[Dict]:
    """Convert the date attribute in a series (list of dict) to a 
        time attribute in years.

    Args:
        series (List[Dict]): List of dictionaries containing date attribute.
        relative_date (datetime.datetime): Relative start date.

    Returns:
        List[Dict]: List of dictionaries containing time attribute (in years).
    """

    new_series = []

    for obj in series:
        new_series.append(
            {
                'time': calculate_years_between_dates(relative_date, obj['date']),
                'rate': obj['rate']
            }
        )

    return new_series