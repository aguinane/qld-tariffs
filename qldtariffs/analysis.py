from collections import namedtuple
import datetime
from .prices import get_tariff_period

Usage = namedtuple('usage', ['peak', 'shoulder', 'offpeak', 'all'])


def get_daily_usages(records, retailer='Ergon'):
    """ Get summated daily usages

    :param records: Tuple in the form of (billing_end, usage)
    :param retailer: Retailer config to get the peak time periods from
    """
    daily_usage = dict()
    billing = split_into_billing_intervals(records)
    for billing_end, usage in billing:
        day = billing_end.date()
        if day not in daily_usage:
            daily_usage[day] = Usage(0, 0, 0, 0)  # Create daily tuple

        period = get_tariff_period(billing_end, retailer, 'T12')
        if period == 'PEAK':
            daily_usage[day] = Usage(daily_usage[day][0] + usage,
                                     daily_usage[day][1],
                                     daily_usage[day][2],
                                     daily_usage[day][3] + usage)
        elif period == 'SHOULDER':
            daily_usage[day] = Usage(daily_usage[day][0],
                                     daily_usage[day][1] + usage,
                                     daily_usage[day][2],
                                     daily_usage[day][3] + usage)
        else:
            daily_usage[day] = Usage(daily_usage[day][0],
                                     daily_usage[day][1],
                                     daily_usage[day][2] + usage,
                                     daily_usage[day][3] + usage)
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
