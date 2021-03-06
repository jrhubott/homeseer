"""
Support for HomeSeer light-type devices.
"""

from pyhs3ng.device import GenericSwitchMultilevel
from .hoomseer import HomeseerEntity
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    SUPPORT_BRIGHTNESS,
    LightEntity,
)

from .const import DATA_CLIENT, _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer light-type devices."""
    light_devices = []
    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if issubclass(type(device), GenericSwitchMultilevel):
            dev = HSLight(device, homeseer)
            light_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer light-type device: {dev.name}")

    async_add_entities(light_devices)


class HSLight(HomeseerEntity, LightEntity):
    """Representation of a HomeSeer light-type device."""

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS

    @property
    def brightness(self):
        """Return the brightness of the light."""
        bri = self._device.dim_percent * 255
        if bri > 255:
            return 255
        return bri

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)
        percent = int(brightness / 255 * 100)
        await self._device.dim(percent)

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self._device.off()
