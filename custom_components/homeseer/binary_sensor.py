"""
Support for HomeSeer binary-type devices.
"""

from pyhs3ng.device import GenericBinarySensor

from .hoomseer import HomeseerEntity
from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    DEVICE_CLASS_DOOR,
    DEVICE_CLASS_WINDOW,
    DEVICE_CLASS_MOTION,
    DEVICE_CLASS_GARAGE_DOOR,
    DEVICE_CLASS_SMOKE,
    DEVICE_CLASS_GAS,
    DEVICE_CLASS_VIBRATION,
)


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

    _device_class = None

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)

        name = self._device.name.lower()

        if "window" in name:
            self._device_class = DEVICE_CLASS_WINDOW

        if "garage" in name:
            self._device_class = DEVICE_CLASS_GARAGE_DOOR

        if "door" in name:
            self._device_class = DEVICE_CLASS_DOOR

        if "entry" in name:
            self._device_class = DEVICE_CLASS_DOOR

        if "garage door" in name:
            self._device_class = DEVICE_CLASS_GARAGE_DOOR

        if "motion" in name:
            self._device_class = DEVICE_CLASS_MOTION

        if "fire" in name:
            self._device_class = DEVICE_CLASS_SMOKE

        if "smoke" in name:
            self._device_class = DEVICE_CLASS_SMOKE

        if "monoxide" in name:
            self._device_class = DEVICE_CLASS_GAS

        if "glass break" in name:
            self._device_class = DEVICE_CLASS_VIBRATION

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.value > 0

    @property
    def device_class(self):
        return self._device_class