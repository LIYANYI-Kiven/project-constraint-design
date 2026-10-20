---
name: project-constraint-design
description: 在编写功能代码前以目标、成功标准、边界和证据设计项目约束，建立 docs/development-log 记忆索引和 docs/rules 长期约束。适用于新项目开工、AI 开发约束、写开发日志和提升规则。不要用于移走已经堆积的无用文件。
metadata:
  short-description: 开工前建立日志记忆和规则
---

# 项目约束设计

在写功能代码之前，把项目的目标、非目标、成功标准、目录边界、唯一入口、验收证据和长期约束固定下来。方法借鉴 Goal-Driven，但只保存可执行的项目契约，不把无限循环提示词或聊天全文写进项目。后续 agent 通过索引找回记忆，不靠翻完整聊天记录。

## 设计来源与边界

本 Skill 对“目标、成功标准、主控独立验收、证据复核与恢复”的工程治理设计，参考并改编自 Goal-Driven 项目；引用和改编边界见 [references/goal-driven-attribution.md](references/goal-driven-attribution.md)。它不是 Goal-Driven 的官方实现或关联项目，也不采用其无限重启 agent 的提示词；项目决策和范围仍由用户控制。

文件已经失控时使用 `runtime-safe-cleanup`。本技能不移动旧文件，也不代替用户做产品决策。

## 必要输入

路径或目标缺失时先询问，不要自行新建到临时位置。

- 项目目录：准备开工或继续约束的项目根目录。
- 项目目标：一两段话，说明要做成什么、明确不做什么。
- 成功标准：可运行、可测试、可复核的验收条件；不能只写“效果更好”。
- 任务范围：本次允许修改的文件或目录；范围外不修改。

缺少项目目标或成功标准时先停止，不用临时目标代替用户决策。

## 1. 建立记忆结构

运行 [scripts/init_docs.py](scripts/init_docs.py)。它只创建缺少的目录和索引，不覆盖已有日志或规则。再用 [scripts/create_goal_contract.py](scripts/create_goal_contract.py) 创建 `docs/goals/active.md`；它不会覆盖已有目标契约。

必须存在：

- `docs/development-log/`：开发日志和项目记忆。
- `docs/development-log/index.md`：日志索引，是后续 agent 的记忆入口。
- `docs/rules/`：从日志提升出来的长期约束。
- `docs/rules/index.md`：规则索引，是后续 agent 的约束入口。
- `docs/goals/active.md`：当前目标契约，包含目标、非目标、成功标准、风险边界和验收证据。

目标契约至少写出：Goal、Non-goals、Criteria、Scope、Evidence 和 Recovery。每条成功标准都要能由测试、文件证据或人工复核判定通过/失败。

## 2. 先写设计，再写代码

第一份日志记录目标、非目标、成功标准、顶层目录、唯一启动入口、运行依赖、验收命令，以及一次任务允许修改的范围。日志格式见 [references/log-format.md](references/log-format.md)。

第一份日志至少提升四条规则：

- `directory-boundary`：允许的顶层目录；禁止随手新建备份、试验副本、缓存目录。
- `startup-entry`：唯一启动命令和脚本位置。说明文档只记录命令，不另存一份启动脚本。
- `change-scope`：没有写入当前任务范围的路径不修改。
- `memory-entry`：以后每次开工先读两个索引，再读相关日志和规则。

规则的提升标准见 [references/promotion-rules.md](references/promotion-rules.md)。

## 3. 每次记日志都复核规则和目标

完成一次设计或实施后追加一份日志，不改写旧日志。逐条检查目标契约和成功标准：满足提升标准就新建或更新 `docs/rules/<id>.md`；不满足就留在日志中。已有规则被替代时把 `status` 改为 `retired`，不要删除历史。没有证据的“完成”不得写入 accepted。

然后运行 [scripts/rebuild_indexes.py](scripts/rebuild_indexes.py)，重新生成两个索引。不要手工维护索引表格。

## 4. 后续会话的顺序

1. 读 `docs/rules/index.md`，遵守 `active` 规则。
2. 读 `docs/development-log/index.md`，只打开和当前任务相关的日志。
3. 在规则允许的路径内工作。
4. 追加日志、提升新的约束，并重建索引。

## 5. Goal-Driven 主控原则

主控 agent 负责判断标准是否满足，而不是接受子任务的自报结果。每次循环只做一组范围明确的改变；完成后收集文件差异、测试输出和运行状态，再决定继续、回滚或结束。达到全部成功标准并通过一次独立复核后才标记 accepted；遇到同一阻塞条件时记录证据并请求人工决策，不无限重复相同失败。
