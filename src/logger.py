"""Centralized logging configuration for the application."""

import logging

# Configure application-wide file logging.
logging.basicConfig(
    filename="logs/netautomonitor.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Expose a shared logger instance for all modules.
logger = logging.getLogger()