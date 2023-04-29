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

  from datetime import datetime, timezone
  import helen_electricity_usage
  helen = helen_electricity_usage.Helen(username, password, delivery_site_id)
  helen.login()
  begin = datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc)
  end = datetime(year=2023, month=1, day=1, hour=23, minute=59, second=59, tzinfo=timezone.utc)
  print(helen.get_electricity(begin, end))

To obtain username and password, register using `web interface
<https://www.helen.fi/kirjautuminen>`_ (paper invoice is required).
After registering and signing in, delivery site id is available on the URL of Sähkö/Electricity page as well as on the page
under Käyttöpaikka/Consumption location

::
  https://web.omahelen.fi/personal/reports/electricity-consumption?location=<delivery_site_id>&resolution=month&date=2023-01-01


Sample output (python dictionary):

::

  {
    "intervals": {
      "electricity": [
        {
          "start": "2022-12-24T00:00:00+00:00",
          "stop": "2022-12-24T23:59:59+00:00",
          "resolution_s": 3600,
          "resolution": "hour",
          "unit": "kWh",
          "measurements": [
            {
              "value": 0.11,
              "status": "valid"
            },
            {
              "value": 0.12,
              "status": "valid"
            },
            {
              "value": 0.11,
              "status": "valid"
            },
            {
              "value": 0.12,
              "status": "valid"
            },
            {
              "value": 0.11,
              "status": "valid"
            },
            {
              "value": 0.12,
              "status": "valid"
            },
            {
              "value": 0.79,
              "status": "valid"
            },
            {
              "value": 0.35,
              "status": "valid"
            },
            {
              "value": 0.28,
              "status": "valid"
            },
            {
              "value": 0.26,
              "status": "valid"
            },
            {
              "value": 0.21,
              "status": "valid"
            },
            {
              "value": 0.26,
              "status": "valid"
            },
            {
              "value": 1.08,
              "status": "valid"
            },
            {
              "value": 1.03,
              "status": "valid"
            },
            {
              "value": 0.39,
              "status": "valid"
            },
            {
              "value": 0.47,
              "status": "valid"
            },
            {
              "value": 3.33,
              "status": "valid"
            },
            {
              "value": 3.83,
              "status": "valid"
            },
            {
              "value": 1.19,
              "status": "valid"
            },
            {
              "value": 0.43,
              "status": "valid"
            },
            {
              "value": 0.4,
              "status": "valid"
            },
            {
              "value": 0.32,
              "status": "valid"
            },
            {
              "value": 0.13,
              "status": "valid"
            },
            {
              "value": 0.12,
              "status": "valid"
            }
          ]
        }
      ]
    }
  }

Missing data can be identified from the status being 'invalid' and value is 0.0.
Usually the data is available next day, but that is not guaranteed.
