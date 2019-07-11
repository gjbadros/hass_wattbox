"""
Component for interacting with a WattBox(tm) (SnapAV) - brand
ip-controlled power strip.

For more details about this component, please refer to the documentation at
https://home-assistant.io/components/wattbox/
"""
import logging

from homeassistant.components.switch import SwitchDevice
from ..wattbox import WattBoxDevice, DEVICES

_LOGGER = logging.getLogger(__name__)

# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the wattbox power strip sensors."""
    devs = []
    for (area_name, wb) in hass.data[DEVICES]['sensor']:
        devs.append(WattBoxSensor(wb, area_name,
                                  "power", lambda c: c.power))
        devs.append(WattBoxSensor(wb, area_name,
                                  "current", lambda c: c.current))
        devs.append(WattBoxSensor(wb, area_name,
                                  "voltage", lambda c: c.voltage))

    add_devices(devs, True)
    _LOGGER.debug("Added wattbox sensors %s", devs)
    return True


class WattBoxSensor(WattBoxDevice, Entity):
    """Representation of a WattBox outlet, just on and off."""

    def __init__(self, controller, area_name, sensor_name, getter):
        """Initialize the light."""
        WattBoxDevice.__init__(self, area_name,
                               sensor_name,
                               sensor_name,
                               controller)
        self._prev = None
        self._getter = getter

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.getter()

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        attr = {}
        attr['Host'] = self._controller.host
        return attr
