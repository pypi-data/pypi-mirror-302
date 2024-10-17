""" Constants for the application."""
from .utilities import invert


# Status Constants
STATUS_OK = 1
STATUS = {
    'indeterminate': -1,
    'ok': 0,
    'error': 1,
}
STATUS = invert(STATUS)
