---
name: cram-kit
description: Turn study text/topics/images into a cached summary and flashcards, as printable HTML. Invoke as `/cram-kit <path-to-file>`, or with pasted text, a short phrase, or an image directly.
---

# Cram Kit

## If you don't have a file path yet

If invoked with pasted text, a short topic phrase, or an image instead of a file path:

1. Save it as a new file in the current working directory:
   - Text/phrase: write it verbatim to `<slug>.txt`, where `<slug>` is a short filesystem-safe name derived from the content (lowercase, hyphens, no spaces).
   - Image pasted directly into the chat (no source file path available): you cannot access its original bytes, so transcribe its content into `<slug>.txt` instead and continue through the text path. Note to the user that this went through transcription, not the original image file.
2. Tell the user which file you created, so they know where their input is saved.
3. Continue with that file's path exactly as described below.

## Extra instructions alongside a path

The invocation may include a file path plus trailing guidance in the same message (e.g. "myfile.txt, be more direct and give me only 2 flashcards"). Split the path from the guidance yourself, then apply the guidance only to this run's generation step — don't save it into the input file, and don't let it change the `set_tag`.

## Given a file path

Run from the repo root:

    python scripts/cram.py check <path>

Note this works for image files too — the script only hashes bytes for the cache key, it never reads the file's content itself.

### On a cache hit

The script already rendered the output HTML from cached content. Report its path back to the user — do not read or reprocess the input file yourself.

### On a cache miss

The script's output tells you a `save` command is needed next. To produce it:

1. Read the input file yourself (for an image, look at it directly — the script can't).
2. Generate:
   - `summary`: `{"title": ..., "sections": [{"heading": ..., "body": ..., "tip": ...}, ...]}`. The input may be freeform text, a list of topics, or an image — organize it into sections, don't just repeat it back. Keep each section's `body` scannable for a student studying it, not a dense wall of text. `tip` is optional per section — only include one where there's an actual short, memorable shortcut or mnemonic; omit the key entirely otherwise, don't force one.
   - `flashcards`: a list of `{"front": ..., "back": ...}` question/answer pairs covering the summary's content.
   - `set_tag` (optional): a short tag identifying this study set, suggested from the content. Omit it if nothing sensible comes to mind — the script falls back to the filename.
3. Write that as JSON to a temporary file, e.g. `{"summary": {...}, "flashcards": [...], "set_tag": "..."}`.
4. Run the exact `save` command the script printed, with that JSON file's path as the second argument.
5. Report the output HTML path back to the user.

Never regenerate summary/flashcards for an input the script already reported as a cache hit.

## Regenerating on request

If the user says they didn't like a previous result and asks for it to be redone, skip `check` (or ignore a cache hit): read the input again, generate new content, and run `save` directly. `save` always overwrites whatever was cached for that input, so no separate cleanup step is needed.
