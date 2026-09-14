---
name: cram-kit
description: Turn a study text/topics file into a cached, printable HTML summary. Invoke explicitly as `/cram-kit <path-to-file>`.
---

# Cram Kit

Given a file path argument, run the bundled script from the repo root:

    python scripts/cram.py <path>

Report the script's printed output (cache hit/miss, output file path) back to the user. Do not read or reprocess the input file yourself — the script owns hashing, caching, and templating.
