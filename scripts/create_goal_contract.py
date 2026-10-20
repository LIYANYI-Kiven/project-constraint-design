"""Create a project goal contract without overwriting an existing one."""
from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATE = """---
title: 项目目标契约
status: active
owner: {owner}
updated: {updated}
---

# Goal

{goal}

## Non-goals

{non_goals}

## Runtime boundary

- 唯一启动入口：{startup}
- 必须保留的代码、配置、数据、模型或外部资源：待项目审查确认
- 明确禁止触碰的路径：待项目负责人确认

## Success criteria

{criteria}

## Allowed scope

{scope}

## Evidence

待项目审查后填写启动、功能、回归、数据完整性和安全检查的位置。

## Recovery

待项目审查后填写可验证的回滚方式。
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--non-goals", default="- 不改变未列入本次范围的功能。")
    parser.add_argument("--startup", default="待项目审查确认")
    parser.add_argument("--criteria", action="append", required=True)
    parser.add_argument("--scope", action="append", required=True)
    parser.add_argument("--owner", default="项目负责人")
    parser.add_argument("--updated", default="2026-10-19")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"项目目录不存在：{root}")
    path = root / "docs" / "goals" / "active.md"
    if path.exists():
        raise SystemExit(f"目标契约已存在，不覆盖：{path}")
    criteria = "\n".join(f"- [ ] {value}" for value in args.criteria)
    scope = "\n".join(f"- `{value}`" for value in args.scope)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(
        owner=args.owner,
        updated=args.updated,
        goal=args.goal.strip(),
        non_goals=args.non_goals.strip(),
        startup=args.startup.strip(),
        criteria=criteria,
        scope=scope,
    ), encoding="utf-8")
    print(path)


if __name__ == "__main__":
    main()
