"""
Support for HomeSeer lock-type devices.
"""

from .hoomseer import HomeseerEntity
from .pyhs3ng.device import GenericDoorLock


from homeassistant.components.lock import LockEntity

from .const import DATA_CLIENT, _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer lock-type devices."""
    lock_devices = []
    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if issubclass(type(device), GenericDoorLock):
            dev = HSLock(device, homeseer)
            lock_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer lock-type device: {dev.name}")

    async_add_entities(lock_devices)


class HSLock(HomeseerEntity, LockEntity):
    """Representation of a HomeSeer lock device."""

    def __init__(self, device, connection):
        self._device = device
        self._connection = connection

    @property
    def is_locked(self):
        """Return true if device is locked."""
        return self._device.is_locked

    async def async_lock(self, **kwargs):
        await self._device.lock()

    async def async_unlock(self, **kwargs):
        await self._device.unlock()
