from typing import NamedTuple
from typing import Optional
from .rates import get_tariff_rates


class Charge(NamedTuple):
    """ Represents a charge """

    units: Optional[float]
    unit_rate: Optional[float]
    cost_excl_gst: float
    gst: float
    cost_incl_gst: float

    def __repr__(self) -> str:
        return f"<Charge {self.cost_incl_gst}c>"


def calculate_charge(units: float, unit_rate: float) -> Charge:
    """ Calculate the billing charge

    units: The number of units to be charged
    unit_rate: The unit rate
    """
    cost_excl_gst = unit_rate * units
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    return Charge(units, unit_rate, cost_excl_gst, gst, cost_incl_gst)


class GeneralTariff(NamedTuple):
    """ Represents a charge """

    supply_charge: Charge
    all_usage: Charge
    total_charges: Charge

    def __repr__(self) -> str:
        return f"<GeneralTariff {self.total_charges.cost_incl_gst}c>"


def electricity_charges_general(
    retailer: str, days: int, usage: float, fy="2017"
) -> GeneralTariff:
    """ Calculate electricity charges for a general tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    usage: The energy usage in kWh for the billing period
    fy: The financial year (ending) to get prices for
    """
    rates = get_tariff_rates("t11", retailer, fy)
    supply_charges = calculate_charge(days, rates.supply_charge)
    usage_charges = calculate_charge(usage, rates.offpeak)
    cost_excl_gst = supply_charges.cost_excl_gst + usage_charges.cost_excl_gst
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return GeneralTariff(supply_charges, usage_charges, total_charges)


class ToUTariff(NamedTuple):
    """ Represents a charge """

    supply_charge: Charge
    peak: Charge
    shoulder: Charge
    offpeak: Charge
    total_charges: Charge

    def __repr__(self) -> str:
        return f"<ToUTariff {self.total_charges.cost_incl_gst}c>"


def electricity_charges_tou(
    retailer: str, days: int, peak: float, shoulder: float, offpeak: float, fy="2017"
) -> ToUTariff:
    """ Calculate electricity charges for a time-of-use tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    peak: The energy usage in kWh for the peak billing period
    shoulder: The energy usage in kWh for the shoulder billing period
    offpeak: The energy usage in kWh for the off-peak billing period
    fy: The financial year (ending) to get prices for
    """

    rates = get_tariff_rates("t12", retailer, fy)
    supply_charges = calculate_charge(days, rates.supply_charge)
    peak_charges = calculate_charge(peak, rates.peak)
    shoulder_charges = calculate_charge(shoulder, rates.shoulder)
    offpeak_charges = calculate_charge(offpeak, rates.offpeak)
    cost_excl_gst = (
        supply_charges.cost_excl_gst
        + peak_charges.cost_excl_gst
        + shoulder_charges.cost_excl_gst
        + offpeak_charges.cost_excl_gst
    )
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUTariff(
        supply_charges, peak_charges, shoulder_charges, offpeak_charges, total_charges
    )


class ToUDTariff(NamedTuple):
    """ Represents a charge """

    supply_charge: Charge
    all_usage: Charge
    demand: Charge
    total_charges: Charge

    def __repr__(self) -> str:
        return f"<ToUDTariff {self.total_charges.cost_incl_gst}c>"


def electricity_charges_tou_demand(
    retailer: str,
    days: int,
    usage: float,
    demand: float,
    fy: str = "2017",
    peak_season: bool = True,
) -> ToUDTariff:
    """ Calculate electricity charges for a time-of-use tariff

    retailer: The name of the retailer to load rates from
    days: The number of days in the billing period
    usage: The energy usage in kWh for the billing period
    demand: The chargeable demand in kW
    fy: The financial year (ending) to get prices for
    peak_season: Do peak season rates apply
    """

    rates = get_tariff_rates("t14", retailer, fy)
    supply_charges = calculate_charge(days, rates.supply_charge)
    usage_charges = calculate_charge(usage, rates.offpeak)
    if peak_season:
        monthly_rate = pro_rata_monthly_charge(rates.demand_peak, days)
    else:
        monthly_rate = pro_rata_monthly_charge(rates.demand_shoulder, days)
        # Set chargeable demand to minimum kW value
        if demand < rates.demand_shoulder_min:
            demand = rates.demand_shoulder_min
    demand_charges = calculate_charge(demand, monthly_rate)
    cost_excl_gst = (
        supply_charges.cost_excl_gst
        + usage_charges.cost_excl_gst
        + demand_charges.cost_excl_gst
    )
    gst = cost_excl_gst * 0.1
    cost_incl_gst = cost_excl_gst + gst
    total_charges = Charge(None, None, cost_excl_gst, gst, cost_incl_gst)

    return ToUDTariff(supply_charges, usage_charges, demand_charges, total_charges)


def pro_rata_monthly_charge(monthly_charge: float, days: int) -> float:
    """ The monthly or annual charges shall be calculated pro rata having
    regard to the number of days in the billing cycle that supply was
    connected (days) and one-twelfth of 365.25 days (to allow for leap years).

    monthly_charge: The monthly charge
    days: The number of days in the billing period
    """
    daily_charge = (monthly_charge * 12) / 365.25
    return daily_charge * days
