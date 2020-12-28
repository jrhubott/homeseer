"""
Support for HomeSeer binary-type devices.
"""

from pyhs3ng.device import GenericBinarySensor

from .hoomseer import HomeseerEntity
from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DATA_CLIENT, _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer binary-type devices."""
    binary_sensor_devices = []
    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if issubclass(type(device), GenericBinarySensor):
            dev = HSBinarySensor(device, homeseer)
            binary_sensor_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer binary-senssor-type device: {dev.name}")

    async_add_entities(binary_sensor_devices)


class HSBinarySensor(HomeseerEntity, BinarySensorEntity):
    """Representation of a HomeSeer binary-type device."""

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.value > 0
