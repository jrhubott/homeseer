"""Constants used in pyhs3."""

import logging

_LOGGER = logging.getLogger(__name__)

DEFAULT_ASCII_PORT = 11000
DEFAULT_HTTP_PORT = 80
DEFAULT_PASSWORD = "default"
DEFAULT_USERNAME = "default"

REASON_DISCONNECTED = "disconnected"
REASON_RECONNECTED = "reconnected"

STATE_CLOSED = "closed"
STATE_CLOSING = "closing"
STATE_CONNECTING = "connecting"
STATE_DISCONNECTED = "disconnected"
STATE_IDLE = "idle"
STATE_LISTENING = "listening"
STATE_OPEN = "open"
STATE_OPENING = "opening"
STATE_STOPPED = "stopped"

HS_UNIT_CELSIUS = "C"
HS_UNIT_FAHRENHEIT = "F"
HS_UNIT_LUX = "Lux"
HS_UNIT_PERCENTAGE = "%"
