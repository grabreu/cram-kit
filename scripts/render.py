import html

CARDS_PER_PAGE = 8

_STYLE = """
* { box-sizing: border-box; }
body {
  font-family: Arial, Helvetica, sans-serif;
  margin: 0;
  background: #eee;
  color: #222;
}
.page {
  max-width: 190mm;
  margin: 10mm auto;
  background: #fff;
  padding: 10mm;
}
.title {
  font-size: 20px;
  font-weight: bold;
  color: #2e5090;
  margin: 0 0 4mm 0;
}
.section {
  margin-bottom: 5mm;
  page-break-inside: avoid;
}
.section h2 {
  font-size: 13px;
  color: #fff;
  background: #2e5090;
  padding: 2mm 3mm;
  margin: 0 0 2mm 0;
  border-radius: 3px;
}
.section p {
  font-size: 12px;
  line-height: 1.4;
  margin: 0 0 2mm 0;
}
.tip {
  font-size: 11px;
  color: #2e7d4f;
  background: #eaf6ef;
  border: 0.5px solid #2e7d4f;
  border-radius: 3px;
  padding: 2mm 3mm;
  margin: 2mm 0 0 0;
}
.tip::before {
  content: "Tip: ";
  font-weight: bold;
}
.cards-page {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 6mm;
  max-width: 190mm;
  margin: 10mm auto;
  background: #fff;
  padding: 10mm;
}
.card {
  border: 1px solid #333;
  border-radius: 4px;
  display: flex;
  align-items: stretch;
  min-height: 45mm;
  position: relative;
  page-break-inside: avoid;
  break-inside: avoid;
}
.card-meta {
  position: absolute;
  top: 2px;
  left: 6px;
  font-size: 7px;
  color: #999;
}
.card-half {
  flex: 1;
  padding: 6mm 4mm 4mm 4mm;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
}
.card-label {
  font-size: 8px;
  letter-spacing: 1px;
  color: #999;
  margin-bottom: 4px;
}
.card-text {
  font-size: 12px;
  line-height: 1.35;
}
.card-front .card-text {
  font-weight: bold;
}
.fold-line {
  width: 0;
  border-left: 1px dashed #999;
  margin: 4mm 0;
}
@media print {
  body { background: #fff; }
  .page, .cards-page {
    margin: 0;
    padding: 10mm;
    page-break-after: always;
  }
}
@page {
  size: A4;
  margin: 10mm;
}
"""


def _render_section(section: dict) -> str:
    heading = html.escape(section["heading"])
    body = html.escape(section["body"])
    tip = section.get("tip")
    tip_html = f'<p class="tip">{html.escape(tip)}</p>' if tip else ""
    return f'<div class="section"><h2>{heading}</h2><p>{body}</p>{tip_html}</div>'


def _render_card(index: int, set_tag: str, card: dict) -> str:
    front = html.escape(card["front"])
    back = html.escape(card["back"])
    tag = html.escape(set_tag)
    return f"""<div class="card">
<div class="card-meta">#{index} - {tag}</div>
<div class="card-half card-front">
<div class="card-label">QUESTION</div>
<div class="card-text">{front}</div>
</div>
<div class="fold-line"></div>
<div class="card-half card-back">
<div class="card-label">ANSWER</div>
<div class="card-text">{back}</div>
</div>
</div>"""


def _render_cards_pages(flashcards: list[dict], set_tag: str) -> str:
    cards = [_render_card(i, set_tag, c) for i, c in enumerate(flashcards, start=1)]
    pages = [
        cards[i : i + CARDS_PER_PAGE] for i in range(0, len(cards), CARDS_PER_PAGE)
    ]
    return "\n".join(f'<div class="cards-page">{"".join(page)}</div>' for page in pages)


def render_html(summary: dict, flashcards: list[dict], set_tag: str) -> str:
    title = html.escape(summary["title"])
    sections_html = "\n".join(_render_section(s) for s in summary["sections"])
    cards_pages_html = _render_cards_pages(flashcards, set_tag)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{_STYLE}</style>
</head>
<body>
<div class="page">
<h1 class="title">{title}</h1>
{sections_html}
</div>
{cards_pages_html}
</body>
</html>
"""
