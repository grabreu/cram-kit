# Cram Kit

## Repository

A Claude Code skill that turns study text/topics into cached summaries, flashcards, and quizzes as printable HTML. Read `README.md` before making changes.

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

### Architecture

- This is a Claude Code skill, not a standalone app: `.claude/skills/cram-kit/SKILL.md` holds the instructions Claude follows; `scripts/` holds the bundled Python for the mechanical parts (content hashing, cache read/write, HTML templating). Claude only generates new text on a cache miss or for quiz questions — it never re-derives already-cached content.
- No separate LLM API/account: generation happens inside the Claude Code/Claude.ai session already running. Do not add an API client or SDK for a third-party LLM provider.
- Invoked explicitly as `/cram-kit <path-to-file>` — no natural-language auto-triggering.

### Caching

- Summary and flashcards are generated together in the same pass and cached, keyed by the input's content hash.
- Quiz questions are never cached — always regenerated fresh.

### Content & Tooling

- Real study content and generated cache/output are personal — never commit them (see `.gitignore`).
- Python: format/lint with `ruff`.
- Not a publishable package: no `CONTRIBUTING.md`/`SECURITY.md`.

### Open Questions

- TODO: HTML/CSS print template design
- TODO: how the kids actually access/run this (Claude Code terminal vs. Claude app)
