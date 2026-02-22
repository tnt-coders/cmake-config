"""Doxygen input filter that converts GitHub Flavored Markdown admonitions to Doxygen commands."""

import re
import sys

ADMONITION_MAP = {
    "NOTE": "note",
    "TIP": "remark",
    "IMPORTANT": "attention",
    "WARNING": "warning",
    "CAUTION": "warning",
}

ADMONITION_RE = re.compile(r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$")
CONTINUATION_RE = re.compile(r"^>\s?(.*)$")


def convert(lines):
    out = []
    i = 0
    while i < len(lines):
        m = ADMONITION_RE.match(lines[i])
        if m:
            command = ADMONITION_MAP[m.group(1)]
            body_lines = []
            i += 1
            while i < len(lines):
                cm = CONTINUATION_RE.match(lines[i])
                if cm:
                    body_lines.append(cm.group(1))
                    i += 1
                else:
                    break
            body = " ".join(line for line in body_lines if line).strip()
            out.append(f"@{command} {body}")
        else:
            out.append(lines[i])
            i += 1
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: doxygen-github-admonitions.py <file>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n\r") for line in f]

    sys.stdout.reconfigure(encoding="utf-8")
    for line in convert(lines):
        print(line)


if __name__ == "__main__":
    main()
