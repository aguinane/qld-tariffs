""" Test Suite
"""

import unittest
from context import qldtariffs

class TestCharges(unittest.TestCase):
    """ Test tariff costs are calculated correctly """

    def test_charges(self):
        """ Test unit rate charges """
        self.assertAlmostEqual(qldtariffs.calculate_charge(31, 60.514).cost_incl_gst, 2064, places=0)


    def test_tariff_11(self):
        """ Test tariff 11 charges """
        charges = qldtariffs.electricity_charges_general('Ergon', 22, 142.50)
        self.assertAlmostEqual(charges.supply_charge.cost_incl_gst, 2168, places=0)
        self.assertAlmostEqual(charges.all_usage.cost_incl_gst, 3858, places=0)
        self.assertAlmostEqual(charges.total_charges.cost_incl_gst, 6025, places=0)

    def test_tariff_12(self):
        """ Test tariff 12 charges """
        charges = qldtariffs.electricity_charges_tou('Ergon', 31, 75.49, 0, 109.5)
        self.assertAlmostEqual(charges.supply_charge.cost_incl_gst, 3455, places=0)
        self.assertAlmostEqual(charges.peak.cost_incl_gst, 4639, places=0)
        self.assertAlmostEqual(charges.shoulder.cost_incl_gst, 0, places=0)
        self.assertAlmostEqual(charges.offpeak.cost_incl_gst, 2392, places=0)
        self.assertAlmostEqual(charges.total_charges.cost_incl_gst, 10486, places=0)

    def test_tariff_14(self):
        """ Test tariff 14 charges """
        charges = qldtariffs.electricity_charges_tou_demand('Ergon', 31, 183.92, 0.700, True)
        self.assertAlmostEqual(charges.supply_charge.cost_incl_gst, 2064, places=0)
        self.assertAlmostEqual(charges.all_usage.cost_incl_gst, 3031, places=0)
        self.assertAlmostEqual(charges.demand.cost_incl_gst, 4846, places=0)
        self.assertAlmostEqual(charges.total_charges.cost_incl_gst, 9941, places=0)

        charges = qldtariffs.electricity_charges_tou_demand('Ergon', 31, 183.92, 0.700, False)
        self.assertAlmostEqual(charges.supply_charge.cost_incl_gst, 2064, places=0)
        self.assertAlmostEqual(charges.all_usage.cost_incl_gst, 3031, places=0)
        self.assertAlmostEqual(charges.demand.cost_incl_gst, 3784, places=0)
        self.assertAlmostEqual(charges.total_charges.cost_incl_gst, 8879, places=0)
