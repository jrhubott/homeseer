"""
Custom component for interacting with a HomeSeer HomeTroller or HS3 software installation.

For more details about this custom component, please refer to the documentation at
https://github.com/marthoc/homeseer
"""
import asyncio
from homeassistant.config_entries import ConfigEntry

import voluptuous as vol
from .pyhs3ng import HomeTroller, STATE_LISTENING
from .pyhs3ng.device import GenericEvent

import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_EVENT,
    CONF_HOST,
    CONF_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
)
from homeassistant.core import EventOrigin, HomeAssistant
from homeassistant.helpers import aiohttp_client, discovery

from .const import (
    _LOGGER,
    CONF_ALLOW_EVENTS,
    CONF_ASCII_PORT,
    CONF_HTTP_PORT,
    CONF_NAME_TEMPLATE,
    CONF_NAMESPACE,
    DEFAULT_ALLOW_EVENTS,
    DEFAULT_ASCII_PORT,
    DEFAULT_HTTP_PORT,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    DEFAULT_NAME_TEMPLATE,
    DOMAIN,
    HOMESEER_PLATFORMS,
)


REQUIREMENTS = []


async def async_setup(hass, config):

    return True


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    """Set up the HomeSeer component."""
    #  config = config.get(DOMAIN)
    host = config.data.get(CONF_HOST)
    namespace = config.data.get(CONF_NAMESPACE)
    username = config.data.get(CONF_USERNAME)
    password = config.data.get(CONF_PASSWORD)
    http_port = config.data.get(CONF_HTTP_PORT)
    ascii_port = config.data.get(CONF_ASCII_PORT)
    name_template = config.data.get(CONF_NAME_TEMPLATE)
    allow_events = config.data.get(CONF_ALLOW_EVENTS)

    name_template.hass = hass

    homeseer = HSConnection(
        hass, host, username, password, http_port, ascii_port, namespace, name_template
    )

    await homeseer.api.initialize()
    if len(homeseer.devices) == 0 and len(homeseer.events) == 0:
        _LOGGER.error("No supported HomeSeer devices found, aborting component setup.")
        return False

    await homeseer.start()
    i = 0
    while homeseer.api.state != STATE_LISTENING:
        if i < 3:
            i += 1
            await asyncio.sleep(1)
        elif i == 3:
            _LOGGER.error(
                "Failed to connect to HomeSeer ASCII server, aborting component setup."
            )
            await homeseer.stop()
            return False
    _LOGGER.info(f"Connected to HomeSeer ASCII server at {host}:{ascii_port}")

    homeseer.add_remotes()

    if not allow_events:
        HOMESEER_PLATFORMS.remove("scene")

    for platform in HOMESEER_PLATFORMS:
        hass.async_create_task(
            discovery.async_load_platform(hass, platform, DOMAIN, {}, config)
        )

    hass.data[DOMAIN] = homeseer

    hass.bus.async_listen_once("homeassistant_stop", homeseer.stop)

    return True


class HSConnection:
    """Manages a connection between HomeSeer and Home Assistant."""

    def __init__(
        self,
        hass,
        host,
        username,
        password,
        http_port,
        ascii_port,
        namespace,
        name_template,
    ):
        self._hass = hass
        self._session = aiohttp_client.async_get_clientsession(self._hass)
        self.api = HomeTroller(
            host,
            self._session,
            username=username,
            password=password,
            http_port=http_port,
            ascii_port=ascii_port,
        )
        self._namespace = namespace
        self._name_template = name_template
        self.remotes = []

    @property
    def devices(self):
        return self.api.devices.values()

    @property
    def events(self):
        return self.api.events

    @property
    def namespace(self):
        return self._namespace

    @property
    def name_template(self):
        return self._name_template

    async def start(self):
        await self.api.start_listener()

    async def stop(self, *args):
        await self.api.stop_listener()

    def add_remotes(self):
        for device in self.devices:
            if issubclass(type(device), GenericEvent):
                self.remotes.append(HSRemote(self._hass, device))
                _LOGGER.info(
                    f"Added HomeSeer remote-type device: {device.name} (Ref: {device.ref})"
                )


class HSRemote:
    """Link remote-type devices that should fire events rather than create entities to Home Assistant."""

    def __init__(self, hass, device):
        self._hass = hass
        self._device = device
        self._device.register_update_callback(
            self.update_callback, suppress_on_reconnect=True
        )
        self._event = f"homeseer_{CONF_EVENT}"

    def update_callback(self):
        """Fire the event."""
        data = {CONF_ID: self._device.ref, CONF_EVENT: self._device.value}
        self._hass.bus.async_fire(self._event, data, EventOrigin.remote)
