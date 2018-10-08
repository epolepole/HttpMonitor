import json
import logging

from displayers.abstract_displayer import AbstractDisplayer

logger = logging.getLogger(__name__)


class LogAbstractDisplayer(AbstractDisplayer):
    def display(self, data):
        logger.info(json.dumps(data))
