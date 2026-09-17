---
name: cram-kit
description: Turn study text/topics/images into a cached summary and flashcards, an interactive quiz, or a printable practice activity, as HTML. Invoke as `/cram-kit <path-to-file>` (or `/cram-kit quiz <path-to-file>`, or `/cram-kit activity <path-to-file>`), with pasted text, a short phrase, or an image directly, or `/cram-kit list` to see what's already been generated.
---

# Cram Kit

## Locating the script

Every command below uses `${CLAUDE_SKILL_DIR}/scripts/cram.py` — `${CLAUDE_SKILL_DIR}` is this skill's own folder, resolved by Claude Code before you see this text, regardless of where it's installed (project-scoped or a personal skills directory) or what the current working directory happens to be. Never substitute a plain `scripts/cram.py` — the current working directory when this skill runs is wherever the user's session is, not this folder.

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

Run:

    python ${CLAUDE_SKILL_DIR}/scripts/cram.py check <path>

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
4. Run `save` with the input path and that JSON file's path (using `${CLAUDE_SKILL_DIR}/scripts/cram.py` as above, same as `check`).
5. Report the output HTML path back to the user.

Never regenerate summary/flashcards for an input the script already reported as a cache hit.

## Regenerating on request

If the user says they didn't like a previous result and asks for it to be redone, skip `check` (or ignore a cache hit): read the input again, generate new content, and run `save` directly. `save` always overwrites whatever was cached for that input, so no separate cleanup step is needed.

## Quiz

If the invocation starts with the word "quiz" (e.g. `/cram-kit quiz <path>`, or "quiz" plus pasted text/phrase/image), run an interactive quiz instead of the normal summary/flashcards flow:

1. Resolve the input to a file path first: if there's no existing file, follow "If you don't have a file path yet" above using the content after "quiz". If there's an existing file, follow "Given a file path" above as normal (generate and cache summary/flashcards on a miss, same as any other invocation) — a quiz always needs a summary/flashcards to draw from.
2. Once summary/flashcards exist (cached or freshly generated), load them:

       python ${CLAUDE_SKILL_DIR}/scripts/cram.py load <path>

   This prints the cached `{"summary": ..., "flashcards": ..., "set_tag": ...}` as JSON — don't regenerate this content, just read it.
3. Generate a set of quiz questions from that content (mix of multiple-choice, open-ended, and true/false, unless the user's extra instructions say otherwise — the same "extra instructions alongside a path" handling above applies here too). Work out the correct answer for each question yourself, but don't reveal any of them yet.

   There is no fixed question count and no natural end. If the user asked for a specific number upfront (e.g. "30 questions"), stop after that many. Otherwise, keep going until the user says they're done (e.g. "chega", "só isso", "pode parar") — don't stop after some default number on your own. Either way, once the underlying content runs out of distinct facts to ask about, reuse the same facts across further questions, rephrased differently each time (different wording, different question type, a different angle on the same fact) rather than stopping. Repeated exposure to the same material in varied forms is the point of "cram" — it's not a flaw to avoid.
4. Ask ONE question at a time in the chat, then stop and wait for the user's reply — don't ask the next question until they've answered the current one.
5. After each answer: judge it (for open-ended answers, judge whether the meaning is close enough, not an exact string match), give brief feedback and the correct answer, then either move to the next question or, if the user has signaled they're done, proceed to the recap below.
6. Once the quiz ends (count reached, or the user said to stop), write a JSON file capturing every question asked so far, shaped `{"questions": [{"type": ..., "question": ..., "options": [...], "correct_answer": ..., "user_answer": ..., "correct": true/false, "explanation": ...}, ...], "set_tag": ...}` (`options` only for multiple-choice, `explanation` optional), then run:

       python ${CLAUDE_SKILL_DIR}/scripts/cram.py quiz-save <path> <json-file>

7. Report the quiz recap HTML path and a quick score summary (e.g. "4/6 correct") in chat.

Quiz results are never cached — `quiz-save` doesn't touch `.cache/` at all, only `check`/`save` do.

## Activity

If the invocation starts with the word "activity" (e.g. `/cram-kit activity <path>`, or "activity" plus pasted text/phrase/image), generate a printable practice worksheet instead of the normal summary/flashcards flow or the interactive quiz.

1. Resolve the input and ensure summary/flashcards exist, same as the "Quiz" section above (steps 1-2: materialize/`check`/`save` if needed, then `load <path>` to read the cached content).
2. Decide which kind of activity fits what's being asked for:
   - **Objective** — the material has exercises with objectively verifiable answers (math problems, fill-in-the-blank, calculations, conversions). Include an answer key.
   - **Subjective** — the request is an open-ended production task (write an essay, a letter, a paragraph, an opinion piece). No answer key is possible here — a real person (or a separate AI review) has to read and judge it, not this script.

   This is a judgment call based on the content/request, not something the user has to specify — but if their extra instructions say which kind they want, follow that instead.
3. Generate the activity JSON, shaped by type:
   - **Objective**: `{"type": "objective", "title": ..., "instructions": ..., "sections": [{"heading": ..., "exercises": [{"number": 1, "prompt": ..., "lines": 2}, ...]}, ...], "answer_key": [{"number": 1, "answer": ...}, ...], "set_tag": ...}`. `instructions` is an optional short intro line. `lines` on an exercise is how many ruled lines to leave for working it out (omit for a sane default). Number exercises sequentially across all sections; `answer_key` must cover every exercise number.
   - **Subjective**: `{"type": "subjective", "title": ..., "instructions": ..., "stimulus": {"heading": ..., "meta": ..., "body": ...}, "prep_questions": [{"prompt": ..., "lines": 1}, ...], "structure_reminder": [{"label": ..., "description": ...}, ...], "writing_prompt": ..., "writing_lines": 14, "checklist": [...], "set_tag": ...}`. `stimulus` (a reading passage to react to), `prep_questions` (guided questions before the main writing task), and `structure_reminder` (a label/description table of the expected structure) are all optional — include only what actually fits the task (a math-adjacent writing task might skip `stimulus` entirely, for example). `writing_prompt` and `checklist` are the only required fields beyond `title`.
4. Write that JSON to a temporary file, then run:

       python ${CLAUDE_SKILL_DIR}/scripts/cram.py activity-save <path> <json-file>

5. Report the output HTML path back to the user. For a subjective activity, also mention that it has no answer key and offer to review what they write once they're done (a real person or an AI review is what grades it, not this script).

Activities are never cached — `activity-save` doesn't touch `.cache/` at all, and re-running produces a fresh set of exercises/prompts each time, same reasoning as quiz.

## List

If the invocation is exactly the word "list" (e.g. `/cram-kit list`), run:

    python ${CLAUDE_SKILL_DIR}/scripts/cram.py list

This prints every cached study set — Set tag, input file path, and the date it was generated — one per line. No input to resolve, no generation, no caching involved. Report the results back to the user as a readable list; if it prints "no study sets generated yet," say so plainly rather than treating it as an error.
