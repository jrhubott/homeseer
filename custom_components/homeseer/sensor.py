"""
Support for HomeSeer sensor-type devices.
"""

from pyhs3ng.device import (
    GenericBatterySensor,
    GenericFanSensor,
    GenericHumiditySensor,
    GenericLuminanceSensor,
    GenericMultiLevelSensor,
    GenericOperatingStateSensor,
    GenericPowerSensor,
    GenericSensor,
)
from pyhs3ng import (
    HS_UNIT_CELSIUS,
    HS_UNIT_FAHRENHEIT,
    HS_UNIT_LUX,
    HS_UNIT_PERCENTAGE,
    HS_UNIT_KILOWATTS,
    HS_UNIT_AMPS,
    HS_UNIT_VOLTS,
    HS_UNIT_WATTS,
)

from homeassistant.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    LIGHT_LUX,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    PERCENTAGE,
    POWER_WATT,
    POWER_KILO_WATT,
    ELECTRICAL_CURRENT_AMPERE,
    VOLT,
)

from homeassistant.helpers.entity import Entity
from .hoomseer import HomeseerEntity
from .const import DATA_CLIENT, _LOGGER, DOMAIN

DEPENDENCIES = ["homeseer"]


UNIT_CONVERSION = {
    HS_UNIT_CELSIUS: TEMP_CELSIUS,
    HS_UNIT_FAHRENHEIT: TEMP_FAHRENHEIT,
    HS_UNIT_LUX: LIGHT_LUX,
    HS_UNIT_PERCENTAGE: PERCENTAGE,
    HS_UNIT_KILOWATTS: POWER_KILO_WATT,
    HS_UNIT_AMPS: ELECTRICAL_CURRENT_AMPERE,
    HS_UNIT_VOLTS: VOLT,
    HS_UNIT_WATTS: POWER_WATT,
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HomeSeer sensor-type devices."""
    sensor_devices = []
    homeseer = hass.data[DOMAIN][DATA_CLIENT][config_entry.entry_id]

    for device in homeseer.devices:
        if issubclass(type(device), GenericSensor):
            dev = get_sensor_device(device, homeseer)
            sensor_devices.append(dev)
            _LOGGER.info(f"Added HomeSeer senssor-type device: {dev.name}")

    async_add_entities(sensor_devices)


class HSSensor(HomeseerEntity, Entity):
    """Base representation of a HomeSeer sensor-type device."""

    def __init__(self, device, connection):
        HomeseerEntity.__init__(self, device, connection)

    @property
    def state(self):
        """Return the state of the device."""
        return self._device.value


class HSBattery(HSSensor):
    """Representation of a HomeSeer device that reports battery level."""

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def icon(self):
        if self.state == 100:
            return "mdi:battery"
        elif self.state > 89:
            return "mdi:battery-90"
        elif self.state > 79:
            return "mdi:battery-80"
        elif self.state > 69:
            return "mdi:battery-70"
        elif self.state > 59:
            return "mdi:battery-60"
        elif self.state > 49:
            return "mdi:battery-50"
        elif self.state > 39:
            return "mdi:battery-40"
        elif self.state > 29:
            return "mdi:battery-30"
        elif self.state > 19:
            return "mdi:battery-20"
        elif self.state > 9:
            return "mdi:battery-10"
        return None

    @property
    def device_class(self):
        return DEVICE_CLASS_BATTERY


class HSHumidity(HSSensor):
    """Representation of a HomeSeer humidity sensor device."""

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def device_class(self):
        return DEVICE_CLASS_HUMIDITY


class HSLuminance(HSSensor):
    """Representation of a HomeSeer light level sensor device."""

    @property
    def unit_of_measurement(self):
        return PERCENTAGE

    @property
    def device_class(self):
        return DEVICE_CLASS_ILLUMINANCE


class HSFanState(HSSensor):
    """Representation of a HomeSeer HVAC fan state sensor device."""

    @property
    def icon(self):
        if self.state == 0:
            return "mdi:fan-off"
        return "mdi:fan"

    @property
    def state(self):
        """Return the state of the device."""
        if self._device.value == 0:
            return "Off"
        elif self._device.value == 1:
            return "On"
        elif self._device.value == 2:
            return "On High"
        elif self._device.value == 3:
            return "On Medium"
        elif self._device.value == 4:
            return "On Circulation"
        elif self._device.value == 5:
            return "On Humidity Circulation"
        elif self._device.value == 6:
            return "On Right-Left Circulation"
        elif self._device.value == 7:
            return "On Up-Down Circulation"
        elif self._device.value == 8:
            return "On Quiet Circulation"
        return None


class HSOperatingState(HSSensor):
    """Representation of a HomeSeer HVAC operating state sensor device."""

    @property
    def icon(self):
        if self.state == "Idle":
            return "mdi:fan-off"
        elif self.state == "Heating":
            return "mdi:flame"
        elif self.state == "Cooling":
            return "mdi:snowflake"
        return "mdi:fan"

    @property
    def state(self):
        """Return the state of the device."""
        if self._device.value == 0:
            return "Idle"
        elif self._device.value == 1:
            return "Heating"
        elif self._device.value == 2:
            return "Cooling"
        elif self._device.value == 3:
            return "Fan Only"
        elif self._device.value == 4:
            return "Pending Heat"
        elif self._device.value == 5:
            return "Pending Cool"
        elif self._device.value == 6:
            return "Vent-Economizer"
        return None


class HSSensorMultilevel(HSSensor):
    """Representation of a HomeSeer multi-level sensor."""

    @property
    def device_class(self):
        uom = self._device.UnitOfMeasurement
        if uom == HS_UNIT_LUX:
            return DEVICE_CLASS_ILLUMINANCE
        if uom == HS_UNIT_CELSIUS:
            return DEVICE_CLASS_TEMPERATURE
        if uom == HS_UNIT_FAHRENHEIT:
            return DEVICE_CLASS_TEMPERATURE
        return None

    @property
    def unit_of_measurement(self):
        uom = self._device.UnitOfMeasurement

        if uom != None:
            return UNIT_CONVERSION[uom]

        return None


class HSSensorPower(HSSensorMultilevel):
    @property
    def device_class(self):
        return DEVICE_CLASS_ENERGY


def get_sensor_device(device, homeseer):
    """Return the proper sensor object based on device type."""

    if issubclass(type(device), GenericHumiditySensor):
        return HSHumidity(device, homeseer)
    if issubclass(type(device), GenericBatterySensor):
        return HSBattery(device, homeseer)
    if issubclass(type(device), GenericLuminanceSensor):
        return HSLuminance(device, homeseer)
    if issubclass(type(device), GenericFanSensor):
        return HSFanState(device, homeseer)
    if issubclass(type(device), GenericOperatingStateSensor):
        return HSOperatingState(device, homeseer)
    if issubclass(type(device), GenericPowerSensor):
        return HSSensorPower(device, homeseer)

    # Check last for this one as everything is based on it
    if issubclass(type(device), GenericMultiLevelSensor):
        return HSSensorMultilevel(device, homeseer)

    return HSSensor(device, homeseer)
