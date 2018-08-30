"""
Component for interacting with a WattBox ip-controlled power strip.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/wattbox/
"""
import asyncio
import logging

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_HOST, CONF_USERNAME, CONF_PASSWORD
from homeassistant.const import CONF_PAYLOAD_OFF, CONF_PAYLOAD_ON
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity

REQUIREMENTS = ['pywattbox==0.0.1']

DOMAIN = 'wattbox'

_LOGGER = logging.getLogger(__name__)

WATTBOX_CONTROLLER = 'wattbox_controller'
WATTBOX_DEVICES = 'wattbox_devices'

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional("area"): cv.string, #FIXME
        vol.Optional("noop_set_state"): cv.boolean, #FIXME
    })
}, extra=vol.ALLOW_EXTRA)


def setup(hass, base_config):
    """Set up the WattBox component."""
    from pywattbox import WattBox

    hass.data[WATTBOX_CONTROLLER] = None
    hass.data[WATTBOX_DEVICES] = {'switch': []}
    
    config = base_config.get(DOMAIN)
    area = config.get('area', 'wattbox')
    hass.data[WATTBOX_CONTROLLER] = WattBox(
        config[CONF_HOST], config[CONF_USERNAME],
        config[CONF_PASSWORD], area, config.get("noop_set_state"))

    hass.data[WATTBOX_CONTROLLER].load_xml()
    _LOGGER.info("Loaded config from Wattbox at %s", config[CONF_HOST])

    # Sort our devices into types
    for switch in hass.data[WATTBOX_CONTROLLER].switches:
        _LOGGER.info("adding switch %s", switch)
        hass.data[WATTBOX_DEVICES]['switch'].append((area, switch))

    discovery.load_platform(hass, 'switch', DOMAIN, None, base_config)
    return True


class WattBoxDevice(Entity):
    """Representation of a Ketra device entity."""

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

    
