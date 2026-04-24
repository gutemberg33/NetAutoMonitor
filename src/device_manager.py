from datetime import datetime, timezone

from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

from logger import logger


class DeviceManager:
    """Connect to devices and execute configured command sets."""

    def __init__(self, devices, commands, timeout=5):
        self.devices = devices
        self.commands = commands
        self.timeout = timeout

    def run(self):
        """Return per-device execution results keyed by host:port."""
        results = {}

        for device in self.devices:
            host = device["host"]
            port = device.get("port", 22)
            key = f"{host}:{port}"
            device_type = device["device_type"]
            conn = None

            try:
                logger.info("Connecting to %s:%s", host, port)
                # Reuse one connection per device for all commands.
                conn = ConnectHandler(**device, timeout=self.timeout)

                # Select the command list using device_type from inventory.
                command_list = self.commands.get(device_type, [])
                command_results = {}
                # Use one UTC timestamp for this device execution batch.
                device_timestamp = datetime.now(timezone.utc).isoformat()

                for command in command_list:
                    output = conn.send_command(command)
                    command_results[command] = {
                        "status": "success",
                        "output": output,
                        "timestamp": device_timestamp,
                    }
                    logger.debug("%s | %s | command executed", host, command)

                results[key] = {"status": "success", "data": command_results}

            except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
                logger.exception("Netmiko connection failure for device %s", key)
                results[key] = {"status": "failed", "error": str(exc)}

            finally:
                if conn is not None:
                    conn.disconnect()

        return results