"""
Support for HomeSeer binary-type devices.
"""

from .pyhs3ng import HASS_BINARY_SENSORS, STATE_LISTENING

from .hoomseer import HomeseerEntity
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up HomeSeer binary-type devices."""
    binary_sensor_devices = []
    homeseer = hass.data[DOMAIN]

    for device in homeseer.devices:
        if device.device_type_string in HASS_BINARY_SENSORS:
            dev = HSBinarySensor(device, homeseer)
            binary_sensor_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer binary-sensor-type device: {dev.name}")

    async_add_entities(binary_sensor_devices)


class HSBinarySensor(HomeseerEntity, BinarySensorEntity):
    """Representation of a HomeSeer binary-type device."""

    def __init__(self, device, connection):
        self._device = device
        self._connection = connection

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.value > 0
