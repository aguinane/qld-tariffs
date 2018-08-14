""" Test Suite
"""


import pytest
import datetime
from nemreader import read_nem_file
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from qldtariffs import get_daily_usages, get_monthly_usages

INTERVAL_READINGS = read_nem_file(
    'examples/example_NEM12.csv').readings['3044076134']['E1']
MANUAL_READINGS = read_nem_file(
    'examples/example_NEM13.csv').readings['3044076134']['11']


def test_nem12_data_daily():
    """ Test example NEM12 daily summary """
    daily_summaries = get_daily_usages(INTERVAL_READINGS, 'ergon', 't14')
    dec1 = daily_summaries[datetime.date(2016, 12, 1)]
    assert dec1.all == pytest.approx(6.29)

    daily_summaries = get_daily_usages(INTERVAL_READINGS, 'ergon', 't14')
    dec1 = daily_summaries[datetime.date(2016, 9, 6)]
    assert dec1.all == pytest.approx(7.17)


def test_nem12_data_monthly():
    """ Test example NEM12 monthly summary """
    month_summaries = get_monthly_usages(INTERVAL_READINGS, 'ergon', 't14')
    dec = month_summaries[(2016, 12)]
    assert dec.days == pytest.approx(31)
    assert dec.all == pytest.approx(176.64)


def test_nem13_data():
    """ Test example NEM13 summary """
    month_summaries = get_monthly_usages(MANUAL_READINGS, 'ergon', 't11')
    july = month_summaries[(2016, 7)]
    assert july.days == pytest.approx(31)
    assert july.all == pytest.approx(208, rel=1e-1)
