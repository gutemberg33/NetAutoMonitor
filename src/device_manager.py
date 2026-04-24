from netmiko import ConnectHandler

class DeviceManager:
    """Connects to devices and runs configured command sets."""

    def __init__(self, devices, commands, timeout=5):
        self.devices = devices
        self.commands = commands
        self.timeout = timeout

    def run(self):
        """Return command outputs keyed by host and command."""
        results = {}

        for device in self.devices:
            host = device["host"]
            device_type = device["device_type"]

            print(f"\n=== {host} ===")

            # Open one SSH session per device and reuse it for all commands.
            conn = ConnectHandler(**device, timeout=self.timeout)

            # Select the command list based on platform/device type.
            cmd_list = self.commands.get(device_type, [])

            device_output = {}

            for cmd in cmd_list:
                output = conn.send_command(cmd)
                device_output[cmd] = output
                print(output)

            conn.disconnect()
            results[host] = device_output

        return results