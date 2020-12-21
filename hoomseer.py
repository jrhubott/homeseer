from .pyhs3ng import STATE_LISTENING


class HomeseerEntity:
    @property
    def available(self):
        """Return whether the device is available."""
        return self._connection.api.state == STATE_LISTENING

    @property
    def device_state_attributes(self):
        attr = {
            "Device Ref": self._device.ref,
            "Location": self._device.location,
            "Location 2": self._device.location2,
            "Device Type": self._device.device_type_string,
        }
        return attr

    @property
    def unique_id(self):
        """Return a unique ID for the device."""
        return f"{self._connection.namespace}-{self._device.ref}"

    @property
    def name(self):
        """Return the name of the device."""
        return self._connection.name_template.async_render(device=self._device).strip()

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def state(self):
        """Return the state of the device."""
        return self._device.value

    async def async_added_to_hass(self):
        """Register value update callback."""
        self._device.register_update_callback(self.async_schedule_update_ha_state)