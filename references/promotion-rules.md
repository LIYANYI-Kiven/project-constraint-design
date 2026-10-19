# 约束提升标准

一条候选约束必须同时满足下面四项，才写入 `docs/rules/<id>.md`：

- 以后的会话仍然有效。
- 违反后会造成目录失控、启动入口冲突，或改变项目行为。
- 可以写成一句可执行的话。
- 不是某一次调试输出、临时报错或已经完成的任务细节。

规则文件使用这个格式：

```markdown
---
id: directory-boundary
title: 目录边界
status: active
source_logs:
  - 2026-10-19-initial-design.md
---

顶层目录只允许 src、docs 和启动脚本。禁止在项目内新建 backup、old、tmp 或试验副本。
```

同一编号只保留一个文件。再次确认时更新正文，并把新日志追加到 `source_logs`。规则失效时保留文件，把 `status` 改为 `retired`。
