from collections import namedtuple
from .tariffs import T11, T12, T14
import datetime

Charge = namedtuple('Charge', ['units', 'unit_rate',
                               'cost_excl_gst', 'gst', 'cost_incl_gst'])


def get_tariff_period(billing_time, retailer='Ergon', tariff='T12'):
    """ Load tariff peak periods from config file

    :param billing_time: The datetime to check
    :param tariff: Name of tariff from config
    :param retailer: Name of retailer to get costs from
    """
    if tariff == 'T11':
        rates = T11
    elif tariff == 'T12':
        rates = T12
    elif tariff == 'T14':
        rates = T14
    else:
        raise ValueError("Invalid Tariff Type {}".format(tariff))

    r = rates[retailer]
    if 'shoulder_months' in r.keys():
        return in_peak(billing_time,
                       r['peak_months'], r['peak_days'],
                       r['peak_start'], r['peak_end'],
                       r['shoulder_months'], r['shoulder_days'],
                       r['shoulder_start'], r['shoulder_end']
                       )
    elif 'peak_months' in r.keys():
        # No shoulder period specified
        return in_peak(billing_time,
                       r['peak_months'], r['peak_days'],
                       r['peak_start'], r['peak_end'],
                       [], [], datetime.time(
                           0, 0, 0), datetime.time(0, 0, 0)
                       )
    else:
        # No peak period specified
        return in_peak(billing_time,
                       [], [], datetime.time(
                           0, 0, 0), datetime.time(0, 0, 0),
                       [], [], datetime.time(
                           0, 0, 0), datetime.time(0, 0, 0)
                       )


def in_peak(billing_time,
            peak_months, peak_days, peak_start, peak_end,
            shoulder_months, shoulder_days, shoulder_start, shoulder_end):
    """ Calculate if billing time is in PEAK, SHOULDER or OFFPEAK period
    """

    if in_peak_day(billing_time, peak_months, peak_days) and in_peak_time(billing_time, peak_start, peak_end):
        period = 'PEAK'
    elif in_peak_day(billing_time, shoulder_months, shoulder_days) and in_peak_time(billing_time, shoulder_start, shoulder_end):
        period = 'SHOULDER'
    else:
        period = 'OFFPEAK'
    if in_peak_time(billing_time, peak_start, peak_end):
        demand_period = 'OFFPEAK'
    else:
        demand_period = 'PEAK'
    return (period, demand_period)


def in_peak_day(billing_time, peak_months, peak_days):
    """ Calculate if billing period falls on a peak day """
    day_of_week = int(billing_time.strftime('%w'))
    if billing_time.month in peak_months and day_of_week in peak_days:
        return True
    else:
        return False


def in_peak_time(billing_time, peak_start, peak_end):
    """ Calculate if billing period falls in peak time period """
    if peak_start < billing_time.time() <= peak_end:
        return True
    else:
        return False


def get_tariff_rates(tariff, retailer):
    """ Load tariff rates from config file

    :param tariff: Name of tariff from config
    :param retailer: Name of retailer to get costs from
    """

    if tariff == 'T11':
        rates = T11
    elif tariff == 'T12':
        rates = T12
    elif tariff == 'T14':
        rates = T14
    else:
        raise ValueError("Invalid Tariff Type {}".format(tariff))
    return rates[retailer]


def calculate_charge(units, unit_rate):
    """ Calculate the billing charge

    units: The number of units to be charged
    unit_rate: The unit rate
    """
    cost_excl_gst = unit_rate * units
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    return Charge(units, unit_rate, cost_excl_gst, gst, cost_incl_gst)


def electricity_charges_general(retailer, days, usage):
    """ Calculate electricity charges for a general tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    usage: The energy usage in kWh for the billing period
    """

    GeneralTariff = namedtuple('GeneralTariff',
                               ['supply_charge', 'all_usage', 'total_charges']
                               )

    tariff_rates = get_tariff_rates('T11', retailer)
    supply_charge = calculate_charge(days, tariff_rates['supply_charge'])
    all_usage = calculate_charge(usage, tariff_rates['usage_all'])
    cost_excl_gst = supply_charge.cost_excl_gst + all_usage.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return GeneralTariff(supply_charge, all_usage, total_charges)


def electricity_charges_tou(retailer, days, peak, shoulder, offpeak):
    """ Calculate electricity charges for a time-of-use tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    peak: The energy usage in kWh for the peak billing period
    shoulder: The energy usage in kWh for the shoulder billing period
    offpeak: The energy usage in kWh for the off-peak billing period
    """

    ToUTariff = namedtuple('ToUTariff',
                           ['supply_charge', 'peak',
                            'shoulder', 'offpeak',
                            'total_charges']
                           )

    tariff_rates = get_tariff_rates('T12', retailer)
    supply_charge = calculate_charge(days, tariff_rates['supply_charge'])
    peak = calculate_charge(peak, tariff_rates['usage_peak'])
    shoulder = calculate_charge(shoulder, tariff_rates['usage_shoulder'])
    offpeak = calculate_charge(offpeak, tariff_rates['usage_offpeak'])
    cost_excl_gst = supply_charge.cost_excl_gst + peak.cost_excl_gst + \
        shoulder.cost_excl_gst + offpeak.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUTariff(supply_charge, peak, shoulder, offpeak, total_charges)


def electricity_charges_tou_demand(retailer, days, usage, demand, peak_season=True):
    """ Calculate electricity charges for a time-of-use tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    usage: The energy usage in kWh for the billing period
    demand: The chargeable demand in kW
    peak_season: Do peak season rates apply
    """

    ToUDTariff = namedtuple('ToUDTariff',
                            ['supply_charge', 'all_usage',
                                'demand', 'total_charges']
                            )

    tariff_rates = get_tariff_rates('T14', retailer)
    supply_charge = calculate_charge(days, tariff_rates['supply_charge'])
    all_usage = calculate_charge(usage, tariff_rates['usage_all'])
    if peak_season:
        demand = calculate_charge(demand, tariff_rates['demand_peak'])
    else:
        demand = calculate_charge(demand, tariff_rates['demand_offpeak'])
    cost_excl_gst = supply_charge.cost_excl_gst + \
        all_usage.cost_excl_gst + demand.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUDTariff(supply_charge, all_usage, demand, total_charges)
