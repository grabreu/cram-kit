import argparse
import json
from pathlib import Path

from cache import content_hash, read_cache, write_cache
from render import render_html


def _render_and_write(input_path: Path, data: dict) -> None:
    html = render_html(data["summary"], data["flashcards"], data["set_tag"])
    output_path = input_path.with_name(f"{data['set_tag']}-summary.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"wrote {output_path}")


def cmd_check(input_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    digest = content_hash(text)
    cached = read_cache(digest)

    if cached is not None:
        print(f"cache hit ({digest[:8]})")
        _render_and_write(input_path, cached)
    else:
        print(f"cache miss ({digest[:8]})")
        print(f"read {input_path}, generate summary + flashcards, then run:")
        print(f"  python scripts/cram.py save {input_path} <json-file>")


def cmd_save(input_path: Path, json_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    digest = content_hash(text)
    generated = json.loads(json_path.read_text(encoding="utf-8"))

    data = {
        "summary": generated["summary"],
        "flashcards": generated["flashcards"],
        "set_tag": generated.get("set_tag") or input_path.stem,
    }
    write_cache(digest, data)
    _render_and_write(input_path, data)


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("input_path", type=Path)

    save_parser = subparsers.add_parser("save")
    save_parser.add_argument("input_path", type=Path)
    save_parser.add_argument("json_path", type=Path)

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args.input_path)
    else:
        cmd_save(args.input_path, args.json_path)


if __name__ == "__main__":
    main()
