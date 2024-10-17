import configparser
import os
from logging import getLogger
from pathlib import Path

_logger = getLogger(__name__)


def parse_config(file: Path) -> dict:
    """
    Function to parse base config file
    :param Path file: Path to main config file
    :return: RawConfigParser
    """
    if not os.path.exists(file):
        raise ValueError(f"Config {file} not found")
    _logger.debug("Parsing %s", file)
    config = configparser.RawConfigParser()
    with open(file=file) as f:
        config.readfp(f)
    results = dict(config.__dict__["_sections"])
    return results
