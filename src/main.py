from device_manager import DeviceManager
from utils import load_yaml
from output_manager import OutputManager

# Load runtime settings (timeouts, command map) and device inventory.
config = load_yaml("config/config.yaml")
devices = load_yaml("config/devices.yaml")

# Build the orchestrator with device list, per-platform commands, and fallback timeout.
manager = DeviceManager(
    devices=devices["devices"],
    commands=config["commands"],
    timeout=config.get("timeout", 5)
)

# Execute all commands across all configured devices.
results = manager.run()

# Persist collected command outputs for later analysis.
OutputManager().save_json(results)