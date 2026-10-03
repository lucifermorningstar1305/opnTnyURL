# LICENSE HEADER MANAGED BY add-license-header
#
# Copyright (c) 2026 Adityam Ghosh
# SPDX-License-Identifier: MIT
#

import logging
from typing import Literal

from rich.logging import RichHandler

LOG_LEVELS = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "error": logging.ERROR,
    "warning": logging.WARNING,
}


class RichLogger:
    def __init__(
        self, name: str, log_lvl: Literal["info", "debug", "warning", "error"] = "info"
    ):
        self._logger = logging.getLogger(name)

        self._logger.setLevel(LOG_LEVELS[log_lvl])

        if not self._logger.handlers:
            console_handler = RichHandler(rich_tracebacks=True)
            console_handler.setLevel(LOG_LEVELS[log_lvl])

            self._logger.addHandler(console_handler)

    def info(self, msg: str, markup: bool = False):
        self._logger.info(msg, extra={"markup": markup})

    def debug(self, msg: str, markup: bool = False):
        self._logger.debug(msg, extra={"markup": markup})

    def warning(self, msg: str, markup: bool = False):
        self._logger.warning(msg, extra={"markup": markup})

    def error(self, msg: str, markup: bool = False):
        self._logger.error(msg, extra={"markup": markup})

    def exception(self, msg: str, markup: bool = False):
        self._logger.exception(msg, extra={"markup": markup})
