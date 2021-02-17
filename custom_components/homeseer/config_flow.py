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
    DEFAULT_HOST,
    DEFAULT_NAME,
    DEFAULT_NAMESPACE,
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
    CONF_FORCED_BLINDS,
)

_LOGGER = logging.getLogger(__name__)

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Required(CONF_HOST, default=DEFAULT_HOST): cv.string,
        vol.Required(CONF_NAMESPACE, default=DEFAULT_NAMESPACE): cv.string,
        vol.Required(CONF_USERNAME, default=DEFAULT_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD, default=DEFAULT_PASSWORD): cv.string,
        vol.Required(CONF_HTTP_PORT, default=DEFAULT_HTTP_PORT): cv.port,
        vol.Required(CONF_ASCII_PORT, default=DEFAULT_ASCII_PORT): cv.port,
        vol.Required(CONF_NAME_TEMPLATE, default=DEFAULT_NAME_TEMPLATE): cv.string,
        vol.Required(CONF_ALLOW_EVENTS, default=DEFAULT_ALLOW_EVENTS): cv.boolean,
        vol.Required(CONF_FORCED_BLINDS, default="0"): cv.string,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:

            await self.async_set_unique_id(user_input[CONF_NAMESPACE])
            self._abort_if_unique_id_configured()

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
                    vol.Required(
                        CONF_NAME_TEMPLATE,
                        default=self.config_entry.options.get(CONF_NAME_TEMPLATE),
                    ): str,
                    vol.Required(
                        CONF_ALLOW_EVENTS,
                        default=self.config_entry.options.get(CONF_ALLOW_EVENTS),
                    ): cv.boolean,
                    vol.Required(
                        CONF_FORCED_BLINDS,
                        default=self.config_entry.options.get(CONF_FORCED_BLINDS),
                    ): str,
                }
            ),
        )
