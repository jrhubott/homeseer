"""
Models a connection to a HomeSeer HomeTroller (or independent HomeSeer HS3 software installation).
Allows sending commands via JSON API and listening for device changes via ASCII interface.
"""

from asyncio import TimeoutError
from .factory import get_device
from .device import HomeSeerDevice
from aiohttp import BasicAuth, ContentTypeError
from typing import Union

import logging

_LOGGER = logging.getLogger(__name__)

from .const import (
    DEFAULT_ASCII_PORT,
    DEFAULT_HTTP_PORT,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    REASON_DISCONNECTED,
    STATE_IDLE,
    STATE_STOPPED,
)
from .events import HomeSeerEvent
from .listener import ASCIIListener


class HomeTroller:
    def __init__(
        self,
        host,
        websession,
        username=DEFAULT_USERNAME,
        password=DEFAULT_PASSWORD,
        http_port=DEFAULT_HTTP_PORT,
        ascii_port=DEFAULT_ASCII_PORT,
    ):
        self._host = host
        self._websession = websession
        self._auth = BasicAuth(username, password)
        self._http_port = http_port
        self._ascii_port = ascii_port
        self._listener = ASCIIListener(
            self._host,
            username=username,
            password=password,
            ascii_port=self._ascii_port,
            async_message_callback=self._update_device_value,
            async_connection_callback=self.refresh_devices,
            async_disconnection_callback=self._disconnect_callback,
        )
        self.devices = {}
        self.all_devices = {}
        self.events = []

    @property
    def state(self):
        return self._listener.state

    async def initialize(self):
        await self._get_devices()
        await self._get_events()

    async def start_listener(self):
        self._listener.state = STATE_IDLE
        await self._listener.connection_handler()

    async def stop_listener(self):
        self._listener.state = STATE_STOPPED
        await self._listener.connection_handler()

    async def control_device_by_value(self, ref: int, value: Union[str, int, float]):
        """
        Provides an interface for controlling devices by value
        directly through the HomeTroller object.
        """
        params = {
            "request": "controldevicebyvalue",
            "ref": ref,
            "value": value,
        }
        await self._request("get", params=params)

    async def _request(self, method, params=None, json=None):
        """Make an API request"""
        url = f"http://{self._host}:{self._http_port}/JSON"

        try:
            async with self._websession.request(
                method,
                url,
                params=params,
                json=json,
                auth=self._auth,
            ) as result:
                result.raise_for_status()
                _LOGGER.debug(f"HomeSeer request response: {await result.text()}")
                return await result.json()

        except ContentTypeError:
            _LOGGER.debug(f"HomeSeer returned non-JSON response: {await result.text()}")

        except TimeoutError:
            _LOGGER.error(
                f"Timeout while requesting HomeSeer data from {self._host}:{self._http_port}"
            )

        except Exception as err:
            _LOGGER.error(f"HomeSeer HTTP Request error: {err}")

    async def _get_devices(self):
        try:
            params = {"request": "getstatus"}
            result = await self._request("get", params=params)

            all_devices = result["Devices"]

            params = {"request": "getcontrol"}
            result = await self._request("get", params=params)

            control_data = result["Devices"]

            for device in all_devices:
                dev = get_device(device, control_data, self._request)

                if dev is not None:
                    self.devices[dev.ref] = dev
                else:
                    # Create a dummy device
                    dev = HomeSeerDevice(device, control_data, self._request)
                    _LOGGER.debug(
                        f"HomeSeer device type not supported: {dev.device_type_string}"
                    )
                # add to the all device list
                self.all_devices[dev.ref] = dev
        except TypeError:
            _LOGGER.error("Error retrieving HomeSeer devices!")

    async def _get_events(self):
        try:
            params = {"request": "getevents"}
            result = await self._request("get", params=params)

            all_events = result["Events"]

            for event in all_events:
                ev = HomeSeerEvent(event, self._request)
                self.events.append(ev)

        except TypeError:
            _LOGGER.error("Error retrieving HomeSeer events!")

    async def _update_device_value(self, device_ref, value):
        try:
            device = self.devices[int(device_ref)]
            prev_value = device.value
            device.update_value(value)
            _LOGGER.info(
                f"{device.device_type_string} '{device.name}' ({device.ref}) updated from: {prev_value} to: {device.value}"
            )

        except KeyError:
            try:
                device = self.all_devices[int(device_ref)]
                device.update_value(value)
                _LOGGER.debug(
                    f"Unsupported {device.device_type_string} '{device.name}' ({device.ref}) updated to: {device.value}"
                )

            except KeyError:
                _LOGGER.error(
                    f"HomeSeer update received for unknown device: {device_ref}"
                )

    async def _disconnect_callback(self):
        for device in self.devices.values():
            device.update_value(None, REASON_DISCONNECTED)

    async def refresh_devices(self, reason=None):
        try:
            params = {"request": "getstatus"}
            result = await self._request("get", params=params)

            all_devices = result["Devices"]

        except TypeError:
            _LOGGER.error("Error retrieving HomeSeer data for refresh!")
            return

        for device in all_devices:
            try:
                dev = self.devices[device["ref"]]
                dev.update_value(device["value"], reason)
                _LOGGER.debug(
                    f"HomeSeer device '{dev.name}' ({dev.ref}) refreshed to: {dev.value}"
                )
            except KeyError:
                _LOGGER.debug(
                    f"HomeSeer refresh data retrieved for unsupported device type: "
                    f"{device['device_type_string']} ({device['ref']})"
                )
