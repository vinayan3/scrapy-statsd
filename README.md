# Scrapy-Statsd
Publish Scrapy stats to statsd daemon to see your spider stats in real time.

**Table of Contents**

- [Details](#details)
	- [Stat Names](#stat-names)
	- [Value Types](#value-types)
	- [Start Ignored for Counters](#start-ignored-for-counters)
- [Installation](#installation)

# Details
Exporting scrapy's metrics into statsd required was not a perfect one to one mapping. The naming conventions and values some adjustment. Please, see them below. 
## Stat Names
The stats will be transformed from the forward slashed notation that is commonly seen on  stats dumps to a more common dotted notation for statsd. Furthermore, if there is a spider present it will be prefixed to the stat name. For instance:

| Scrapy Notation | StatsD Notation  |
|---|---|
|downloader/exception_count |downloader.exception_count   |
|downloader/exception_type_count/twisted.internet.error.DNSLookupError|downloader.exception_type_count.twisted.internet.error.DNSLookupError   |
|downloader/request_count|downloader.request_count   |
|downloader/response_status_count/200   |downloader.response_status_count.200   |

## Value Types
Only numeric types are exported to statsd. No other types are exported. One might be inclined why set_value is not translated into a set within statsd. There is a mismatch in the purpose of setting a non-numeric value from scarpy to statsd. The statsd set counts the number of unique items. This is fundamentally different than setting a value with Scrapy's default stats module.

## Start Ignored for Counters
The operations increment or decrement do not use the parameter start. Scrapy has a notion that the stats are being collected in a single dictionary where you can check if the value has been set. Statsd doesn't act like a key value store. There is no mechanism to check if a value has been set for a given metric.
 
# Installation
1. Clone the repo into a location which is on the `PYTHONPATH` 
```
git clone git@github.com:vinayan3/scrapy-statsd.git
```

1. Pip install dependencies
```
cd ~/work/scrapy-statsd/scrapy_statds
pip install -r requirements.txt
```
_Note:The requirements state Scrapy version 1.05 but that'll be reduce once testing is done._

1. Add the following lines to your `settings.py` of your Scrapy project 
```
STATS_CLASS = 'scrapy_statsd.statscollectors.StatsDStatsCollector'
 
STATSD_HOST = 'localhost'
STATSD_PORT = 8125
```

_Note: This process will get better once I get this into pip._