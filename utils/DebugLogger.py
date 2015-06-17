__author__ = 'Hannah'

import logging


_LOGGER = logging.getLogger(__name__)


def log(message):
    _LOGGER.debug("Debug Logger:" + str(message))