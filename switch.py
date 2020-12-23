"""
Support for HomeSeer switch-type devices.
"""

from .pyhs3ng.device import GenericSwitch, GenericSwitchMultilevel
from .hoomseer import HomeseerEntity

from homeassistant.components.switch import SwitchEntity

from .const import _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up HomeSeer switch-type devices."""
    switch_devices = []
    homeseer = hass.data[DOMAIN]

    for device in homeseer.devices:
        if (
            issubclass(type(device), GenericSwitch)
            and issubclass(type(device), GenericSwitchMultilevel) == False
        ):
            dev = HSSwitch(device, homeseer)
            switch_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer switch-type device: {dev.name}")

    async_add_entities(switch_devices)


class HSSwitch(HomeseerEntity, SwitchEntity):
    """Representation of a HomeSeer switch-type device."""

    def __init__(self, device, connection):
        self._device = device
        self._connection = connection

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        await self._device.on()

    async def async_turn_off(self, **kwargs):
        await self._device.off()
