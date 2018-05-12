"""
Support for WattBox outlet switches

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/light.ketra/
"""
import logging

from homeassistant.components.switch import SwitchDevice
from .. import wattbox
#(WattBoxDevice, WATTBOX_DEVICES, WATTBOX_CONTROLLER)

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['wattbox']

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the wattbox power strip switches."""
    devs = []
    for (area_name, device) in hass.data[wattbox.WATTBOX_DEVICES]['switch']:
        dev = WattBoxSwitch(area_name, device, hass.data[wattbox.WATTBOX_CONTROLLER])
        devs.append(dev)

    add_devices(devs, True)
    _LOGGER.warning("Added " + str(devs))
    return True


class WattBoxSwitch(wattbox.WattBoxDevice, SwitchDevice):
    """Representation of a WattBox outlet, just on and off."""

    def __init__(self, area_name, wattbox_switch, controller):
        """Initialize the light."""
        wattbox.WattBoxDevice.__init__(self, area_name, wattbox_switch, controller)
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
