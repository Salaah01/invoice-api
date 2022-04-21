import typing as _t
from datetime import datetime, date
from django.conf import settings


def date_to_str(date_: _t.Union[date, datetime]) -> str:
    """Convert date to string.
    Args:
        date_: Date to convert.
    Returns:
        String representation of date.
    """
    return date_.strftime(settings.DATE_FMT)
