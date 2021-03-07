import inspect
import logging

from jals.logger import logger

logger = logging.getLogger(__name__)


class Base:
    """
    every class (node, rule) should have an evaluate function and name field.
    """

    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return
