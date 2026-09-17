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
.quiz-score {
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 4mm;
}
.quiz-item {
  margin-bottom: 4mm;
  padding: 3mm;
  border: 1px solid #ccc;
  border-radius: 3px;
  page-break-inside: avoid;
}
.quiz-item.correct {
  border-color: #2e7d4f;
  background: #eaf6ef;
}
.quiz-item.incorrect {
  border-color: #b3261e;
  background: #fbeceb;
}
.quiz-type {
  font-size: 8px;
  letter-spacing: 1px;
  color: #999;
  text-transform: uppercase;
}
.quiz-question {
  font-size: 12px;
  font-weight: bold;
  margin: 1mm 0 2mm 0;
}
.quiz-answer-line {
  font-size: 11px;
  margin: 0 0 1mm 0;
}
.quiz-explanation {
  font-size: 10px;
  color: #555;
  margin: 1mm 0 0 0;
}
.activity-instructions {
  font-size: 11px;
  color: #2e7d4f;
  background: #eaf6ef;
  border: 0.5px solid #2e7d4f;
  border-radius: 3px;
  padding: 2mm 3mm;
  margin: 0 0 4mm 0;
}
.exercise {
  margin-bottom: 4mm;
  page-break-inside: avoid;
}
.exercise-number {
  font-weight: bold;
}
.write-lines {
  margin: 2mm 0;
}
.write-line {
  border-bottom: 1px solid #ccc;
  height: 7mm;
}
.answer-key-item {
  font-size: 11px;
  margin: 0 0 1mm 0;
}
.answer-key-section {
  page-break-before: always;
}
.stimulus-box {
  border: 1px solid #2e5090;
  border-radius: 3px;
  padding: 3mm 4mm;
  margin: 0 0 4mm 0;
  page-break-inside: avoid;
}
.stimulus-heading {
  font-weight: bold;
  color: #2e5090;
  margin: 0 0 1mm 0;
}
.stimulus-meta {
  font-size: 9px;
  color: #999;
  margin: 0 0 2mm 0;
}
.prep-question {
  margin-bottom: 3mm;
}
.structure-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10px;
  margin: 0 0 4mm 0;
}
.structure-table td {
  border: 1px solid #ccc;
  padding: 1.5mm 2mm;
  vertical-align: top;
}
.structure-label {
  font-weight: bold;
  background: #eaf0fb;
  white-space: nowrap;
}
.checklist-item {
  font-size: 11px;
  margin: 0 0 1.5mm 0;
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


def _render_quiz_item(item: dict) -> str:
    status = "correct" if item["correct"] else "incorrect"
    question = html.escape(item["question"])
    qtype = html.escape(item["type"])
    lines = [f'<div class="quiz-item {status}">']
    lines.append(f'<div class="quiz-type">{qtype}</div>')
    lines.append(f'<div class="quiz-question">{question}</div>')
    lines.append(
        f'<p class="quiz-answer-line">Your answer: {html.escape(item["user_answer"])}</p>'
    )
    lines.append(
        f'<p class="quiz-answer-line">Correct answer: {html.escape(item["correct_answer"])}</p>'
    )
    explanation = item.get("explanation")
    if explanation:
        lines.append(f'<p class="quiz-explanation">{html.escape(explanation)}</p>')
    lines.append("</div>")
    return "\n".join(lines)


def render_quiz_html(questions: list[dict], set_tag: str) -> str:
    title = html.escape(f"{set_tag} — Quiz Results")
    correct_count = sum(1 for q in questions if q["correct"])
    score = f"Score: {correct_count}/{len(questions)}"
    items_html = "\n".join(_render_quiz_item(q) for q in questions)

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
<p class="quiz-score">{score}</p>
{items_html}
</div>
</body>
</html>
"""


def _render_write_lines(count: int) -> str:
    lines = "\n".join('<div class="write-line"></div>' for _ in range(count))
    return f'<div class="write-lines">{lines}</div>'


def _render_exercise(exercise: dict) -> str:
    number = html.escape(str(exercise["number"]))
    prompt = html.escape(exercise["prompt"])
    lines = _render_write_lines(exercise.get("lines", 2))
    return (
        f'<div class="exercise"><p><span class="exercise-number">{number}.</span> '
        f"{prompt}</p>{lines}</div>"
    )


def _render_objective_section(section: dict) -> str:
    heading = html.escape(section["heading"])
    exercises_html = "\n".join(_render_exercise(e) for e in section["exercises"])
    return f'<div class="section"><h2>{heading}</h2>{exercises_html}</div>'


def _render_answer_key(answer_key: list[dict]) -> str:
    items = "\n".join(
        f'<p class="answer-key-item"><strong>{html.escape(str(a["number"]))}.</strong> '
        f"{html.escape(a['answer'])}</p>"
        for a in answer_key
    )
    return f'<div class="section answer-key-section"><h2>Answer Key</h2>{items}</div>'


def _render_objective_activity(activity: dict) -> str:
    parts = []
    instructions = activity.get("instructions")
    if instructions:
        parts.append(
            f'<p class="activity-instructions">{html.escape(instructions)}</p>'
        )
    parts.extend(_render_objective_section(s) for s in activity["sections"])
    parts.append(_render_answer_key(activity["answer_key"]))
    return "\n".join(parts)


def _render_stimulus(stimulus: dict) -> str:
    heading = html.escape(stimulus["heading"])
    meta = stimulus.get("meta")
    meta_html = f'<p class="stimulus-meta">{html.escape(meta)}</p>' if meta else ""
    body = html.escape(stimulus["body"])
    return (
        f'<div class="stimulus-box"><p class="stimulus-heading">{heading}</p>'
        f"{meta_html}<p>{body}</p></div>"
    )


def _render_prep_question(question: dict) -> str:
    prompt = html.escape(question["prompt"])
    lines = _render_write_lines(question.get("lines", 1))
    return f'<div class="prep-question"><p>{prompt}</p>{lines}</div>'


def _render_structure_table(rows: list[dict]) -> str:
    rows_html = "\n".join(
        f'<tr><td class="structure-label">{html.escape(r["label"])}</td>'
        f"<td>{html.escape(r['description'])}</td></tr>"
        for r in rows
    )
    return f'<table class="structure-table">{rows_html}</table>'


def _render_checklist(items: list[str]) -> str:
    items_html = "\n".join(
        f'<p class="checklist-item">☐ {html.escape(item)}</p>' for item in items
    )
    return f'<div class="section"><h2>Checklist</h2>{items_html}</div>'


def _render_subjective_activity(activity: dict) -> str:
    parts = []
    instructions = activity.get("instructions")
    if instructions:
        parts.append(
            f'<p class="activity-instructions">{html.escape(instructions)}</p>'
        )

    stimulus = activity.get("stimulus")
    if stimulus:
        parts.append(_render_stimulus(stimulus))

    prep_questions = activity.get("prep_questions")
    if prep_questions:
        questions_html = "\n".join(_render_prep_question(q) for q in prep_questions)
        parts.append(
            f'<div class="section"><h2>Before You Write</h2>{questions_html}</div>'
        )

    structure = activity.get("structure_reminder")
    if structure:
        parts.append(
            f'<div class="section"><h2>Structure Reminder</h2>'
            f"{_render_structure_table(structure)}</div>"
        )

    writing_prompt = html.escape(activity["writing_prompt"])
    writing_lines = _render_write_lines(activity.get("writing_lines", 14))
    parts.append(
        f'<div class="section"><h2>Your Turn</h2><p>{writing_prompt}</p>{writing_lines}</div>'
    )

    checklist = activity.get("checklist")
    if checklist:
        parts.append(_render_checklist(checklist))

    return "\n".join(parts)


def render_activity_html(activity: dict) -> str:
    title = html.escape(activity["title"])
    if activity["type"] == "objective":
        body_html = _render_objective_activity(activity)
    else:
        body_html = _render_subjective_activity(activity)

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
{body_html}
</div>
</body>
</html>
"""


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
