"""Check that a goal contract contains actionable goals and acceptance gates."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = ("# Goal", "## Non-goals", "## Runtime boundary", "## Success criteria", "## Allowed scope", "## Evidence", "## Recovery")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    path = args.root.expanduser().resolve() / "docs" / "goals" / "active.md"
    if not path.is_file():
        raise SystemExit(f"缺少目标契约：{path}")
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in REQUIRED if heading not in text]
    placeholders = [marker for marker in ("待项目审查", "待项目负责人", "TODO", "TBD") if marker in text]
    criteria = re.findall(r"^- \[[ xX]\] .+", text, flags=re.MULTILINE)
    if missing or placeholders or not criteria:
        raise SystemExit({"ok": False, "missing": missing, "placeholders": placeholders, "criteria_count": len(criteria)})
    print({"ok": True, "path": str(path), "criteria_count": len(criteria)})


if __name__ == "__main__":
    main()
