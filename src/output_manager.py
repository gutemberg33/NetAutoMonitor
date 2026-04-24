"""Output serialization utilities."""

import json
from pathlib import Path


class OutputManager:
    """Handle writing collected automation results to disk."""

    def save_json(self, data, filename="output.json"):
        """Serialize result data to JSON under the local output directory."""
        # Keep output artifacts in a dedicated folder.
        path = Path("output") / filename

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        # Provide a simple operator-visible confirmation.
        print(f"Saved to {path}")