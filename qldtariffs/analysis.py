from collections import namedtuple
from statistics import mean
import datetime
import calendar
from energy_shaper import group_into_profiled_intervals
from energy_shaper import group_into_daily_summary
from . import get_tariff_rates

Usage = namedtuple('Usage', ['peak', 'shoulder', 'offpeak', 'all'])
MonthUsage = namedtuple(
    'MonthUsage', ['days', 'peak', 'shoulder', 'offpeak', 'all', 'demand'])


def get_monthly_usages(records, retailer='Ergon', tariff='T14', fy='2016'):
    """ Get summated monthly usages

    :param records: Tuple in the form of (billing_start, billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    """

    months = dict()
    billing = list(group_into_profiled_intervals(records, interval_m=30))
    for reading in billing:
        # Dates are end of billing period so first interval is previous day
        day = reading.end - datetime.timedelta(hours=0.5)
        month = (day.year, day.month)
        if month not in months:
            months[month] = []

    dailies = get_daily_usages(records, retailer, tariff, fy)
    for day in dailies:
        month = (day.year, day.month)
        months[month].append(dailies[day])

    months_summary = dict()
    for month in months:
        daily_data = months[month]
        demand = average_peak_demand(daily_data)
        u = [sum(x) for x in zip(*daily_data)]
        num_days = calendar.monthrange(month[0], month[1])[1]
        summary = MonthUsage(num_days, u[0], u[1], u[2], u[3], demand)
        months_summary[month] = summary

    return months_summary


def average_peak_demand(daily_summary):
    """ Get the average peak demand for a set of daily usage stats
    """
    # Sort and get top 4 demand days
    top_four_days = []
    for i, day in enumerate(sorted(daily_summary, key=lambda tup: (tup[0], tup[1]), reverse=True)):
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


def average_daily_peak_demand(peak_usage, peak_hrs=6.5):
    """ Calculate the average daily peak demand in kW

    :param peak_usage: Usage during peak window in kWh
    :param peak_hrs: Length of peak window in hours
    """
    return peak_usage / peak_hrs


def get_daily_usages(records, retailer='Ergon', tariff='t12', fy='2016'):
    """ Get summated daily usages

    :param records: Tuple in the form of (billing_start, billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    """

    daily_usage = dict()

    profile = [0.05,  0.07,  0.12,  0.11, 0.14,  0.14,  0.27, 0.10]

    rates = get_tariff_rates(tariff, retailer, fy)

    half_hourly = list(group_into_profiled_intervals(records, interval_m=30))
    daily_summaries = group_into_daily_summary(half_hourly, profile,
                                               rates.peak_months, rates.peak_days,
                                               rates.peak_start, rates.peak_end,
                                               rates.shoulder_months, rates.shoulder_days,
                                               rates.shoulder_start, rates.shoulder_end)
    for day in daily_summaries:
        daily_usage[day.day.date()] = Usage(day.peak, day.shoulder,
                                            day.offpeak, day.total)

    return daily_usage
