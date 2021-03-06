"""
Support for HomeSeer switch-type devices.
"""

from pyhs3ng.device import GenericDevice, GenericSwitch, GenericSwitchMultilevel
from .hoomseer import HomeseerEntity

from homeassistant.components.switch import SwitchEntity

from .const import DATA_CLIENT, _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer switch-type devices."""
    switch_devices = []
    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if (
            issubclass(type(device), GenericSwitch)
            and issubclass(type(device), GenericSwitchMultilevel) == False
        ):
            dev = HSSwitch(device, homeseer)
            switch_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer switch-type device: {dev.name}")

        if (
            issubclass(type(device), GenericDevice)
            and device.device_type_string == "Virtual Switch"
        ):
            dev = HSSwitch(device, homeseer)
            switch_devices.append(dev)
            _LOGGER.info(
                f"Added HomeSeer virtual switch as switch-type device: {dev.name}"
            )

    async_add_entities(switch_devices)


class HSSwitch(HomeseerEntity, SwitchEntity):
    """Representation of a HomeSeer switch-type device."""

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        await self._device.on()

    async def async_turn_off(self, **kwargs):
        await self._device.off()
