""" Test Suite
"""

import unittest
import datetime
from qldtariffs import get_billing_end, billing_intervals
from qldtariffs import get_daily_usages, get_monthly_usages


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


    def test_interval_splitting(self):
        """ Test months are grouped correctly """
        start_date = datetime.datetime(2016, 12, 31, 0, 0)
        end_date = datetime.datetime(2017, 1, 1, 0, 0)
        split = list(billing_intervals(start_date, end_date))
        self.assertEqual(len(split), 48)
        first_interval = start_date + datetime.timedelta(seconds=30 * 60)
        self.assertEqual(split[0], first_interval)
        self.assertEqual(split[-1], end_date)


    def test_month_grouping(self):
        """ Test months are grouped correctly """
        records = [(datetime.datetime(2016, 12, 1, 0, 0),
                    datetime.datetime(2017, 1, 1, 0, 0), 480)
                   ]
        months = list(get_monthly_usages(records, 'Ergon', 'T14').keys())
        self.assertEqual(len(months), 1)
        self.assertEqual(months, [(2016, 12)])

        records = [(datetime.datetime(2016, 12, 1, 0, 0),
            datetime.datetime(2017, 2, 1, 0, 0), 480)
            ]
        months = list(get_monthly_usages(records, 'Ergon', 'T14').keys())
        self.assertEqual(len(months), 2)
        self.assertEqual(sorted(months), [(2016, 12), (2017, 1)])

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
