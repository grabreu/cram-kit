# Print output is HTML/CSS, not a generated PDF

Study material renders as HTML with print-oriented CSS (`@page`, `page-break-*`) instead of a PDF built with a library like `reportlab` — the tool used for the hand-built study materials this project replaces. Reportlab worked there, but it's a real dependency and its own templating code that cram-kit doesn't otherwise need.

The HTML approach reuses the browser's own print pipeline (Ctrl+P → Save as PDF), so the same output serves on-screen viewing and printing without a separate render step.

**Consequences**: no PDF-library dependency, but layout fidelity depends on the browser's print engine rather than being pixel-controlled. Revisit if precise page layout ever becomes a real requirement.
