# Cram Kit

## Repository

A Claude Code skill that turns study text/topics into cached summaries, flashcards, quizzes, and printable practice activities as HTML. Read `README.md` before making changes — it documents the project pitch and usage. Read `docs/architecture.md` for the domain model and the check/save flow. Significant, hard-to-reverse decisions are recorded in `docs/adr/` — check it before revisiting one, and add an entry when making a new one.

## General Rules

- Keep changes scoped to the requested change.
- Prefer existing patterns over introducing new abstractions.
- Do not add dependencies unless they are necessary.
- Do not fill gaps with assumptions when the user hasn't given the information — ask, or mark it as pending.
- Do not claim a validation command passed unless it was actually run.
- Code, comments, commit messages, and documentation are always written in English.

## Git

- Do not create or switch branches unless explicitly requested.
- Do not create commits unless explicitly requested.
- Do not push unless explicitly requested.
- Keep commits focused on the requested change.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/) (`type: summary`).

## Documentation

### Audience

Future-you revisiting this months later, or someone browsing the portfolio to see how it works. Not onboarding material — keep it concise and skimmable.

### Content Rules

- State facts concisely. Avoid unnecessary explanations or trailing rationale.
- Do not document information that is already obvious from the repository structure or configuration.
- Do not invent features, API shapes, or future direction — mark undecided things as TODO.
- Document a capability only after it is implemented and verified.
- Use proper Markdown headings (`##`, `###`), not bold text as headings.

---

## Project-Specific Guidelines

### Source

- `.claude/skills/cram-kit/SKILL.md` - the instructions Claude follows when invoked.
- `.claude/skills/cram-kit/scripts/cram.py` - CLI entry point with six subcommands: `check` (hash the input, render from cache on a hit, or report a miss), `save` (write Claude-generated content to cache and render), `load` (print the cached summary/flashcards as JSON, for quiz/activity generation), `quiz-save` (render a quiz recap HTML, never touches the cache), `activity-save` (render a practice activity HTML, never touches the cache), and `list` (print every cached study set's tag, input path, and generation date).
- `.claude/skills/cram-kit/scripts/cache.py` - content hashing and cache read/write.
- `.claude/skills/cram-kit/scripts/render.py` - HTML templating.

Scripts live *inside* the skill's own folder (not at the repo root) so the whole `.claude/skills/cram-kit/` folder is self-contained and can be copied to another project or to a personal Claude Code skills directory (`~/.claude/skills/cram-kit/`) without leaving anything behind.

### Architecture

- This is a Claude Code skill, not a standalone app. Claude only generates new text on a cache miss or for quiz questions — it never re-derives already-cached content.
- The current working directory when the skill runs is wherever the user's session happens to be, never assumed to be this repo. `SKILL.md` references the script as `${CLAUDE_SKILL_DIR}/scripts/cram.py` (a path Claude Code resolves to this skill's own folder), never a bare `scripts/cram.py`. `CACHE_DIR` in `cache.py` is likewise anchored to the script's own file location, not the working directory, so the cache travels with the skill wherever it's installed.
- No separate LLM API/account: generation happens inside the Claude Code/Claude.ai session already running. Do not add an API client or SDK for a third-party LLM provider.
- Invoked explicitly as `/cram-kit <path-to-file>` — no natural-language auto-triggering. Also accepts pasted text or a short phrase directly (no existing file): Claude saves it as a file in the current working directory first, then proceeds the same way. An image pasted directly into the chat has no accessible source file, so it's transcribed to text instead of saved as-is — only an image given as an actual file path goes through the pipeline as an image.
- `/cram-kit quiz <path-to-file>` (leading "quiz" keyword) triggers the quiz flow instead of summary/flashcards generation.
- `/cram-kit activity <path-to-file>` (leading "activity" keyword) triggers a printable practice activity instead.
- `/cram-kit list` (no path) prints every cached study set.

### Caching

- Summary and flashcards are generated together in the same pass and cached, keyed by the input's content hash (raw bytes, not decoded text — works for images too). Each cache entry also records `input_path` (resolved to absolute) and `generated_at` (a UTC date), so `list` can show where each study set's source file lives without needing a separate index.
- Summary shape: `{title, sections: [{heading, body, tip?}]}` — `tip` is optional per section, only included where there's an actual memorable shortcut.
- Quiz questions are never cached — always regenerated fresh.
- Regenerating on request (user didn't like a result) bypasses the cache check and overwrites the existing entry for that input.
- Style guidance passed alongside new content (no file yet) is saved as part of the same input text, so it naturally busts the cache key. Guidance passed alongside an existing file path is applied only to that run's generation and not persisted anywhere.

### Quiz

- The one interactive piece of the skill — everything else (summary, flashcards) is static printable HTML; quiz is a live, one-question-at-a-time back-and-forth in chat, with feedback given immediately after each answer.
- Requires summary/flashcards to already exist for the input (generated first if missing) — quiz questions are drawn from that content, never from the raw input directly.
- Question types: multiple-choice, open-ended, and true/false, mixed unless the user requests otherwise.
- No fixed question count or natural end: continues until a user-requested count is reached or the user says to stop. Once distinct facts run out, later questions rephrase the same facts differently rather than ending — repeated exposure is the intent of "cram," not a flaw.
- Never cached — regenerated fresh every time, and `quiz-save` doesn't touch `.cache/` at all.
- After the last question, a recap HTML (`<set_tag>-quiz.html`) is written: every question, the user's answer, the correct answer, and whether they got it right — this is the answer-key equivalent for quiz, produced after the fact rather than upfront.

### Activity

- A printable practice worksheet — static HTML like summary/flashcards, not interactive like quiz. Drawn from the existing cached summary/flashcards, same prerequisite as quiz.
- Two kinds, decided by Claude's judgment based on the content/request (not something the user has to specify): **objective** (verifiable answers — math, fill-in-the-blank, calculations) gets an answer key as the last section; **subjective** (open-ended production — an essay, a letter) gets no answer key, since grading it requires a real person or a separate AI review, not this script.
- Subjective activities may optionally include a reading stimulus, guided prep questions, and a structure reminder — only whichever of those actually fits the task, none are mandatory beyond a title, writing prompt, and checklist.
- Never cached — regenerated fresh every time, and `activity-save` doesn't touch `.cache/` at all, same reasoning as quiz (more practice material each time, not a fixed worksheet).

### Content & Tooling

- Real study content and generated cache/output are personal — never commit them (see `.gitignore`).
- Not a publishable package: no `CONTRIBUTING.md`/`SECURITY.md`.

### Validation

Run `ruff format --check .`, `ruff check .` before considering a change done — CI (`.github/workflows/ci.yml`) runs the same on push/PR to `main`.

### Open Questions

- TODO: whether the kids' actual environment is Claude Code (where `SKILL.md` works today) or the Claude app — skills as built here are a Claude Code mechanism and may not carry over
