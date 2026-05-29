# Agent 使用说明

## 实际工作流

1. Claude 执行分析任务：使用 `agents/claude/android-reverse-agent.md`。
2. Claude 生成普通分析报告：使用 `agents/claude/analysis-report-agent.md`。
3. Codex 合并最终报告：使用 `agents/codex/final-report-agent.md`。
4. Codex 审查报告：使用 `agents/codex/report-analysis-reviewer-agent.md`。

## 维护原则

- agent 只做平台入口和工具权限配置。
- 规则正文放在 `skills/` 中。
- 修改工作规则时优先改 skill，再同步薄壳 agent 的一句话边界。
- 旧 agent 放入 `agents/archive/`，不要继续作为主入口。
