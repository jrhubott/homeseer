from pyhs3ng.device import HomeSeerDevice
from .const import DEFAULT_NAMESPACE
from pyhs3ng import STATE_LISTENING
from homeassistant.helpers.entity import Entity


class HomeseerEntity:
    def __init__(self, device: HomeSeerDevice, connection):
        self._device = device
        self._connection = connection
        self._entity_id = None
        self._parent = None

    @property
    def entity_id(self):

        if self._entity_id == None:
            if self._connection.namespace == DEFAULT_NAMESPACE:
                self._entity_id = f"{self.platform.domain}.{self._device.location2}_{self._device.location}_{self._device.name}_{self._device.ref}"
            else:
                self._entity_id = f"{self.platform.domain}.{self._device.location2}_{self._device.location}_{self._device.name}_{self._connection.namespace}_{self._device.ref}"

        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value

    @property
    def available(self):
        """Return whether the device is available."""
        return self._connection.api.state == STATE_LISTENING

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self.parent = value

    @property
    def device_state_attributes(self):
        attr = {
            "HS Ref": self._device.ref,
            "HS Name": self._device.name,
            "HS Location": f"{self._device.location} / {self._device.location2}",
            "HS Type": self._device.device_type_string,
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

    async def async_added_to_hass(self):
        if not self._device == None:
            """Register value update callback."""
            self._device.register_update_callback(self.async_schedule_update_ha_state)

    @property
    def device_info(self):
        root = self._device.root

        return {
            "identifiers": {(self._connection.namespace, root.ref)},
            "name": root.name,
            "manufacturer": root.interface_name,
            "model": root.device_type_string,
        }
