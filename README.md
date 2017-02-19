# qld-tariffs
Calculate the energy costs for QLD tariffs

# Usage

Get the monthly usage summaries from a set of energy usage records:
```
import datetime
from qldtariffs import get_daily_usages, get_monthly_usages

PEAK_RECORDS = [
    (datetime.datetime(2017, 1, 1, 0, 0),
     datetime.datetime(2017, 1, 2, 0, 0), 480),
    (datetime.datetime(2017, 1, 2, 0, 0),
     datetime.datetime(2017, 1, 3, 0, 0), 480)
]

month_summaries = get_monthly_usages(PEAK_RECORDS, 'Ergon')
for month in sorted(month_summaries):
    print(month, month_summaries[month])
```

Will output:
```
(2017, 1) MonthUsage(days=31, peak=260.0, shoulder=0, offpeak=720.0, all=980.0, demand=1.5384615384615385)
```

Then use the usage stats to calculate the bill amount:
```
from qldtariffs import electricity_charges_general
print(electricity_charges_general('Ergon', days, usage_all))
```

Will yield:
```
GeneralTariff(supply_charge=Charge(units=31, unit_rate=89.572, cost_excl_gst=2776.732, gst=277.6732, cost_incl_gst=3054.4052), all_usage=Charge(units=980.0, unit_rate=24.61,
cost_excl_gst=24117.8, gst=2411.78, cost_incl_gst=26529.579999999998), total_charges=Charge(units=None, unit_rate=None, cost_excl_gst=26894.532, gst=2689.4532, cost_incl_gst=
29583.9852))
```

In addition to the general tariff, you can also calculate time of use tariffs:
```
from qldtariffs import electricity_charges_tou
from qldtariffs import electricity_charges_tou_demand
```
