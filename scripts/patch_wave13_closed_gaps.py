#!/usr/bin/env python3
"""Close leftover unread-licence gaps on records wave 13 actually read.

The merge attaches a licence object and new claims, but it does not rewrite
the original gap/flag text that said the number had never been read. Those
sentences would otherwise render as current facts on records that now have a
regulator page. Historical wording is preserved behind a CLOSED prefix.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "data" / "research.json"
DATE = "2026-09-15"
UNREAD = re.compile(
    r"NOT read on CSLB|No CSLB licence-detail page was read|has NOT been read on CSLB",
    re.I,
)


def main() -> int:
    data = json.loads(TARGET.read_text(encoding="utf-8"))
    gaps = flags = 0
    for b in data["businesses"]:
        lic = b.get("license")
        if not lic:
            continue
        number = str(lic["number"])
        closed = (
            f"CLOSED {DATE}: licence {number} was read directly at CSLB "
            f"({lic['status']}, classes {', '.join(lic.get('classes') or [])}). "
            "The unread-licence statement below is retained as the earlier gap, not as the current fact. "
        )
        new_gaps = []
        for g in b.get("gaps") or []:
            if UNREAD.search(g) and not g.startswith("CLOSED "):
                new_gaps.append(closed + g)
                gaps += 1
            else:
                new_gaps.append(g)
        b["gaps"] = new_gaps
        for f in b.get("flags") or []:
            text = f.get("text") or ""
            if UNREAD.search(text) and not text.startswith("CLOSED "):
                f["text"] = closed + text
                if f.get("level") == "hold" and lic.get("status") == "active":
                    f["level"] = "notice"
                flags += 1
    TARGET.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"closed leftover unread-licence wording: {gaps} gaps, {flags} flags")
    return 0


if __name__ == "__main__":
    sys.exit(main())
