import hashlib
import json
from pathlib import Path


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


CACHE_DIR = Path(".cache")


def cache_path(digest: str) -> Path:
    return CACHE_DIR / f"{digest}.json"


def read_cache(digest: str) -> dict | None:
    path = cache_path(digest)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_cache(digest: str, data: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path(digest).write_text(json.dumps(data, indent=2), encoding="utf-8")
