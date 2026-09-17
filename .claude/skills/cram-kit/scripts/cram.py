import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

from cache import content_hash, list_cache, read_cache, write_cache
from render import render_activity_html, render_html, render_quiz_html


def _render_and_write(input_path: Path, data: dict) -> None:
    html = render_html(data["summary"], data["flashcards"], data["set_tag"])
    output_path = input_path.with_name(f"{data['set_tag']}-summary.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"wrote {output_path}")


def cmd_check(input_path: Path) -> None:
    digest = content_hash(input_path.read_bytes())
    cached = read_cache(digest)

    if cached is not None:
        print(f"cache hit ({digest[:8]})")
        _render_and_write(input_path, cached)
    else:
        print(f"cache miss ({digest[:8]})")
        print(f"read {input_path}, generate summary + flashcards, then run:")
        print(f"  save {input_path} <json-file>")


def cmd_save(input_path: Path, json_path: Path) -> None:
    digest = content_hash(input_path.read_bytes())
    generated = json.loads(json_path.read_text(encoding="utf-8"))

    data = {
        "summary": generated["summary"],
        "flashcards": generated["flashcards"],
        "set_tag": generated.get("set_tag") or input_path.stem,
        "input_path": str(input_path.resolve()),
        "generated_at": datetime.now(UTC).date().isoformat(),
    }
    write_cache(digest, data)
    _render_and_write(input_path, data)


def cmd_list() -> None:
    entries = list_cache()

    if not entries:
        print("no study sets generated yet")
        return

    for entry in entries:
        set_tag = entry.get("set_tag", "?")
        input_path = entry.get("input_path", "?")
        generated_at = entry.get("generated_at", "?")
        print(f"{set_tag} - {input_path} (generated {generated_at})")


def cmd_load(input_path: Path) -> None:
    digest = content_hash(input_path.read_bytes())
    cached = read_cache(digest)

    if cached is None:
        print(f"no cache entry ({digest[:8]}) - run check/save on this input first")
        raise SystemExit(1)

    print(json.dumps(cached))


def cmd_quiz_save(input_path: Path, json_path: Path) -> None:
    generated = json.loads(json_path.read_text(encoding="utf-8"))
    questions = generated["questions"]
    set_tag = generated.get("set_tag") or input_path.stem

    html = render_quiz_html(questions, set_tag)
    output_path = input_path.with_name(f"{set_tag}-quiz.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"wrote {output_path}")


def cmd_activity_save(input_path: Path, json_path: Path) -> None:
    generated = json.loads(json_path.read_text(encoding="utf-8"))
    set_tag = generated.get("set_tag") or input_path.stem

    html = render_activity_html(generated)
    output_path = input_path.with_name(f"{set_tag}-activity.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"wrote {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("input_path", type=Path)

    save_parser = subparsers.add_parser("save")
    save_parser.add_argument("input_path", type=Path)
    save_parser.add_argument("json_path", type=Path)

    load_parser = subparsers.add_parser("load")
    load_parser.add_argument("input_path", type=Path)

    quiz_save_parser = subparsers.add_parser("quiz-save")
    quiz_save_parser.add_argument("input_path", type=Path)
    quiz_save_parser.add_argument("json_path", type=Path)

    activity_save_parser = subparsers.add_parser("activity-save")
    activity_save_parser.add_argument("input_path", type=Path)
    activity_save_parser.add_argument("json_path", type=Path)

    subparsers.add_parser("list")

    args = parser.parse_args()

    if args.command == "check":
        cmd_check(args.input_path)
    elif args.command == "save":
        cmd_save(args.input_path, args.json_path)
    elif args.command == "load":
        cmd_load(args.input_path)
    elif args.command == "quiz-save":
        cmd_quiz_save(args.input_path, args.json_path)
    elif args.command == "activity-save":
        cmd_activity_save(args.input_path, args.json_path)
    else:
        cmd_list()


if __name__ == "__main__":
    main()
