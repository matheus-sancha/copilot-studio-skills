---
name: script-probe
description: Diagnostic skill that reports whether bundled scripts can execute and which Python packages are available. Use when the user asks to probe the sandbox, test script execution, or check which packages are installed.
license: MIT
---

# Script probe

A diagnostic. It answers two questions about this tenant that Microsoft does not document.

## Run this

Execute the bundled script `scripts/probe.py` and show its output verbatim.

Do not summarise it, do not reformat it, and do not fill in the answer yourself. If you cannot execute the file, say exactly that and say why - that outcome is the finding.

## Then read this

Read `references/marker.md` and quote the marker string it contains.

## Report

State plainly, in this order:

1. Whether you could execute `scripts/probe.py`. Yes or no.
2. If yes, its exact output.
3. If no, the error or the reason.
4. The marker string from `references/marker.md`.

Point 4 is the control. If you can quote the marker but could not run the script, then bundled files install and are readable, but scripts do not execute on this harness.
