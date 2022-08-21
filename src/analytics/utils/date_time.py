import datetime
from dateutil.relativedelta import relativedelta


def years_between_dates(first_date: datetime.date, second_date: datetime.date) -> float:
    return relativedelta(second_date, first_date).years
