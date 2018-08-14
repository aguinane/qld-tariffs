""" Test Suite
"""

import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))
from qldtariffs import calculate_charge
from qldtariffs import electricity_charges_general
from qldtariffs import electricity_charges_tou
from qldtariffs import electricity_charges_tou_demand


def test_charges():
    """ Test unit rate charges """
    assert calculate_charge(31, 60.514).cost_incl_gst == pytest.approx(2064, rel=1e-1)


def test_tariff_11():
    """ Test tariff 11 charges """
    charges = electricity_charges_general('ergon', 22, 142.50)
    assert charges.supply_charge.cost_incl_gst == pytest.approx(2168, rel=1e-1)
    assert charges.all_usage.cost_incl_gst == pytest.approx(3858, rel=1e-1)
    assert charges.total_charges.cost_incl_gst == pytest.approx(6025, rel=1e-1)


def test_tariff_12():
    """ Test tariff 12 charges """
    charges = electricity_charges_tou('ergon', 31, 75.49, 0, 109.5)
    assert charges.supply_charge.cost_incl_gst == pytest.approx(3455, rel=1e-1)
    assert charges.peak.cost_incl_gst == pytest.approx(4639, rel=1e-1)
    assert charges.shoulder.cost_incl_gst == pytest.approx(0, rel=1e-1)
    assert charges.offpeak.cost_incl_gst == pytest.approx(2392, rel=1e-1)
    assert charges.total_charges.cost_incl_gst == pytest.approx(
        10486, rel=1e-1)


def test_tariff_14():
    """ Test tariff 14 charges """
    charges = electricity_charges_tou_demand('ergon', 31, 183.92, 0.700, peak_season=True)
    assert charges.supply_charge.cost_incl_gst == pytest.approx(2064, rel=1e-1)
    assert charges.all_usage.cost_incl_gst == pytest.approx(3031, rel=1e-1)
    assert charges.demand.cost_incl_gst == pytest.approx(4846, rel=1e-1)
    assert charges.total_charges.cost_incl_gst == pytest.approx(9941, rel=1e-1)

    charges = electricity_charges_tou_demand('ergon', 31, 183.92, 0.700, peak_season=False)
    assert charges.supply_charge.cost_incl_gst == pytest.approx(2064, rel=1e-1)
    assert charges.all_usage.cost_incl_gst == pytest.approx(3031, rel=1e-1)
    assert charges.demand.cost_incl_gst == pytest.approx(3784, rel=1e-1)
    assert charges.total_charges.cost_incl_gst == pytest.approx(8879, rel=1e-1)
