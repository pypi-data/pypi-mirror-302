import json
from pathlib import Path


def load_data(path_to_data: Path) -> dict[str, str]:
    with path_to_data.open() as f:
        return json.loads(f.read())
