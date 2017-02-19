""" Costs for each tariff are specified below (excl. GST)

Supply charges are in c/day
Usage charges are in c/kWh
Demand charges are in c/kW/month
"""

import datetime

# Tariff 11 - Residential
T11 = {
    'Ergon':    {'supply_charge': 89.572,
                 'usage_all': 24.610},
    'AGL':    {'supply_charge': 98.51,
               'usage_all': 24.61},
    'Origin':    {'supply_charge': 116.47,
                  'usage_all': 23.26},
}

# Tariff 12 - Time of Use
T12 = {
    'Ergon':    {'supply_charge': 101.306,
                 'usage_peak': 55.865,
                 'usage_shoulder': 19.859,
                 'usage_offpeak': 19.859,
                 'peak_start': datetime.time(15, 0, 0),
                 'peak_end': datetime.time(21, 30, 0),
                 'peak_months': [1, 2, 12],
                 'peak_days': [0, 1, 2, 3, 4, 5, 6]
                },
    'AGL':      {'supply_charge': 95.69,
                 'usage_peak': 29.79,
                 'usage_shoulder': 21.47,
                 'usage_offpeak': 17.49,
                 'peak_start': datetime.time(16, 0, 0),
                 'peak_end': datetime.time(20, 0, 0),
                 'peak_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 'peak_days': [1, 2, 3, 4, 5],
                 'shoulder_start': datetime.time(7, 0, 0),
                 'shoulder_end': datetime.time(22, 0, 0),
                 'shoulder_months': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 'shoulder_days': [0, 1, 2, 3, 4, 5, 6]
                },
    'Origin':    {'supply_charge': 116.47,
                  'usage_peak': 30.73,
                  'usage_shoulder': 22.15,
                  'usage_offpeak': 17.97,
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
        'supply_charge': 60.514,
        'usage_all': 14.984,
        'demand_peak': 6179.0,
        'demand_offpeak': 1125.8,
        'peak_start': datetime.time(15, 0, 0),
        'peak_end': datetime.time(21, 30, 0),
        'peak_months': [1, 2, 12],
        'peak_days': [0, 1, 2, 3, 4, 5, 6]
    }
}
