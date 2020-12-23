"""Models Z-Wave devices."""

import logging

_LOGGER = logging.getLogger(__name__)

from .const import (
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_OPEN,
    STATE_OPENING,
)
from .device import (
    GenericCover,
    GenericDoorLock,
    GenericSwitch,
    GenericSwitchMultilevel,
    HomeSeerDevice,
)


class ZWaveBarrierOperator(GenericCover):
    @property
    def current_state(self):
        if self.value == 0:
            return STATE_CLOSED
        elif self.value == 252:
            return STATE_CLOSING
        elif self.value == 254:
            return STATE_OPENING
        else:
            return STATE_OPEN

    async def open(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def close(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class ZWaveDoorLock(GenericDoorLock):
    @property
    def is_locked(self):
        return self.value == self._lock_value

    async def lock(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._lock_value,
        }

        await self._request("get", params=params)

    async def unlock(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._unlock_value,
        }

        await self._request("get", params=params)


class ZWaveSwitch(GenericSwitch):
    pass


class ZWaveSwitchMultilevel(GenericSwitchMultilevel):
    pass