from statistics import mean
from datetime import datetime, timedelta
import calendar
from typing import NamedTuple
from typing import Iterable, Tuple, Dict
from energy_shaper import group_into_profiled_intervals
from .dayanalysis import Usage, get_daily_charges


class MonthUsage(NamedTuple):
    """ Represents a usage period """

    days: int
    peak: float
    shoulder: float
    offpeak: float
    total: float
    demand: float

    def __repr__(self) -> str:
        return f"<MonthUsage {self.days} days {self.total}>"


def get_monthly_charges(
    records: Iterable[Tuple[datetime, datetime, float]],
    retailer: str = "ergon",
    tariff: str = "T14",
    fy: str = "2016",
) -> Dict[Tuple[int, int], MonthUsage]:
    """ Get summated monthly charges

    :param records: Tuple in the form of (billing_start, billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    """

    months: dict = {}
    billing = list(group_into_profiled_intervals(records, interval_m=30))
    for reading in billing:
        # Dates are end of billing period so first interval is previous day
        day = reading.end - timedelta(hours=0.5)
        month = (day.year, day.month)
        if month not in months:
            months[month] = []

    dailies = get_daily_charges(records, retailer, tariff, fy)
    for day in dailies:
        month = (day.year, day.month)
        months[month].append(dailies[day])

    months_summary = {}
    for month in months:
        daily_data = months[month]
        demand = average_peak_demand(daily_data)
        u = [sum(x) for x in zip(*daily_data)]
        num_days = calendar.monthrange(month[0], month[1])[1]
        summary = MonthUsage(num_days, u[0], u[1], u[2], u[3], demand)
        months_summary[month] = summary

    return months_summary


def average_daily_peak_demand(peak_usage: float, peak_hrs: float = 6.5) -> float:
    """ Calculate the average daily peak demand in kW

    :param peak_usage: Usage during peak window in kWh
    :param peak_hrs: Length of peak window in hours
    """
    return peak_usage / peak_hrs


def average_peak_demand(daily_summary: Dict[str, Usage]) -> float:
    """ Get the average peak demand for a set of daily usage stats
    """
    # Sort and get top 4 demand days
    top_four_days = []
    for i, day in enumerate(
        sorted(daily_summary, key=lambda tup: (tup[0], tup[1]), reverse=True)
    ):
        if i < 4:
            if day.peak:
                demand = day.peak
            else:
                demand = day.shoulder
            avg_peak_demand = average_daily_peak_demand(demand)
            top_four_days.append(avg_peak_demand)
    if top_four_days:
        return mean(top_four_days)
    else:
        return 0
