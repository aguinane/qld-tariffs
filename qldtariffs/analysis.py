from collections import namedtuple
from statistics import mean
import datetime
import calendar
from .prices import get_tariff_period

Usage = namedtuple('Usage', ['peak', 'shoulder', 'offpeak', 'all', 'demand'])
MonthUsage = namedtuple(
    'MonthUsage', ['days', 'peak', 'shoulder', 'offpeak', 'all', 'demand'])


def get_monthly_usages(records, retailer='Ergon', tariff='T14'):
    """ Get summated monthly usages

    :param records: Tuple in the form of (billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    """

    months = dict()
    billing = split_into_billing_intervals(records)
    for billing_end, usage in billing:
        month = (billing_end.year, billing_end.month)
        if month not in months:
            months[month] = []

    dailies = get_daily_usages(records, retailer, tariff)
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

    :param records: Tuple in the form of (billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    """
    # Sort and get top 4 demand days
    top_four_days = []
    for i, day in enumerate(sorted(daily_summary, key=lambda tup: tup[4], reverse=True)):
        if i < 4:
            avg_peak_demand = average_daily_peak_demand(day.demand)
            top_four_days.append(avg_peak_demand)
    return mean(top_four_days)


def average_daily_peak_demand(peak_usage, peak_hrs=6.5):
    """ Calculate the average daily peak demand in kW

    :param peak_usage: Usage during peak window in kWh
    :param peak_hrs: Length of peak window in hours
    """
    return peak_usage / peak_hrs


def get_daily_usages(records, retailer='Ergon', tariff='T12'):
    """ Get summated daily usages

    :param records: Tuple in the form of (billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    :param tariff: Name of tariff from config
    """
    daily_usage = dict()
    billing = split_into_billing_intervals(records)
    for billing_end, usage in billing:
        day = billing_end.date()
        if day not in daily_usage:
            daily_usage[day] = Usage(0, 0, 0, 0, 0)  # Create daily tuple

        period, demand_period = get_tariff_period(billing_end, retailer, tariff)
        if demand_period == 'PEAK':
            demand_usage = usage
        else:
            demand_usage = 0

        if period == 'PEAK':
            daily_usage[day] = Usage(daily_usage[day][0] + usage,
                                     daily_usage[day][1],
                                     daily_usage[day][2],
                                     daily_usage[day][3] + usage,
                                     demand_usage)
        elif period == 'SHOULDER':
            daily_usage[day] = Usage(daily_usage[day][0],
                                     daily_usage[day][1] + usage,
                                     daily_usage[day][2],
                                     daily_usage[day][3] + usage,
                                     demand_usage)
        else:
            daily_usage[day] = Usage(daily_usage[day][0],
                                     daily_usage[day][1],
                                     daily_usage[day][2] + usage,
                                     daily_usage[day][3] + usage,
                                     demand_usage)
    return daily_usage


def split_into_billing_intervals(records):
    """ Split load data into 30 min billing intervals

    :param records: Tuple in the form of (start_date, end_date, usage)
    """
    usage_records = dict()
    for record in records:
        start_date = record[0]
        end_date = record[1]
        usage = record[2]
        interval = int((end_date - start_date).total_seconds() / 60)

        if interval <= 30:
            billing_end = get_billing_end(end_date)
            # Increment dictionary value
            if billing_end not in usage_records:
                usage_records[billing_end] = usage
            else:
                usage_records[billing_end] += usage
        else:
            # Calcualte average usage per 30mins
            avg_usage = usage / (interval / 30)

            # Split this usage into 30-min billing intervals
            adj_start = get_billing_end(start_date)
            adj_end = get_billing_end(end_date)
            for billing_end in billing_intervals(adj_start, adj_end):
                # Increment dictionary value
                if billing_end not in usage_records:
                    usage_records[billing_end] = avg_usage
                else:
                    usage_records[billing_end] += avg_usage

    # Output grouped values as list
    for key in sorted(usage_records.keys()):
        yield (key, usage_records[key])


def billing_intervals(start_date, end_date):
    """ Get list of billing intervals between two dates """
    delta = datetime.timedelta(seconds=30 * 60)
    curr = start_date
    while curr <= end_date:
        yield curr
        curr += delta


def get_billing_end(end_date):
    """ Get 30min billing end time """
    if end_date.minute == 0:
        return end_date
    elif end_date.minute > 30:
        return end_date.replace(hour=end_date.hour + 1, minute=0)
    else:
        return end_date.replace(minute=30)
