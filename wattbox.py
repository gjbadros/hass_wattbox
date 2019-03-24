"""
Component for interacting with a WattBox ip-controlled power strip.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/wattbox/
"""
import asyncio
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD, CONF_DEVICES
from homeassistant.const import CONF_PAYLOAD_OFF, CONF_PAYLOAD_ON
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pywattbox==0.0.2']

DOMAIN = 'wattbox'
DEVICES = 'wattbox_devices'

_LOGGER = logging.getLogger(__name__)

CONF_AREA = 'area'
CONF_SWITCH_NOOP = 'switch_noop'

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional("area"): cv.string, #FIXME
    vol.Optional("noop_set_state"): cv.boolean, #FIXME
})

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_DEVICES): vol.All(cv.ensure_list, [DEVICE_SCHEMA])
    }),
}, extra=vol.ALLOW_EXTRA)


def setup(hass, config):
    """Set up the WattBox component."""
    from pywattbox import WattBox

    wattboxes = []

    hass.data[DEVICES] = {'switch': []}

    for index, wb_config in enumerate(config[DOMAIN][CONF_DEVICES]):
        host = wb_config.get(CONF_HOST)
        username = wb_config.get(CONF_USERNAME)
        password = wb_config.get(CONF_PASSWORD)
        area = wb_config.get(CONF_AREA)
        noop = wb_config.get(CONF_SWITCH_NOOP)

        wattbox = WattBox(host, username, password, area, noop)
        wattboxes.append(wattbox)
        wattbox.load_xml()
        _LOGGER.info("Loaded config from Wattbox at %s", host)
        for switch in wattbox.switches:
            _LOGGER.info("adding switch %s (%s)", switch, str(wattbox))
            hass.data[DEVICES]['switch'].append((area, switch, wattbox))
    
    hass.data[DOMAIN] = wattboxes
    
    discovery.load_platform(hass, 'switch', DOMAIN, None, config)

    return True


# The only device type now is a switch but we keep this here anyway
class WattBoxDevice(Entity):
    """Representation of a wattbox device entity."""

    def __init__(self, area_name, wattbox_switch, controller):
        """Initialize the device."""
        self._wattbox_switch = wattbox_switch
        self._controller = controller
        self._area_name = area_name
        self._unique_id = 'wattbox-{}-{}'.format(wattbox_switch._wattbox._serial_number,
                                                 wattbox_switch._outlet_num)

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Register callbacks."""

    def _update_callback(self, _switch):
        """Run when invoked by pywattbox when the device state changes."""
        self.schedule_update_ha_state()

    @property
    def name(self):
        """Return the name of the device."""
        return "{} {}".format(self._area_name, self._wattbox_switch.name)

    @property
    def should_poll(self):
        """No polling needed."""
        return True

    @property
    def unique_id(self):
        """Unique ID of wattbox device -- uses serial number and outlet number."""
        return self._unique_id

    
