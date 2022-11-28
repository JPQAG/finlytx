import datetime
from dateutil.relativedelta import relativedelta
from typing import  Any, Dict, List

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

def get_dict_from_list(
    dict_list: List[Dict],
    key_input: str,
    val_input: any
) -> List[Dict]:
    assert len(dict_list) !=0, f"List must not be empty."
    assert isinstance(key_input, str), f"Key must be of type string."
    keys_lists = [list(obj.keys()) for obj in dict_list]
    assert not keys_lists or all(keys_lists[0] == b for b in keys_lists[1:]), f"Keys of dictionaries must match."
    assert key_input in keys_lists[0], f"Key not found in dicts."
    
    filtered_list = [obj for obj in dict_list if obj[key_input] == val_input]
    
    assert len(filtered_list) != 0, f"Key/Val not found in provided list."
    assert len(filtered_list) == 1, f"More than one dictionary matched."
    
    return filtered_list[0]