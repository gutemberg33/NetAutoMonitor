from pathlib import Path
import yaml

def load_yaml(path):
    """Load and parse a YAML file into a Python object."""
    with open(path) as f:
        return yaml.safe_load(f)