import logging
from typing import Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_NAME,
    CONF_EVENT,
    CONF_HOST,
    CONF_ID,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_PORT,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.util import slugify
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN,
    CONF_NAMESPACE,
    DEFAULT_PASSWORD,
    DEFAULT_USERNAME,
    DEFAULT_ASCII_PORT,
    DEFAULT_HTTP_PORT,
    CONF_ASCII_PORT,
    CONF_HTTP_PORT,
    CONF_NAME_TEMPLATE,
    DEFAULT_NAME_TEMPLATE,
    CONF_ALLOW_EVENTS,
    DEFAULT_ALLOW_EVENTS,
)

_LOGGER = logging.getLogger(__name__)

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default="Homeseer"): cv.string,
        vol.Required(CONF_HOST, default="salix.home.rhusoft.com"): cv.string,
        vol.Optional(CONF_NAMESPACE, default="homeseer"): cv.string,
        vol.Optional(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
        vol.Optional(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
        vol.Optional(CONF_HTTP_PORT, default=DEFAULT_HTTP_PORT): cv.port,
        vol.Optional(CONF_ASCII_PORT, default=DEFAULT_ASCII_PORT): cv.port,
        vol.Optional(CONF_NAME_TEMPLATE, default=DEFAULT_NAME_TEMPLATE): cv.string,
        vol.Optional(CONF_ALLOW_EVENTS, default=DEFAULT_ALLOW_EVENTS): cv.boolean,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for OpenSprinkler."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:

            name = user_input[CONF_NAME]
            host = user_input[CONF_HOST]
            password = user_input[CONF_PASSWORD]
            username = user_input[CONF_USERNAME]

            return self.async_create_entry(
                title=name,
                data={
                    CONF_HOST: host,
                    CONF_NAMESPACE: user_input[CONF_NAMESPACE],
                    CONF_USERNAME: username,
                    CONF_PASSWORD: password,
                    CONF_HTTP_PORT: user_input[CONF_HTTP_PORT],
                    CONF_ASCII_PORT: user_input[CONF_ASCII_PORT],
                    CONF_NAME_TEMPLATE: user_input[CONF_NAME_TEMPLATE],
                    CONF_ALLOW_EVENTS: user_input[CONF_ALLOW_EVENTS],
                },
            )

        return self.async_show_form(
            step_id="user", data_schema=DEVICE_SCHEMA, errors=errors
        )

    async def async_step_import(self, user_input):
        """Handle import."""
        return await self.async_step_user(user_input)
