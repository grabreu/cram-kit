# cram-kit

[![CI](https://github.com/grabreu/cram-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/grabreu/cram-kit/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/grabreu/cram-kit?style=flat-square)](LICENSE)

Claude Code skill that turns study text/topics into cached summaries, flashcards, quizzes, and printable practice activities as HTML.

## Tech stack

Python · ruff

## Usage

```shell
/cram-kit <path-to-file>
```

Also accepts pasted text, a short topic phrase, or an image directly — no existing file needed:

```shell
/cram-kit Explain the water cycle
```

For a quiz instead of a summary, add `quiz` — an interactive, one-question-at-a-time session in chat, with a printable recap (score + answer key) written at the end:

```shell
/cram-kit quiz <path-to-file>
```

For a printable practice worksheet instead, add `activity` — math-style exercises get an answer key at the end, open-ended writing tasks (an essay, a letter) don't, since those need a person or a separate AI review to grade:

```shell
/cram-kit activity <path-to-file>
```

To see what's already been generated:

```shell
/cram-kit list
```

## Development

Requires Python 3.11+.

```bash
pip install ruff
ruff format --check .
ruff check .
```

## License

Licensed under the [MIT License](LICENSE).
