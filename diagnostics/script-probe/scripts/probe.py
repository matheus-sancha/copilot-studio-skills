"""Sandbox probe. Standard library only - it must not depend on anything to report that nothing is available."""
import sys
import platform

print("SCRIPT-EXECUTION-OK-7741")
print("python:", sys.version.replace("\n", " "))
print("platform:", platform.platform())
print("--- package availability ---")

candidates = [
    "openpyxl",      # xlsx
    "xlsxwriter",    # xlsx
    "docx",          # python-docx
    "pptx",          # python-pptx
    "reportlab",     # pdf
    "fpdf",          # pdf
    "pypdf",         # pdf read
    "PIL",           # images
    "pandas",
    "numpy",
    "matplotlib",
    "requests",      # expected to be useless: no network
    "bs4",
    "lxml",
    "yaml",
    "jinja2",
]

available, missing = [], []
for name in candidates:
    try:
        __import__(name)
        available.append(name)
    except Exception:
        missing.append(name)

print("available:", ", ".join(available) if available else "(none)")
print("missing:  ", ", ".join(missing) if missing else "(none)")
print("--- end ---")
