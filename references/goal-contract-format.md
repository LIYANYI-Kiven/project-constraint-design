# 目标契约格式

`docs/goals/active.md` 使用以下结构。目标契约不是论文结论，也不是模型记忆；它只规定本项目要交付什么、如何验收和允许修改什么。

```markdown
---
title: 项目目标契约
status: active
owner: 项目负责人
updated: 2026-10-19
---

# Goal

用一句话说明最终可交付结果。

## Non-goals

- 不做什么。

## Runtime boundary

- 唯一启动入口：
- 必须保留的代码、配置、数据、模型或外部资源：
- 明确禁止触碰的路径：

## Success criteria

- [ ] 功能标准：
- [ ] 数据/文件完整性标准：
- [ ] 回归测试标准：
- [ ] 安全与可恢复标准：

## Allowed scope

本轮允许修改的路径：

## Evidence

验收命令、输出文件和人工检查位置：

## Recovery

失败时的回滚方式：
```
