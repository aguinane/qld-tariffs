from datetime import datetime, date
from typing import NamedTuple
from typing import Iterable, Tuple, Dict, List
from energy_shaper import PROFILE_DEFAULT
from energy_shaper import group_into_profiled_intervals
from energy_shaper import group_into_daily_summary
from .rates import get_tariff_rates
from .rates import get_tou_times


def get_daily_usages(
    records: Iterable[Tuple[datetime, datetime, float]],
    tou_timings: str = "qld-regional",
    profile: List[float] = PROFILE_DEFAULT,
):
    """ Get summated daily usages

    :return: Dictionary with DaySummary by day
    """

    tou_times = get_tou_times(tou_timings)
    half_hourly = list(group_into_profiled_intervals(records, interval_m=30))
    return group_into_daily_summary(
        half_hourly,
        profile,
        tou_times.peak_months,
        tou_times.peak_days,
        tou_times.peak_start,
        tou_times.peak_end,
        tou_times.shoulder_months,
        tou_times.shoulder_days,
        tou_times.shoulder_start,
        tou_times.shoulder_end,
    )


class Usage(NamedTuple):
    """ Represents a usage period """

    peak: float
    shoulder: float
    offpeak: float
    total: float

    def __repr__(self) -> str:
        return f"<Usage {self.total}>"


def get_daily_charges(
    records: Iterable[Tuple[datetime, datetime, float]],
    retailer: str = "ergon",
    tariff: str = "t12",
    fy: str = "2016",
    profile: List[float] = PROFILE_DEFAULT,
) -> Dict[date, Usage]:
    """ Get summated daily usages

    :param records: Tuple in the form of (billing_start, billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    :return: Dictionary with usages by day
    """
    rates = get_tariff_rates(tariff, retailer, fy)
    daily_summaries = get_daily_usages(records, rates.tou_desc, profile)
    daily_usage = {}
    for day in daily_summaries:
        daily_usage[day.day.date()] = Usage(
            day.peak, day.shoulder, day.offpeak, day.total
        )

    return daily_usage


def financial_year_ending(day: date) -> int:
    """ Return the financial year (ending) for a date

    :param day: Day in time
    """
    if day.month >= 7:
        return day.year
    return day.year
