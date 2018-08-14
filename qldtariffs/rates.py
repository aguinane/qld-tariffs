import os
from typing import List, NamedTuple
import pytoml as toml
from datetime import datetime, time


class Tariff(NamedTuple):
    """ Represents a Tariff """
    tariff: str
    retailer: str
    fy: str
    supply_charge: float
    offpeak: float
    shoulder: float
    peak: float
    peak_months: List[int]
    peak_days: List[int]
    peak_start: time
    peak_end: time
    shoulder_months: List[int]
    shoulder_days: List[int]
    shoulder_start: time
    shoulder_end: time
    demand_peak: float
    demand_shoulder: float
    demand_shoulder_min: float

    def __repr__(self) -> str:
        return f'<Tariff {self.tariff} {self.retailer} {self.fy}>'


def get_tariff_rates(tariff: str='t12', retailer: str='ergon', fy: str='2016'):
    """ Load tariff rates from config file

    :param tariff: Name of tariff from config
    :param retailer: Name of retailer to get costs from
    :param fy: FY (starting) to get costs from
    """

    mydir = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(mydir, 'prices.toml')

    with open(config_file, 'rb') as stream:
        prices = toml.load(stream)

    retailer_rates = prices[tariff][retailer]
    fy_rates = retailer_rates[fy]

    supply_charge = fy_rates['supply_charge']
    try:
        peak = fy_rates['peak_usage']
    except KeyError:
        peak = fy_rates['usage']
    try:
        shoulder = fy_rates['shoulder_usage']
    except KeyError:
        shoulder = fy_rates['usage']
    try:
        offpeak = fy_rates['offpeak_usage']
    except KeyError:
        offpeak = fy_rates['usage']

    try:
        periods = fy_rates['periods']
    except KeyError:
        periods = 'ergon-periods'

    try:
        peak_months = prices[periods]['peak_months']
    except KeyError:
        peak_months = []
    try:
        peak_days = prices[periods]['peak_days']
    except KeyError:
        peak_days = []
    try:
        peak_start = prices[periods]['peak_start']
        peak_start = datetime.strptime(peak_start, '%H:%M').time()
    except KeyError:
        peak_start = time(0, 0, 0)
    try:
        peak_end = prices[periods]['peak_end']
        peak_end = datetime.strptime(peak_end, '%H:%M').time()
    except KeyError:
        peak_end = time(0, 0, 0)

    try:
        shoulder_months = prices[periods]['shoulder_months']
    except KeyError:
        shoulder_months = []
    try:
        shoulder_days = prices[periods]['shoulder_days']
    except KeyError:
        shoulder_days = []
    try:
        shoulder_start = prices[periods]['shoulder_start']
        shoulder_start = datetime.strptime(shoulder_start, '%H:%M').time()
    except KeyError:
        shoulder_start = time(0, 0, 0)
    try:
        shoulder_end = prices[periods]['shoulder_end']
        shoulder_end = datetime.strptime(shoulder_end, '%H:%M').time()
    except KeyError:
        shoulder_end = time(0, 0, 0)

    try:
        demand_peak = fy_rates['demand_peak'] * 100
    except KeyError:
        demand_peak = 0.0
    try:
        demand_shoulder = fy_rates['demand_shoulder'] * 100
    except KeyError:
        demand_shoulder = 0.0
    try:
        demand_shoulder_min = fy_rates['demand_shoulder_min']
    except KeyError:
        demand_shoulder_min = 3.0

    return Tariff(tariff, retailer, fy,
                  supply_charge, offpeak, shoulder, peak,
                  peak_months, peak_days, peak_start, peak_end,
                  shoulder_months, shoulder_days, shoulder_start, shoulder_end,
                  demand_peak, demand_shoulder, demand_shoulder_min
                  )
