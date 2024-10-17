"""
Simple utility module for reused functions that don't fit into any other module.
"""

from datetime import date, datetime


def normalize_date(year: date | datetime | int, month: int = 0, day: int = 0) -> date:
    """Returns a date object from a date or datetime object or even numbers.

    If a date or datetime object is passed, it is stripped of time information.
    If only a year as number is passed, the month and day numbers are extracted
    from the other arguments.

    Args:
        year (int | date | datetime): Either a date to check or the year if
            month and day are also provided.
        month (int, optional): If the year is a number, the month must also
            be provided. Defaults to 0.
        day (int, optional): If the year is a number, the day must also be
            provided. Defaults to 0.

    Returns:
        The normalized date object, stripped of time information.
    """
    if isinstance(year, datetime):
        return year.date()
    if isinstance(year, date):
        return year
    return date(year, month, day)

def easter(year: int | date | datetime) -> date:
    """Calculates the date of Easter Sunday for a given year.

    If a date or datetime object is passed, the year is extracted from it.

    Args:
        year: The year for which to calculate Easter Sunday.

    Returns:
        The date of Easter Sunday for the given year.
    """
    if isinstance(year, datetime) or isinstance(year, date):
        year = year.year
    a, b, c = year % 19, year // 100, year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    return date(year, f // 31, f % 31 + 1)
