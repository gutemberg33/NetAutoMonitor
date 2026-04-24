import logging

# Configure file-based logging shared across the application.
logging.basicConfig(
    filename="logs/netautomonitor.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger()