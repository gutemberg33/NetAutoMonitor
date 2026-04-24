"""Network device orchestration and command execution logic."""

from datetime import datetime, timezone

# Netmiko handles SSH connectivity to multi-vendor network devices.
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

# Reuse project-level logger configuration.
from logger import logger


class DeviceManager:
    """Connect to devices and execute configured command sets."""

    def __init__(self, devices, commands, timeout=5):
        """Store runtime dependencies and execution settings."""
        self.devices = devices
        self.commands = commands
        self.timeout = timeout

    def run(self):
        """Run commands for every device and return structured results."""
        # Final payload keyed by '<host>:<port>'.
        results = {}

        # Process devices independently so one failure does not stop the run.
        for device in self.devices:
            host = device["host"]
            port = device.get("port", 22)
            key = f"{host}:{port}"
            device_type = device["device_type"]
            # Initialize as None to allow safe cleanup in finally block.
            conn = None

            try:
                # Record connection attempt in logs for observability.
                logger.info("Connecting to %s:%s", host, port)
                # Reuse one connection per device for all commands.
                conn = ConnectHandler(**device, timeout=self.timeout)

                # Select the command list using device_type from inventory.
                command_list = self.commands.get(device_type, [])
                # Store command-level output details for this specific device.
                command_results = {}
                # Use one UTC timestamp for this device execution batch.
                device_timestamp = datetime.now(timezone.utc).isoformat()

                # Execute commands sequentially and capture output.
                for command in command_list:
                    output = conn.send_command(command, use_textfsm=True)
                    # TextFSM may return structured rows (list) or raw text (str).
                    if isinstance(output, list):
                        normalized_output = output
                    else:
                        normalized_output = str(output)

                    command_results[command] = {
                        "status": "success",
                        "output": normalized_output,
                        "timestamp": device_timestamp,
                    }
                    logger.debug("%s | %s | command executed", host, command)

                # Mark the full device run as successful.
                results[key] = {"status": "success", "data": command_results}

            except (NetmikoAuthenticationException, NetmikoTimeoutException) as exc:
                # Keep failure reason per device while continuing other devices.
                logger.exception("Netmiko connection failure for device %s", key)
                results[key] = {"status": "failed", "error": str(exc)}

            finally:
                # Always close active SSH sessions to avoid leaked connections.
                if conn is not None:
                    conn.disconnect()

        return results