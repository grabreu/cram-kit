import argparse
from pathlib import Path

from cache import content_hash, read_cache, write_cache
from render import render_summary_html


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=Path)
    args = parser.parse_args()

    text = args.input_path.read_text(encoding="utf-8")
    digest = content_hash(text)
    cached = read_cache(digest)

    if cached is not None:
        print(f"cache hit ({digest[:8]})")
        summary = cached["summary"]
        set_tag = cached["set_tag"]
    else:
        print(f"cache miss ({digest[:8]}) — generating")
        summary = text
        set_tag = args.input_path.stem
        write_cache(digest, {"summary": summary, "set_tag": set_tag})

    html = render_summary_html(summary, set_tag)
    output_path = args.input_path.with_name(f"{set_tag}-summary.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
