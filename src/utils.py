"""Shared utility helpers."""

import yaml


def load_yaml(path):
    """Load and parse a YAML file into a Python object."""
    # safe_load prevents arbitrary code execution from untrusted YAML.
    with open(path) as f:
        return yaml.safe_load(f)