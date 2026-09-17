# Cram Kit

## Repository

A Claude Code skill that turns study text/topics into cached summaries, flashcards, and quizzes as printable HTML. Read `README.md` before making changes — it documents the project pitch and usage.

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
- `scripts/cram.py` - CLI entry point with two subcommands: `check` (hash the input, render from cache on a hit, or report a miss) and `save` (write Claude-generated content to cache and render).
- `scripts/cache.py` - content hashing and cache read/write.
- `scripts/render.py` - HTML templating.

### Architecture

- This is a Claude Code skill, not a standalone app. Claude only generates new text on a cache miss or for quiz questions — it never re-derives already-cached content.
- No separate LLM API/account: generation happens inside the Claude Code/Claude.ai session already running. Do not add an API client or SDK for a third-party LLM provider.
- Invoked explicitly as `/cram-kit <path-to-file>` — no natural-language auto-triggering. Also accepts pasted text or a short phrase directly (no existing file): Claude saves it as a file in the current working directory first, then proceeds the same way. An image pasted directly into the chat has no accessible source file, so it's transcribed to text instead of saved as-is — only an image given as an actual file path goes through the pipeline as an image.

### Caching

- Summary and flashcards are generated together in the same pass and cached, keyed by the input's content hash (raw bytes, not decoded text — works for images too).
- Summary shape: `{title, sections: [{heading, body, tip?}]}` — `tip` is optional per section, only included where there's an actual memorable shortcut.
- Quiz questions are never cached — always regenerated fresh.
- Regenerating on request (user didn't like a result) bypasses the cache check and overwrites the existing entry for that input.

### Content & Tooling

- Real study content and generated cache/output are personal — never commit them (see `.gitignore`).
- Not a publishable package: no `CONTRIBUTING.md`/`SECURITY.md`.

### Validation

Run `ruff format --check .`, `ruff check .` before considering a change done — CI (`.github/workflows/ci.yml`) runs the same on push/PR to `main`.

### Open Questions

- TODO: how the kids actually access/run this (Claude Code terminal vs. Claude app)
- TODO: allow passing generation style guidance (e.g. "be more direct", "more detailed") alongside the path — the cache key is currently just the input's content hash, so this needs a decision on whether guidance busts the cache key or just bypasses the cache for that run
