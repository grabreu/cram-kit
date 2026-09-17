def render_html(summary: str, flashcards: list[dict], set_tag: str) -> str:
    cards_html = "\n".join(
        f"<div><p><strong>Q:</strong> {card['front']}</p>"
        f"<p><strong>A:</strong> {card['back']}</p></div>"
        for card in flashcards
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{set_tag}</title>
</head>
<body>
<h1>Summary</h1>
<pre>{summary}</pre>
<h1>Flashcards</h1>
{cards_html}
</body>
</html>
"""
