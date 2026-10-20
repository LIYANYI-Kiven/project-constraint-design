"""Create the required memory folders without overwriting existing files."""
from __future__ import annotations

import argparse
from pathlib import Path


LOG_INDEX = """# 开发日志索引

后续 agent 修改项目前先读本文件，再打开相关日志。长期约束以 `docs/rules/index.md` 为准。

| 日期 | 标题 | 状态 | 日志 | 已提升规则 |
| --- | --- | --- | --- | --- |
|  |  |  | 尚无日志 |  |
"""

RULE_INDEX = """# 规则索引

后续 agent 修改项目前先遵守状态为 active 的规则。

| 编号 | 标题 | 状态 | 规则 | 来源日志 |
| --- | --- | --- | --- | --- |
|  |  |  | 尚无规则 |  |
"""


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return "kept"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return "created"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"项目目录不存在：{root}")
    docs = root / "docs"
    results = {
        "development_log_index": write_if_missing(docs / "development-log" / "index.md", LOG_INDEX),
        "rules_index": write_if_missing(docs / "rules" / "index.md", RULE_INDEX),
        "goals_directory": "created" if not (docs / "goals").exists() else "kept",
    }
    (docs / "goals").mkdir(parents=True, exist_ok=True)
    print(results)


if __name__ == "__main__":
    main()
