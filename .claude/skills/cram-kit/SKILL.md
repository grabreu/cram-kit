---
name: cram-kit
description: Turn a study text/topics file into a cached summary and flashcards, as printable HTML. Invoke explicitly as `/cram-kit <path-to-file>`.
---

# Cram Kit

Given a file path argument, run from the repo root:

    python scripts/cram.py check <path>

## On a cache hit

The script already rendered the output HTML from cached content. Report its path back to the user — do not read or reprocess the input file yourself.

## On a cache miss

The script's output tells you a `save` command is needed next. To produce it:

1. Read the input file yourself.
2. Generate:
   - `summary`: an organized summary of the content, structured with headings. The input may be freeform text or just a list of topics — organize it, don't just repeat it back.
   - `flashcards`: a list of `{"front": ..., "back": ...}` question/answer pairs covering the summary's content.
   - `set_tag` (optional): a short tag identifying this study set, suggested from the content. Omit it if nothing sensible comes to mind — the script falls back to the filename.
3. Write that as JSON to a temporary file, e.g. `{"summary": "...", "flashcards": [...], "set_tag": "..."}`.
4. Run the exact `save` command the script printed, with that JSON file's path as the second argument.
5. Report the output HTML path back to the user.

Never regenerate summary/flashcards for an input the script already reported as a cache hit.
