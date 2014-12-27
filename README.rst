Helsingin Energia electricity usage scraper
===========================================

This small script fetches per-hour electricity usage from Helsingin
Energia (Helen) website. This is unofficial implementation which may
break at any time, if Helen changes their website or implements any
additional validations.

Installation:

::

  pip install helen_electricity_usage

Usage:

::

  import helen_electricity_usage
  helen = helen_electricity_usage.Helen(username, password, metering_point_number)
  helen.login()
  print helen.get_date("20141225")

To obtain username and password, register using `web interface
<https://www2.helen.fi/raportointi/>`_ (Flash and paper invoice is
required). After registering and signing in, metering point number is
available on the top-right corner.

Sample output (python dictionary):

::

  [ {
    "milestones" : [ ],
    "month" : 12,
    "value" : 0.22999,
    "year" : 2014,
    "day" : 25,
    "hour" : 0
  }, {
    "milestones" : [ ],
    "month" : 12,
    "value" : 0.15,
    "year" : 2014,
    "day" : 25,
    "hour" : 1
  }...
  ]

There is no way to check whether data for specific date is available. If
data is not available, all fields are provided, but values are 0.0.
There is no way to distinct between missing data and hours with no
electricity consumption. Usually the data is available next day, but
that is not guaranteed.
