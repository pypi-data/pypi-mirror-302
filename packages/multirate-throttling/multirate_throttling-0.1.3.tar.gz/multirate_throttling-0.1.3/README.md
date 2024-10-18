# MULTIRATE THROTTLING

This module provides a multirate parent throttle for Django Rest Framework (DRF) with optional support for [Constance](https://django-constance.readthedocs.io/).

The multirate settings prevents from adding several throttle classes for each rate when the scope could be the same.  

The use of Constance allows the dynamic change of the throttling rates on the fly.  

It supports the use of a white list of IP addresses that are not subject to the throttle.

## Dependencies

- Django
- Django Rest Framework
- Constance (Optionally)

## Installation

`pip install multirate-throttling`

## Usage
The list of rates for a scope can we defined as a comma-separated list of rates. 

A single rate can be defined as a "number/time_unit" where 'number' if the maximum number of requests in the specified 'unit time': 5/day

The unit time can be one of the following: sec, min, hour, day, week. Actually, only the first letter of the unit matters, so you can also use: s, m, h, d, w

Example of a valid list of rates for a scope: "15/s, 20/day, 50/we" 

NOTES:
- Should a time unit be repeated, only the last occurrence would be applied.
- Should a rate in the list be wrong, that rate will be ignored and its value logged.

## Settings

You can store each scope's settings in two places:

 - As a standard DRF throttle, adding the scope and rate list to the 'DEFAULT_THROTTLE_RATES' key of 'REST_FRAMEWORK' in Django settings
 - In Constance, prepending 'THROTTLE_RATE_' to the scope's name in *UPPER CASE* and adding it to the Constance config as a key with the rate list as its value. Later, you will be able to change the rate list on the fly at any time.

As the usage of Constance is optional, you must add the following variable to Django Settings to enable it:

***
    MULTIRATE_THROTTLING_USE_CONSTANCE = True
***

### Examples

- As a DRF standard throttle setting:
---
    REST_FRAMEWORK = {
        'THROTTLE_RATE_WHITE_LIST': ['127.0.0.1', ],
        'DEFAULT_THROTTLE_RATES': {
            'some_scope': '5/sec, 50/min, 100/hour, 500/day, 100/week',
        }
    }
---

- As a Constance config:
---
    MULTIRATE_THROTTLING_USE_CONSTANCE = True
    CONSTANCE_CONFIG = {
        'THROTTLE_RATE_WHITE_LIST': '127.0.0.1, 127.0.0.2',
        'THROTTLE_RATE_SOME_SCOPE': '5/sec, 50/min, 100/hour, 500/day, 100/week',
    }
---

  
