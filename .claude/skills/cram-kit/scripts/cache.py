import hashlib
import json
from pathlib import Path


def content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"


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


def list_cache() -> list[dict]:
    if not CACHE_DIR.exists():
        return []
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CACHE_DIR.glob("*.json"))
    ]
