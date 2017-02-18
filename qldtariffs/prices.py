from collections import namedtuple
from .tariffs import T11, T12, T14

Charge = namedtuple('Charge', ['units', 'unit_rate',
                               'cost_excl_gst', 'gst', 'cost_incl_gst'])


def get_tariff_rates(tariff, retailer):
    """ Load tariff rates from config file

    :param tariff: Name of tariff from yaml config
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


