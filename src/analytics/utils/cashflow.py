from typing import Dict, List

def generate_cashflows() -> None:
    pass

def match_cashflow_to_discount_curve(
    cashflows: List[Dict],
    discount_curve: List[Dict]
) -> List[Dict]:

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