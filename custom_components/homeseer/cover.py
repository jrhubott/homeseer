"""
Support for HomeSeer cover-type devices.
"""
import csv
from pyhs3ng.device import GenericCover
from .hoomseer import HomeseerEntity

from homeassistant.components.cover import (
    CoverEntity,
    ATTR_POSITION,
    DEVICE_CLASS_BLIND,
    DEVICE_CLASS_GARAGE,
    SUPPORT_CLOSE,
    SUPPORT_OPEN,
    SUPPORT_SET_POSITION,
)
from homeassistant.const import STATE_CLOSED, STATE_CLOSING, STATE_OPENING

from .const import DATA_CLIENT, _LOGGER, DOMAIN, CONF_FORCED_BLINDS

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer cover-type devices."""
    cover_devices = []

    forced_covers = list(
        map(int, config_entry.options.get(CONF_FORCED_BLINDS).split(","))
    )

    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if issubclass(type(device), GenericCover):
            dev = HSCover(device, homeseer)
            cover_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer cover-type device: {dev.name}")
        elif int(device.ref) in forced_covers:
            dev = HSBlind(device, homeseer)
            cover_devices.append(dev)
            _LOGGER.info(f"Force Added HomeSeer cover-type device: {dev.name}")

    async_add_entities(cover_devices)


class HSCover(HomeseerEntity, CoverEntity):
    """Representation of a HomeSeer cover-type device."""

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)


class HSBlind(HSCover):
    """Representation of a window-covering device."""

    @property
    def supported_features(self):
        """Return the features supported by the device."""
        return SUPPORT_OPEN | SUPPORT_CLOSE | SUPPORT_SET_POSITION

    @property
    def device_class(self):
        """Return the device class for the device."""
        return DEVICE_CLASS_BLIND

    @property
    def current_cover_position(self):
        """Return the current position of the cover."""
        return int(self._device.dim_percent * 100)

    @property
    def is_closed(self):
        """Return if the cover is closed or not."""
        return not self._device.is_on

    async def async_open_cover(self, **kwargs):
        await self._device.on()

    async def async_close_cover(self, **kwargs):
        await self._device.off()

    async def async_set_cover_position(self, **kwargs):
        await self._device.dim(kwargs.get(ATTR_POSITION, 0))

    @property
    def should_poll(self):
        return True
