""" Test Suite
"""

import unittest
import datetime
from qldtariffs import get_daily_usages, get_billing_end


PEAK_RECORDS = [
    (datetime.datetime(2017, 1, 2, 0, 0),
     datetime.datetime(2017, 1, 3, 0, 0), 480),
    (datetime.datetime(2017, 1, 3, 0, 0),
     datetime.datetime(2017, 1, 3, 0, 30), 10),
    (datetime.datetime(2017, 1, 3, 0, 30),
     datetime.datetime(2017, 1, 3, 0, 40), 3.3),
    (datetime.datetime(2017, 1, 3, 0, 40),
     datetime.datetime(2017, 1, 3, 0, 50), 3.3),
    (datetime.datetime(2017, 1, 3, 0, 50),
     datetime.datetime(2017, 1, 3, 1, 0), 3.3),
    (datetime.datetime(2017, 1, 3, 1, 0),
     datetime.datetime(2017, 1, 3, 1, 10), 3.3),
]

OFFPEAK_RECORDS = [
    (datetime.datetime(2017, 4, 1, 0, 0),
     datetime.datetime(2017, 4, 2, 0, 0), 480)
]


class TestGrouping(unittest.TestCase):
    """ Test tariff costs are grouped into daily usage correctly """

    def test_billing_end(self):
        """ Test billing dates are allocated correctly """
        billing_end = datetime.datetime(2017, 1, 1, 23, 40)
        check = datetime.datetime(2017, 1, 2, 0, 0)
        self.assertEqual(get_billing_end(billing_end), check)

        billing_end = datetime.datetime(2017, 1, 2, 0, 0)
        check = datetime.datetime(2017, 1, 2, 0, 0)
        self.assertEqual(get_billing_end(billing_end), check)

        billing_end = datetime.datetime(2017, 1, 2, 0, 20)
        check = datetime.datetime(2017, 1, 2, 0, 30)
        self.assertEqual(get_billing_end(billing_end), check)

        billing_end = datetime.datetime(2017, 1, 2, 0, 30)
        check = datetime.datetime(2017, 1, 2, 0, 30)
        self.assertEqual(get_billing_end(billing_end), check)

    def test_agl_peak(self):
        """ Test time of day usage for AGL on weekday """
        dailies = get_daily_usages(PEAK_RECORDS, 'AGL')
        test_day = dailies[datetime.date(2017, 1, 2)]
        self.assertAlmostEqual(test_day.all, 480, places=0)
        self.assertAlmostEqual(test_day.peak, 80, places=0)
        self.assertAlmostEqual(test_day.shoulder, 220, places=0)
        self.assertAlmostEqual(test_day.offpeak, 180, places=0)

    def test_agl_offpeak(self):
        """ Test time of day usage for AGL on weekend """
        dailies = get_daily_usages(OFFPEAK_RECORDS, 'AGL')
        test_day = dailies[datetime.date(2017, 4, 1)]
        self.assertAlmostEqual(test_day.all, 480, places=0)
        self.assertAlmostEqual(test_day.peak, 0, places=0)
        self.assertAlmostEqual(test_day.shoulder, 300, places=0)
        self.assertAlmostEqual(test_day.offpeak, 180, places=0)

    def test_ergon_peak(self):
        """ Test time of day usage for Ergon in peak season """
        dailies = get_daily_usages(PEAK_RECORDS, 'Ergon')
        test_day = dailies[datetime.date(2017, 1, 2)]
        self.assertAlmostEqual(test_day.all, 480, places=0)
        self.assertAlmostEqual(test_day.peak, 130, places=0)
        self.assertAlmostEqual(test_day.offpeak, 350, places=0)

    def test_ergon_offpeak(self):
        """ Test time of day usage for Ergon in offpeak season """
        dailies = get_daily_usages(OFFPEAK_RECORDS, 'Ergon')
        test_day = dailies[datetime.date(2017, 4, 1)]
        self.assertAlmostEqual(test_day.all, 480, places=0)
        self.assertAlmostEqual(test_day.peak, 0, places=0)
        self.assertAlmostEqual(test_day.offpeak, 480, places=0)
