"""
Constants for the HomeSeer component.
"""

import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "homeseer"

ATTR_REF = "ref"
ATTR_VALUE = "value"

CONF_HTTP_PORT = "http_port"
CONF_ASCII_PORT = "ascii_port"
CONF_ALLOW_EVENTS = "allow_events"
CONF_NAMESPACE = "namespace"
CONF_NAME_TEMPLATE = "name_template"

DATA_CLIENT = "homeseer_client"

DEFAULT_HTTP_PORT = 80
DEFAULT_PASSWORD = "xleter"
DEFAULT_USERNAME = "admin"
DEFAULT_ASCII_PORT = 11000
DEFAULT_NAME_TEMPLATE = "{{ device.location }} {{ device.name }}"
DEFAULT_ALLOW_EVENTS = True
DEFAULT_NAMESPACE = "homeseer"
DEFAULT_NAME = "Homeseer"
DEFAULT_HOST = "salix.home.rhusoft.com"
HOMESEER_PLATFORMS = [
    "binary_sensor",
    "cover",
    "light",
    "lock",
    "scene",
    "sensor",
    "switch",
]
