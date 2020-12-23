"""Helpers for Home Assistant."""
from .const import (
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
