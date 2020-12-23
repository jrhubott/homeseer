from .zwave import (
    ZWaveBarrierOperator,
    ZWaveDoorLock,
    ZWaveSwitch,
    ZWaveSwitchMultilevel,
)
from .insteon import InsteonSwitch, InsteonSwitchMultilevel
import logging

_LOGGER = logging.getLogger(__name__)

from .device import (
    GenericBatterySensor,
    GenericBinarySensor,
    GenericEvent,
    GenericFanSensor,
    GenericHumiditySensor,
    GenericLuminanceSensor,
    GenericMultiLevelSensor,
    GenericOperatingStateSensor,
    GenericPowerSensor,
    GenericSensor,
    HomeSeerDevice,
)

# Key / Value
HASS_DICTIONARY = {
    # Insteon switchs
    "Insteon Dual-Band SwitchLinc On/Off": InsteonSwitch,
    "Insteon Outdoor ApplianceLinc": InsteonSwitch,
    "ApplianceLinc": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button B": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button C": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button D": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button E": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button F": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button G": InsteonSwitch,
    "Insteon KeypadLinc V2 Dimmer Button H": InsteonSwitch,
    "Insteon I/O Linc Output Relay": InsteonSwitch,
    # Insteon multilevel switch
    "Insteon Dual-Band SwitchLinc Dimmer": InsteonSwitchMultilevel,
    "Insteon KeypadLinc V2 Dimmer Button A/Load": InsteonSwitchMultilevel,
    # Insteon sensors
    "Insteon I/O Linc Input Sensor": GenericBinarySensor,
    # ZWave switch
    "Z-Wave Switch": ZWaveSwitch,
    "Z-Wave Switch Binary": ZWaveSwitch,
    # ZWave multilevel switch
    "Z-Wave Switch Multilevel": ZWaveSwitchMultilevel,
    # ZWave sensors
    "Z-Wave Sensor Binary": GenericBinarySensor,
    "Z-Wave Sensor Multilevel": GenericMultiLevelSensor,
    "Z-Wave Temperature": GenericMultiLevelSensor,
    "Z-Wave Battery": GenericBatterySensor,
    "Z-Wave Fan State": GenericFanSensor,
    "Z-Wave Relative Humidity": GenericHumiditySensor,
    "Z-Wave Operating State": GenericOperatingStateSensor,
    "Z-Wave Luminance": GenericLuminanceSensor,
    "Z-Wave Watts": GenericPowerSensor,
    # ZWave Locks
    "Z-Wave Door Lock": ZWaveDoorLock,
    # ZWave Cover
    "Z-Wave Barrier Operator": ZWaveBarrierOperator,
    # ZWave Events
    "Z-Wave Central Scene": GenericEvent,
}


def get_device(raw, control_data, request):
    device_type = raw["device_type_string"]

    # lookup
    try:
        type = HASS_DICTIONARY[device_type]
        return type(raw, control_data, request)
    except KeyError:
        return None

    return None