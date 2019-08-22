hass_wattbox
============

By Greg J. Badros <badros@gmail.com>

For license information, see LICENSE -- use at your own risk.


This is a component for Home Assistant for the SnapAV(tm) Binary(tm) brand
of IP-controlled power outlets.

It relies on my pywattbox module at github at https://github.com/gjbadros/pywattbox
or PyPi (as pysnapavwattbox) at https://pypi.org/project/pysnapavwattbox/

Put these files in .homeassistant/custom_components/wattbox

And configure using a config like:

```
wattbox:
  devices:
    - host: 192.168.0.19
      username: !secret wattbox_user
      password: !secret wattobx_password
      area: 'Some area'
      exclude_name_substring: "SKIP"
    - host: 192.168.0.20
      username: !secret wattbox_user
      password: !secret wattobx_password
      area: 'Some area'
      exclude_name_substring: "OLD"
'''
