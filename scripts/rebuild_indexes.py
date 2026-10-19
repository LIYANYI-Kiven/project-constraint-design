"""Rebuild the development-log and rules indexes from Markdown frontmatter."""
from __future__ import annotations

import argparse
from pathlib import Path


def parse_frontmatter(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    data: dict[str, object] = {}
    current: str | None = None
    for line in text[4:end].splitlines():
        if line.startswith("  - ") and current:
            value = data.setdefault(current, [])
            if isinstance(value, list):
                value.append(line[4:].strip())
            continue
        if ":" not in line or line.startswith(" "):
            continue
        key, raw = line.split(":", 1)
        current = key.strip()
        raw = raw.strip().strip('"')
        data[current] = [] if raw == "" else raw
    return data


def cell(value: object) -> str:
    if isinstance(value, list):
        return "、".join(str(item) for item in value) or "—"
    text = str(value or "—").replace("|", "\\|")
    return text or "—"


def rows(directory: Path) -> list[dict[str, object]]:
    parsed = []
    for path in sorted(directory.glob("*.md")):
        if path.name == "index.md":
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        meta["file"] = path.name
        parsed.append(meta)
    return parsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    logs = root / "docs" / "development-log"
    rules = root / "docs" / "rules"
    if not logs.is_dir() or not rules.is_dir():
        raise SystemExit("缺少 docs/development-log 或 docs/rules，先运行 init_docs.py")

    log_lines = [
        "# 开发日志索引",
        "",
        "后续 agent 修改项目前先读本文件，再打开相关日志。长期约束以 `docs/rules/index.md` 为准。",
        "",
        "| 日期 | 标题 | 状态 | 日志 | 已提升规则 |",
        "| --- | --- | --- | --- | --- |",
    ]
    log_rows = rows(logs)
    if not log_rows:
        log_lines.append("|  |  |  | 尚无日志 |  |")
    for item in log_rows:
        name = cell(item.get("file"))
        log_lines.append(
            f"| {cell(item.get('date'))} | {cell(item.get('title'))} | {cell(item.get('status'))} | [{name}]({name}) | {cell(item.get('promoted_rules'))} |"
        )

    rule_lines = [
        "# 规则索引",
        "",
        "后续 agent 修改项目前先遵守状态为 active 的规则。",
        "",
        "| 编号 | 标题 | 状态 | 规则 | 来源日志 |",
        "| --- | --- | --- | --- | --- |",
    ]
    rule_rows = rows(rules)
    if not rule_rows:
        rule_lines.append("|  |  |  | 尚无规则 |  |")
    for item in rule_rows:
        name = cell(item.get("file"))
        rule_lines.append(
            f"| {cell(item.get('id'))} | {cell(item.get('title'))} | {cell(item.get('status'))} | [{name}]({name}) | {cell(item.get('source_logs'))} |"
        )

    (logs / "index.md").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    (rules / "index.md").write_text("\n".join(rule_lines) + "\n", encoding="utf-8")
    print({"logs": len(log_rows), "rules": len(rule_rows)})


if __name__ == "__main__":
    main()
