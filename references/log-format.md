# 开发日志格式

每份日志是 `docs/development-log/` 下的一个 Markdown 文件，文件名以日期开头。`index.md` 由脚本生成，不要手工编辑。

```markdown
---
date: 2026-10-19
title: 确定项目边界
type: decision
status: accepted
promoted_rules:
  - directory-boundary
---

## 记忆

用短句记录以后还需要知道的决定、原因和被拒绝的方案。

## 候选约束

- id: directory-boundary
  promote: true
  statement: 顶层只允许保留 src、docs 和启动脚本。
  reason: 随意新建目录会让后续 agent 找不到入口。
```

`type` 使用 `decision`、`implementation` 或 `memory`。`status` 使用 `accepted` 或 `superseded`。`promoted_rules` 只列出本次实际写入 `docs/rules/` 的规则编号。
