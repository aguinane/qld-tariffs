""" Costs for each tariff are specified below (excl. GST)

Supply charges are in c/day
Usage charges are in c/kWh
Demand charges are in c/kW/month
"""

import datetime

# Tariff 11 - Residential
T11 = {
    'Ergon':    {'supply_charge': 95.846,
                 'usage_all': 28.479},
    'AGL':    {'supply_charge': 100.00,
               'usage_all': 26.00},
    'Origin':    {'supply_charge': 114.19,
                  'usage_all': 24.51},
}

# Tariff 12 - Time of Use
T12 = {
    'Ergon':    {'supply_charge': 98.833,
                 'usage_peak': 67.251,
                 'usage_shoulder': 23.177,
                 'usage_offpeak': 23.177,
                 'peak_start': datetime.time(15, 0, 0),
                 'peak_end': datetime.time(21, 30, 0),
                 'peak_months': [1, 2, 12],
                 'peak_days': [0, 1, 2, 3, 4, 5, 6]
                },
    'AGL':      {'supply_charge': 101.00,
                 'usage_peak': 35.00,
                 'usage_shoulder': 26.00,
                 'usage_offpeak': 22.00,
                 'peak_start': datetime.time(16, 0, 0),
                 'peak_end': datetime.time(20, 0, 0),
                 'peak_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 'peak_days': [1, 2, 3, 4, 5],
                 'shoulder_start': datetime.time(7, 0, 0),
                 'shoulder_end': datetime.time(22, 0, 0),
                 'shoulder_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 'shoulder_days': [0, 1, 2, 3, 4, 5, 6]
                },
    'Origin':    {'supply_charge': 114.19,
                  'usage_peak': 32.38,
                  'usage_shoulder': 23.24,
                  'usage_offpeak': 18.94,
                  'peak_start': datetime.time(16, 0, 0),
                  'peak_end': datetime.time(20, 0, 0),
                  'peak_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                  'peak_days': [1, 2, 3, 4, 5],
                  'shoulder_start': datetime.time(7, 0, 0),
                  'shoulder_end': datetime.time(22, 0, 0),
                  'shoulder_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                  'shoulder_days': [0, 1, 2, 3, 4, 5, 6]
                 },
}


# Tariff 14 - Time of Use (Demand)
T14 = {
    'Ergon': {
        'supply_charge': 50.324,
        'usage_all': 19.173,
        'demand_peak': 7240.0,
        'demand_offpeak': 1092.4,
        'demand_offpeak_min': 3,
        'peak_start': datetime.time(15, 0, 0),
        'peak_end': datetime.time(21, 30, 0),
        'peak_months': [1, 2, 12],
        'peak_days': [0, 1, 2, 3, 4, 5, 6]
    }
}
