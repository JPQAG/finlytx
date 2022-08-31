import datetime

from typing import Dict, List



def generate_cashflows() -> None:
    pass

def match_cashflow_to_discount_curve(
    cashflows: List[Dict],
    discount_curve: List[Dict]
) -> List[Dict]:
    """Match cashflows to discount rates by date.

    Args:
        cashflows (List[Dict]): Cashflow series
        discount_curve (List[Dict]): Discount curve series.

    Returns:
        List[Dict]: Combined date, cashflow value and discount rate.
    """

    matched_list = []

    for cashflow in cashflows:
        for rate in discount_curve:
            if rate['date'] == cashflow["date"]:
                matched_list.append(
                    {
                        "date": cashflow["date"],
                        "cashflow_value": cashflow["cashflow_value"],
                        "discount_rate": rate["discount_rate"]
                    }
                )

    return matched_list

def sum_cashflows(
    cashflows: List[Dict]
) -> float:
    """Calulate the sum of a series of cashflows.

    Args:
        cashflows (List[Dict]): Cashflow series (date, cashflow_value)

    Returns:
        float: Sum of cashflows.
    """

    sum = 0

    for cashflow in cashflows:
        sum += cashflow['cashflow_value']
    
    return sum

def trim_cashflows_after_workout(
    cashflows: List[Dict],
    workout_date: datetime.datetime
) -> List[Dict]:
    """Trim the cashflows to exclude any cashflows after workout date.


    Args:
        cashflows (List[Dict]): Date and value of cashflows.
        workout_date (datetime.datetime): Date after which cashflows will be excluded.

    Returns:
        List[Dict]: The included cashflows.
    """

    included_cashflows = []

    for cashflow in cashflows:
        if cashflow["date"] <= workout_date:
            included_cashflows.append(cashflow)

    return included_cashflows