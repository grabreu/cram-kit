# Cache key hashes raw input bytes, not decoded text

`content_hash` hashes the input file's raw bytes (`read_bytes()`) rather than text decoded as UTF-8. Hashing decoded text was the original implementation, but it assumes a text file and crashes on binary input like an image.

Hashing bytes instead lets one `check`/`save` pipeline serve both text and image inputs unchanged — the script never needs to understand *what* it's hashing, only that identical bytes should hit the same cache entry.

**Consequences**: two files a human would call "the same content" but saved with different encodings or line endings produce different cache entries. Acceptable since inputs are either freshly materialized by Claude or a single fixed file, not the same content re-saved by hand.
