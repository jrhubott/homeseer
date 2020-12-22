"""Models Z-Wave devices."""

from .const import INSTEON_BINARY_SENSORS, _LOGGER, INSTEON_SWITCHES, INSTEON_LIGHTS
from .device import HomeSeerDevice


class InsteonSwitch(HomeSeerDevice):
    @property
    def is_on(self):
        return self.value > self._off_value

    async def on(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._on_value,
        }

        await self._request("get", params=params)

    async def off(self):
        params = {
            "request": "controldevicebyvalue",
            "ref": self.ref,
            "value": self._off_value,
        }

        await self._request("get", params=params)


class ZWaveSwitchMultilevel(InsteonSwitch):
    @property
    def dim_percent(self):
        return self.value / self._on_value

    async def dim(self, percent: int):
        value = int(self._on_value * (percent / 100))

        params = {"request": "controldevicebyvalue", "ref": self.ref, "value": value}

        await self._request("get", params=params)


class ZWaveSensorBinary(HomeSeerDevice):

    pass


def get_insteon_device(raw, control_data, request):
    device_type = raw["device_type_string"]
    if device_type in INSTEON_SWITCHES:
        return InsteonSwitch(raw, control_data, request)
    if device_type in INSTEON_LIGHTS:
        return ZWaveSwitchMultilevel(raw, control_data, request)
    if device_type in INSTEON_BINARY_SENSORS:
        return ZWaveSwitchMultilevel(raw, control_data, request)

    return None
