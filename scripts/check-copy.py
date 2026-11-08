#!/usr/bin/env python3
"""Copy check for bulkstem.com: every quoted string of the brief's CONTENT section must appear on the page.

Usage: python3 scripts/check-copy.py <path to landing-prompt-lovable.md> [path to index.html]

The brief is docs/product/landing-prompt-lovable.md in the Summermark repository. The script reads the
```text block of the brief, takes every double-quoted string of 4 or more characters after the line that
starts with "CONTENT (use this copy" and reports every string missing from the visible text of index.html.
On a line that offers alternatives in square brackets ([ROMAN: ...], [CAPTAIN: ...]) only the quoted
strings before the first "[" count. It also fails on retired v1 phrases, on a wrong <title> and on a meta
description that differs from the hero subheadline. Exit code 0 when everything matches, 1 otherwise.
Python 3 standard library only.
"""

import html
import pathlib
import re
import sys

EXPECTED_TITLE = "BulkStem — voyage fuel and cargo planning for bulk-carrier officers"

RETIRED_V1_PHRASES = [
    "with every formula shown",
    "(ballast, laden, in port, eco)",
    "Bunker planning",
    "clock changes are explicit events",
    "validated against real voyages before release",
    "Opens Voyage Fuel Planner",
    "Sea margin, stated",
]

CONTENT_MARKER = "CONTENT (use this copy"
QUOTED = re.compile(r'"([^"]+)"')


def normalise(text: str) -> str:
    text = (text.replace("“", '"').replace("”", '"')
                .replace("‘", "'").replace("’", "'")
                .replace(" ", " "))
    return re.sub(r"\s+", " ", text).strip()


def brief_text_block(brief: str) -> str:
    match = re.search(r"^```text\n(.*?)^```", brief, re.S | re.M)
    if not match:
        sys.exit("error: no ```text block in the brief")
    return match.group(1)


def expected_strings(brief: str) -> tuple[list[str], str]:
    """Return the quoted strings of the CONTENT section and the hero subheadline."""
    lines = brief_text_block(brief).splitlines()
    start = next((i for i, line in enumerate(lines) if line.startswith(CONTENT_MARKER)), None)
    if start is None:
        sys.exit(f'error: no line starting with "{CONTENT_MARKER}" in the brief')
    strings, subheadline = [], ""
    for line in lines[start + 1:]:
        line = normalise(line)
        if "[" in line:
            line = line.split("[", 1)[0]
        found = [s for s in QUOTED.findall(line) if len(s) >= 4]
        if line.lstrip("- ").startswith("Subheadline:") and found:
            subheadline = found[0]
        strings.extend(found)
    if not subheadline:
        sys.exit("error: no hero subheadline in the brief")
    return strings, subheadline


def page_text(page: str) -> str:
    page = re.sub(r"<!--.*?-->", " ", page, flags=re.S)
    page = re.sub(r"<(script|style)\b[^>]*>.*?</\1\s*>", " ", page, flags=re.S | re.I)
    page = re.sub(r"<[^>]+>", " ", page)
    return normalise(html.unescape(page))


def tag_content(page: str, pattern: str) -> str | None:
    match = re.search(pattern, page, re.S | re.I)
    return normalise(html.unescape(match.group(1))) if match else None


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    brief = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    index_path = pathlib.Path(sys.argv[2]) if len(sys.argv) == 3 else pathlib.Path(__file__).resolve().parent.parent / "index.html"
    page = index_path.read_text(encoding="utf-8")

    strings, subheadline = expected_strings(brief)
    text = page_text(page)
    # Inline links and tags split words with spaces; compare with spaces before punctuation removed as well.
    text_tight = re.sub(r" ([.,;:!?)])", r"\1", text)
    errors = []

    missing = [s for s in strings if s not in text and s not in text_tight]
    for s in missing:
        errors.append(f"missing: {s}")

    raw = normalise(html.unescape(page))
    for phrase in RETIRED_V1_PHRASES:
        if phrase in raw:
            errors.append(f"retired v1 phrase present: {phrase}")

    title = tag_content(page, r"<title>(.*?)</title>")
    if title != EXPECTED_TITLE:
        errors.append(f"title is {title!r}, expected {EXPECTED_TITLE!r}")

    description = tag_content(page, r'<meta\s+name="description"\s+content="([^"]*)"')
    if description != subheadline:
        errors.append("meta description differs from the hero subheadline")

    print(f"{len(strings)} brief strings checked against {index_path}, {len(missing)} missing; "
          f"{len(RETIRED_V1_PHRASES)} retired phrases checked; title and meta description checked.")
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
