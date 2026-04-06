import json
from pathlib import Path


def load_json(path):
    """Load JSON from disk."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path, indent: int = 2) -> None:
    """Save JSON to disk."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent)


def pretty_json(data) -> str:
    """Return a pretty-printed JSON string."""
    return json.dumps(data, indent=2, ensure_ascii=False)
