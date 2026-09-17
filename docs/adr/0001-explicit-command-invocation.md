# Invocation is explicit (/cram-kit), never inferred from conversation

`/cram-kit` requires the user to type the command explicitly — a bare path, a phrase, an image, or "quiz" plus any of those — rather than Claude inferring intent from ordinary conversation and triggering the skill on its own. A `SKILL.md` description broad enough for Claude to auto-trigger on any study-related request was the realistic alternative, and was rejected early on.

This keeps behavior predictable for a young user: the skill only runs when asked for by name, never as a side effect of an unrelated conversation.

**Consequences**: the user has to know `/cram-kit` exists and its handful of forms — there's no fallback if they just ask "can you summarize this?" in plain conversation.
