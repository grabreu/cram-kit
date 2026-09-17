---
name: cram-kit
description: Turn study text/topics/images into a cached summary and flashcards, or an interactive quiz, as printable HTML. Invoke as `/cram-kit <path-to-file>` (or `/cram-kit quiz <path-to-file>`), or with pasted text, a short phrase, or an image directly.
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

## Quiz

If the invocation starts with the word "quiz" (e.g. `/cram-kit quiz <path>`, or "quiz" plus pasted text/phrase/image), run an interactive quiz instead of the normal summary/flashcards flow:

1. Resolve the input to a file path first: if there's no existing file, follow "If you don't have a file path yet" above using the content after "quiz". If there's an existing file, follow "Given a file path" above as normal (generate and cache summary/flashcards on a miss, same as any other invocation) — a quiz always needs a summary/flashcards to draw from.
2. Once summary/flashcards exist (cached or freshly generated), load them:

       python scripts/cram.py load <path>

   This prints the cached `{"summary": ..., "flashcards": ..., "set_tag": ...}` as JSON — don't regenerate this content, just read it.
3. Generate a set of quiz questions from that content (mix of multiple-choice, open-ended, and true/false, unless the user's extra instructions say otherwise — the same "extra instructions alongside a path" handling above applies here too). Work out the correct answer for each question yourself, but don't reveal any of them yet.

   There is no fixed question count and no natural end. If the user asked for a specific number upfront (e.g. "30 questions"), stop after that many. Otherwise, keep going until the user says they're done (e.g. "chega", "só isso", "pode parar") — don't stop after some default number on your own. Either way, once the underlying content runs out of distinct facts to ask about, reuse the same facts across further questions, rephrased differently each time (different wording, different question type, a different angle on the same fact) rather than stopping. Repeated exposure to the same material in varied forms is the point of "cram" — it's not a flaw to avoid.
4. Ask ONE question at a time in the chat, then stop and wait for the user's reply — don't ask the next question until they've answered the current one.
5. After each answer: judge it (for open-ended answers, judge whether the meaning is close enough, not an exact string match), give brief feedback and the correct answer, then either move to the next question or, if the user has signaled they're done, proceed to the recap below.
6. Once the quiz ends (count reached, or the user said to stop), write a JSON file capturing every question asked so far, shaped `{"questions": [{"type": ..., "question": ..., "options": [...], "correct_answer": ..., "user_answer": ..., "correct": true/false, "explanation": ...}, ...], "set_tag": ...}` (`options` only for multiple-choice, `explanation` optional), then run:

       python scripts/cram.py quiz-save <path> <json-file>

7. Report the quiz recap HTML path and a quick score summary (e.g. "4/6 correct") in chat.

Quiz results are never cached — `quiz-save` doesn't touch `.cache/` at all, only `check`/`save` do.
