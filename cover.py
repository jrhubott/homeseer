"""
Support for HomeSeer cover-type devices.
"""

from .pyhs3ng.device import GenericCover
from .hoomseer import HomeseerEntity

from homeassistant.components.cover import CoverEntity
from homeassistant.const import STATE_CLOSED, STATE_CLOSING, STATE_OPENING

from .const import _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer cover-type devices."""
    cover_devices = []
    homeseer = hass.data[DOMAIN]

    for device in homeseer.devices:
        if issubclass(type(device), GenericCover):
            dev = HSCover(device, homeseer)
            cover_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer cover-type device: {dev.name}")

    async_add_entities(cover_devices)


class HSCover(HomeseerEntity, CoverEntity):
    """Representation of a HomeSeer cover-type device."""

    def __init__(self, device, connection):
        self._device = device
        self._connection = connection

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return self._device.current_state == STATE_OPENING

    @property
    def is_closing(self):
        """Return if the cover is closing or not."""
        return self._device.current_state == STATE_CLOSING

    @property
    def is_closed(self):
        """Return if the cover is closed or not."""
        return self._device.current_state == STATE_CLOSED

    async def async_open_cover(self, **kwargs):
        await self._device.open()

    async def async_close_cover(self, **kwargs):
        await self._device.close()
