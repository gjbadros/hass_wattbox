"""
Support for WattBox outlet switches

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.ketra/
"""
import logging

from homeassistant.components.switch import SwitchDevice
from ..wattbox import WattBoxDevice, WATTBOX_DEVICES, WATTBOX_CONTROLLER

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['wattbox']

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the wattbox power strip switches."""
    devs = []
    for (area_name, device, wattbox) in hass.data[DEVICES]['switch']:
        dev = WattBoxSwitch(area_name, device, wattbox)
        devs.append(dev)

    add_devices(devs, True)
    _LOGGER.warning("Added " + str(devs))
    return True


class WattBoxSwitch(WattBoxDevice, SwitchDevice):
    """Representation of a WattBox outlet, just on and off."""

    def __init__(self, area_name, wattbox_switch, controller):
        """Initialize the light."""
        WattBoxDevice.__init__(self, area_name, wattbox_switch, controller)
        self._prev = None

    def turn_on(self, **kwargs):
        """Turn the switch on."""
        self._wattbox_switch._set_state(True)
        self.schedule_update_ha_state()
        

    def turn_off(self, **kwargs):
        """Turn the light off."""
        self._wattbox_switch._set_state(False)
        self.schedule_update_ha_state()

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._wattbox_switch._on

    def update(self):
        """Call when forcing a refresh of the device."""
        if self._wattbox_switch.update():
            self.schedule_update_has_state()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        attr['Controller'] = str(self._controller)
        return attr
