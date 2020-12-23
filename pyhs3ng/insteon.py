"""Models Z-Wave devices."""

from .const import (
    _LOGGER,
)
from .device import GenericSwitch, GenericSwitchMultilevel, HomeSeerDevice


class InsteonSwitch(GenericSwitch):
    pass


class InsteonSwitchMultilevel(GenericSwitchMultilevel):
    pass


class InsteonSensorBinary(HomeSeerDevice):
    pass
