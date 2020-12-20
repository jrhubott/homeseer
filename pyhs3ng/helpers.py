"""Helpers for Home Assistant."""
from .const import (
    DEVICE_ZWAVE_BARRIER_OPERATOR,
    DEVICE_ZWAVE_BATTERY,
    DEVICE_ZWAVE_CENTRAL_SCENE,
    DEVICE_ZWAVE_DOOR_LOCK,
    DEVICE_ZWAVE_FAN_STATE,
    DEVICE_ZWAVE_LUMINANCE,
    DEVICE_ZWAVE_OPERATING_STATE,
    DEVICE_ZWAVE_RELATIVE_HUMIDITY,
    DEVICE_ZWAVE_SENSOR_BINARY,
    DEVICE_ZWAVE_SENSOR_MULTILEVEL,
    DEVICE_ZWAVE_SWITCH,
    DEVICE_ZWAVE_SWITCH_BINARY,
    DEVICE_ZWAVE_SWITCH_MULTILEVEL,
    DEVICE_ZWAVE_TEMPERATURE,
    DEVICE_INSTEON_SWITCH,
    DEVICE_INSTEON_SWITCH2,
    HS_UNIT_CELSIUS,
    HS_UNIT_FAHRENHEIT,
    HS_UNIT_LUX,
    HS_UNIT_PERCENTAGE,
)
from .device import HomeSeerDevice


async def parse_uom(device: HomeSeerDevice):
    """
    Parses the status property of a device object to return a unit of measure,
    or none if no unit can be parsed.
    """
    if "Lux" in device.status:
        return HS_UNIT_LUX
    if "%" in device.status:
        return HS_UNIT_PERCENTAGE
    if "F" in device.status:
        return HS_UNIT_FAHRENHEIT
    if "C" in device.status:
        return HS_UNIT_CELSIUS
    return None
