def render_summary_html(content: str, set_tag: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{set_tag}</title>
</head>
<body>
<pre>{content}</pre>
</body>
</html>
"""
