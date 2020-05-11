import os
from typing import List, NamedTuple
import pytoml as toml
from datetime import datetime, time


class ToUTimes(NamedTuple):
    """ Represents Time of Use Times """

    tou_desc: str
    peak_months: List[int]
    peak_days: List[int]
    peak_start: time
    peak_end: time
    shoulder_months: List[int]
    shoulder_days: List[int]
    shoulder_start: time
    shoulder_end: time

    def __repr__(self) -> str:
        return f"<ToU {self.tou_desc}>"


def get_tou_times(tou_desc: str = "qld-regional") -> ToUTimes:
    """ Load usage periods from config file

    :param tou_desc: Name of ToU config
    """
    mydir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(mydir, "toutimes.toml")

    with open(config_file, "rb") as stream:
        periods = toml.load(stream)

    peak_months = periods[tou_desc].get("peak_months", [])
    peak_days = periods[tou_desc].get("peak_days", [])
    peak_start = periods[tou_desc].get("peak_start", time(0, 0, 0))
    peak_start = datetime.strptime(peak_start, "%H:%M").time()
    peak_end = periods[tou_desc].get("peak_end", time(0, 0, 0))
    peak_end = datetime.strptime(peak_end, "%H:%M").time()

    shoulder_months = periods[tou_desc].get("shoulder_months", [])
    shoulder_days = periods[tou_desc].get("shoulder_days", [])
    shoulder_start = periods[tou_desc].get("shoulder_start", time(0, 0, 0))
    shoulder_start = datetime.strptime(shoulder_start, "%H:%M").time()
    shoulder_end = periods[tou_desc].get("shoulder_end", time(0, 0, 0))
    shoulder_end = datetime.strptime(shoulder_end, "%H:%M").time()

    return ToUTimes(
        tou_desc,
        peak_months,
        peak_days,
        peak_start,
        peak_end,
        shoulder_months,
        shoulder_days,
        shoulder_start,
        shoulder_end,
    )


class Tariff(NamedTuple):
    """ Represents a Tariff """

    tariff: str
    retailer: str
    fy: str
    supply_charge: float
    offpeak: float
    shoulder: float
    peak: float
    demand_peak: float
    demand_shoulder: float
    demand_shoulder_min: float
    tou_desc: str
    tou_times: ToUTimes

    def __repr__(self) -> str:
        return f"<Tariff {self.tariff} {self.retailer} {self.fy}>"


def get_tariff_rates(
    tariff: str = "t12", retailer: str = "ergon", fy: str = "2017"
) -> Tariff:
    """ Load tariff rates from config file

    :param tariff: Name of tariff from config
    :param retailer: Name of retailer to get costs from
    :param fy: FY (ending) to get costs from
    """

    mydir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(mydir, "prices.toml")

    with open(config_file, "rb") as stream:
        prices = toml.load(stream)

    retailer_rates = prices[tariff][retailer]
    try:
        fy_rates = retailer_rates[fy]
    except KeyError:
        if int(fy) < 2017:
            fy_rates = retailer_rates["2017"]
        else:
            fy_rates = retailer_rates["2019"]

    supply_charge = fy_rates["supply_charge"]
    try:
        peak = fy_rates["peak_usage"]
    except KeyError:
        peak = fy_rates["usage"]
    try:
        shoulder = fy_rates["shoulder_usage"]
    except KeyError:
        shoulder = fy_rates["usage"]
    try:
        offpeak = fy_rates["offpeak_usage"]
    except KeyError:
        offpeak = fy_rates["usage"]

    demand_peak = fy_rates.get("demand_peak", 0.0) * 100
    demand_shoulder = fy_rates.get("demand_shoulder", 0.0) * 100
    demand_shoulder_min = fy_rates.get("demand_shoulder_min", 3.0)
    tou_desc = fy_rates.get("tou_def", "qld-regional")
    tou_times = get_tou_times(tou_desc)

    return Tariff(
        tariff,
        retailer,
        fy,
        supply_charge,
        offpeak,
        shoulder,
        peak,
        demand_peak,
        demand_shoulder,
        demand_shoulder_min,
        tou_desc,
        tou_times,
    )
