import datetime
from dateutil.relativedelta import relativedelta


def days_between_dates(first_date: datetime.datetime, second_date: datetime.datetime) -> float:
    return (second_date - first_date).days

def months_between_dates(first_date: datetime.datetime, second_date: datetime.datetime) -> float:
    return (first_date.year - second_date.year) * 12 + first_date.month - second_date.month

def years_between_dates(first_date: datetime.datetime, second_date: datetime.datetime) -> float:
    return relativedelta(second_date, first_date).years
