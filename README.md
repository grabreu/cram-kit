# cram-kit

[![CI](https://github.com/grabreu/cram-kit/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/grabreu/cram-kit/actions/workflows/ci.yml)
[![License](https://img.shields.io/github/license/grabreu/cram-kit?style=flat-square)](LICENSE)

Claude Code skill that turns study text/topics into cached summaries, flashcards, and quizzes as printable HTML.

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

## Development

Requires Python 3.11+.

```bash
pip install ruff
ruff format --check .
ruff check .
```

## License

Licensed under the [MIT License](LICENSE).
