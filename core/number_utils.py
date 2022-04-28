"""Utility functions for numbers."""

import typing as _t
from decimal import Decimal


def float_to_dp(
    value: float,
    dp: int = 2,
    as_decimal=False,
) -> _t.Union[Decimal, float]:
    """Convert a float to a decimal with a certain number of decimal places.

    :param value: The float to convert.
    :type value: float
    :param dp: The number of decimal places to use.
    :type dp: int
    :return: The converted value to the specified number of decimal places.
    :rtype: Decimal or float
    """
    res = Decimal(value).quantize(Decimal(10) ** -dp)
    if as_decimal:
        return res
    return float(res)
