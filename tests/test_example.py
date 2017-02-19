""" Test Suite
"""

import unittest
import datetime
from nemreader import MeterRecord
from qldtariffs import get_monthly_usages, get_daily_usages

INTERVAL_READINGS = MeterRecord('examples/example_NEM12.csv').readings['E1']
MANUAL_READINGS = MeterRecord('examples/example_NEM13.csv').readings['11']


class TestGrouping(unittest.TestCase):
    """ Test tariff costs are grouped into daily usage correctly """

    def test_nem12_data(self):
        """ Test example NEM12 summary """
        daily_summaries = get_daily_usages(INTERVAL_READINGS, 'Ergon', 'T14')
        dec1 = daily_summaries[datetime.date(2016, 12, 1)]
        self.assertAlmostEqual(dec1.all, 6.3, places=1)
        self.assertAlmostEqual(dec1.peak, dec1.demand, places=2)

        month_summaries = get_monthly_usages(INTERVAL_READINGS, 'Ergon', 'T14')
        dec = month_summaries[(2016,12)]
        self.assertAlmostEqual(dec.days, 31, places=0)
        self.assertAlmostEqual(dec.all, 176.64, places=0)
        self.assertAlmostEqual(dec.demand, 0.730, places=2)

    def test_nem13_data(self):
        """ Test example NEM13 summary """
        month_summaries = get_monthly_usages(MANUAL_READINGS, 'Ergon', 'T11')
        july = month_summaries[(2016,7)]
        self.assertAlmostEqual(july.days, 31, places=0)
        self.assertAlmostEqual(july.all, 208, places=0)

