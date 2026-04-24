import json
from pathlib import Path

class OutputManager:
    """Handles writing collected automation results to disk."""

    def save_json(self, data, filename="output.json"):
        """Save result data under the local output directory."""
        path = Path("output") / filename

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Saved to {path}")