import json
from pathlib import Path


def load_documents(path: str = "src/data/documents.json") -> list[dict]:
    """Carica e restituisce una lista di documenti JSON."""
    full_path = Path(path)
    if not full_path.exists():
        raise FileNotFoundError(f"JSON file not found: {full_path.resolve()}")
    with open(full_path, encoding="utf-8") as f:
        return json.load(f)
