"""Application entrypoint for running network command collection."""

# Import the orchestration, config loading, and persistence components.
from device_manager import DeviceManager
from utils import load_yaml
from output_manager import OutputManager

# Load runtime settings (command mapping, timeout) from YAML files.
config = load_yaml("config/config.yaml")
# Load target device inventory from YAML files.
devices = load_yaml("config/devices.yaml")

# Create the manager with inventory, per-platform command map, and timeout.
manager = DeviceManager(
    devices=devices["devices"],
    commands=config["commands"],
    timeout=config.get("timeout", 5)
)

# Run command collection against all configured devices.
results = manager.run()

# Save collected data as JSON for auditing and later analysis.
OutputManager().save_json(results)