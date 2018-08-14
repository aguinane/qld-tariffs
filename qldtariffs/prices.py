from collections import namedtuple
import datetime
from . import get_tariff_rates


Charge = namedtuple('Charge',
                    ['units', 'unit_rate',
                     'cost_excl_gst', 'gst', 'cost_incl_gst']
                    )


def calculate_charge(units: float, unit_rate: float) -> Charge:
    """ Calculate the billing charge

    units: The number of units to be charged
    unit_rate: The unit rate
    """
    cost_excl_gst = unit_rate * units
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    return Charge(units, unit_rate, cost_excl_gst, gst, cost_incl_gst)


def electricity_charges_general(retailer: str, days: int, usage: float, fy='2016'):
    """ Calculate electricity charges for a general tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    usage: The energy usage in kWh for the billing period
    """

    GeneralTariff = namedtuple('GeneralTariff',
                               ['supply_charge', 'all_usage', 'total_charges']
                               )

    rates = get_tariff_rates('t11', retailer, fy)
    supply_charge = calculate_charge(days, rates.supply_charge)
    all_usage = calculate_charge(usage, rates.offpeak)
    cost_excl_gst = supply_charge.cost_excl_gst + all_usage.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return GeneralTariff(supply_charge, all_usage, total_charges)


def electricity_charges_tou(retailer: str, days: int, peak: float, shoulder: float, offpeak: float, fy='2016'):
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

    rates = get_tariff_rates('t12', retailer, fy)
    supply_charge = calculate_charge(days, rates.supply_charge)
    peak = calculate_charge(peak, rates.peak)
    shoulder = calculate_charge(shoulder, rates.shoulder)
    offpeak = calculate_charge(offpeak, rates.offpeak)
    cost_excl_gst = supply_charge.cost_excl_gst + peak.cost_excl_gst + \
        shoulder.cost_excl_gst + offpeak.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUTariff(supply_charge, peak, shoulder, offpeak, total_charges)


def electricity_charges_tou_demand(retailer, days, usage, demand, fy='2016', peak_season=True):
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

    rates = get_tariff_rates('t14', retailer, fy)
    supply_charge = calculate_charge(days, rates.supply_charge)
    all_usage = calculate_charge(usage, rates.offpeak)
    if peak_season:
        monthly_rate = pro_rata_monthly_charge(
            rates.demand_peak, days)
    else:
        monthly_rate = pro_rata_monthly_charge(
            rates.demand_shoulder, days)
        # Set chargeable demand to minimum kW value
        if demand < rates.demand_shoulder_min:
            demand = rates.demand_shoulder_min
    demand_cost = calculate_charge(demand, monthly_rate)
    cost_excl_gst = supply_charge.cost_excl_gst + \
        all_usage.cost_excl_gst + demand_cost.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUDTariff(supply_charge, all_usage, demand_cost, total_charges)


def pro_rata_monthly_charge(monthly_charge: float, days: int) -> float:
    """ The monthly or annual charges shall be calculated pro rata having
    regard to the number of days in the billing cycle that supply was
    connected (days) and one-twelfth of 365.25 days (to allow for leap years).

    monthly_charge: The monthly charge
    days: The number of days in the billing period
    """
    daily_charge = (monthly_charge * 12) / 365.25
    return daily_charge * days
