"""Models the basic API data for a HomeSeer device."""

from .const import (
    REASON_DISCONNECTED,
    REASON_RECONNECTED,
)


class HomeSeerDevice:
    """Do not use this class directly, subclass it."""

    def __init__(self, raw, control_data, request):
        self._raw = raw
        self._control_data = control_data
        self._request = request
        self._value = self._raw["value"]
        self._on_value = None
        self._off_value = None
        self._lock_value = None
        self._unlock_value = None
        self._value_update_callback = None
        self._suppress_value_update_callback = False
        self._get_control_values()

    @property
    def ref(self):
        return self._raw["ref"]

    @property
    def name(self):
        return self._raw["name"]

    @property
    def location(self):
        return self._raw["location"]

    @property
    def location2(self):
        return self._raw["location2"]

    @property
    def value(self):
        """Return int or float device value as appropriate."""
        if "." in str(self._value):
            return float(self._value)
        return int(self._value)

    @property
    def device_type_string(self):
        return self._raw["device_type_string"]

    @property
    def status(self):
        return self._raw["status"]

    def _get_control_values(self):
        for item in self._control_data:
            if item["ref"] == self.ref:
                control_pairs = item["ControlPairs"]
                for pair in control_pairs:
                    control_use = pair["ControlUse"]
                    control_label = pair["Label"]
                    if control_use == 1:
                        self._on_value = pair["ControlValue"]
                    elif control_use == 2:
                        self._off_value = pair["ControlValue"]
                    elif control_use == 18:
                        self._lock_value = pair["ControlValue"]
                    elif control_use == 19:
                        self._unlock_value = pair["ControlValue"]
                    elif control_label == "Lock":
                        self._lock_value = pair["ControlValue"]
                    elif control_label == "Unlock":
                        self._unlock_value = pair["ControlValue"]
                break

    def register_update_callback(self, callback, suppress_on_reconnect=False):
        self._suppress_value_update_callback = suppress_on_reconnect
        self._value_update_callback = callback

    def update_value(self, value, reason=None):
        if value is not None:
            self._value = value

        if reason == REASON_RECONNECTED and self._suppress_value_update_callback:
            return
        elif reason == REASON_DISCONNECTED and self._suppress_value_update_callback:
            return
        elif self._value_update_callback is not None:
            self._value_update_callback()
