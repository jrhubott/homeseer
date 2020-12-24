from homeassistant.core import callback
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
from homeassistant import config_entries, core

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
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:

            name = user_input[CONF_NAME]

            return self.async_create_entry(
                title=name,
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=DEVICE_SCHEMA, errors=errors
        )

    async def async_step_import(self, user_input):
        """Handle import."""
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        """Initialize Hue options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}

        """Manage the options."""
        if user_input is not None:

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_NAME_TEMPLATE,
                        default=self.config_entry.options.get(CONF_NAME_TEMPLATE),
                    ): str,
                }
            ),
        )
