# 逆向分析工作流整理版

本目录是整理后的可取走版本。原始材料、旧 agent、旧提示词都已和正式产物分开。

## 一、工作流

1. Claude 负责 Android 逆向分析。
2. Claude 根据分析结果生成普通分析报告。
3. Codex 负责把多份普通分析报告合并成最终报告。
4. Codex 负责审查最终报告是否可交付。

对应关系：

| 阶段 | 工具 | 入口 |
|---|---|---|
| 逆向分析 | Claude | `agents/claude/android-reverse-agent.md` + `skills/android-reverse/` |
| 普通分析报告 | Claude | `agents/claude/analysis-report-agent.md` + `skills/analysis-report/` |
| 最终报告合并 | Codex | `agents/codex/final-report-agent.md` + `skills/final-report/` |
| 报告审查 | Codex | `agents/codex/report-analysis-reviewer-agent.md` + `skills/report-analysis-reviewer/` |

## 二、目录结构

```text
逆向skills整合-整理版/
  README.md
  skills/
    android-reverse/
    analysis-report/
    final-report/
    report-analysis-reviewer/
    project-record-tracker/
  agents/
    claude/
      android-reverse-agent.md
      analysis-report-agent.md
    codex/
      final-report-agent.md
      report-analysis-reviewer-agent.md
    opencode/
      report-analysis-reviewer.md
    archive/
      ...
  prompts/
    optimized/
      通用全局提示词.md
      逆向项目提示词.md
      提示词取舍说明.md
    project/
      项目规则.md.example
      AGENTS.md
      claude项目CLAUDE.md
    global/
      claude全局CLAUDE.md
      codex全局AGENTS.md
      opencode全局AGENTS.md
    archive/
      ida提示词.md
```

## 三、正式文件说明

### 1. Skills

| 路径 | 用途 | 是否安装 |
|---|---|---|
| `skills/android-reverse/` | Android 逆向分析能力 | 必装 |
| `skills/analysis-report/` | 普通分析报告，支持精简版、标准版、阶段版 | 必装 |
| `skills/final-report/` | 最终报告合并 | 必装 |
| `skills/report-analysis-reviewer/` | 报告审查 | 必装 |
| `skills/project-record-tracker/` | 项目记录、项目追溯、项目复盘、简历和面试素材 | 推荐安装 |

### 2. Agents

| 路径 | 用途 | 是否安装 |
|---|---|---|
| `agents/claude/android-reverse-agent.md` | Claude 分析入口 | Claude 需要 |
| `agents/claude/analysis-report-agent.md` | Claude 普通报告入口 | Claude 需要 |
| `agents/codex/final-report-agent.md` | Codex 最终报告合并入口 | Codex 需要 |
| `agents/codex/report-analysis-reviewer-agent.md` | Codex 报告审查入口 | Codex 需要 |
| `agents/opencode/report-analysis-reviewer.md` | opencode 报告审查入口 | 可选 |
| `agents/archive/` | 旧 agent 原文 | 不安装，仅回查 |

### 3. Prompts

| 路径 | 用途 | 是否使用 |
|---|---|---|
| `prompts/optimized/通用全局提示词.md` | 各工具通用全局规则 | 推荐作为全局提示词 |
| `prompts/optimized/逆向项目提示词.md` | Android 逆向项目级规则 | 推荐作为项目提示词 |
| `prompts/optimized/提示词取舍说明.md` | 为什么这样拆分 | 只读说明 |
| `prompts/project/项目规则.md.example` | 项目规则示例 | 只作示例，不安装 |
| `prompts/global/` | 旧平台全局提示词模板 | 历史参考 |
| `prompts/project/AGENTS.md` | 旧项目通用 AGENTS | 历史参考或兼容 |
| `prompts/project/claude项目CLAUDE.md` | 旧 Claude 项目提示词 | 历史参考 |
| `prompts/archive/` | 旧提示词素材 | 不安装，仅回查 |

## 四、安装到哪里

以下路径按常见默认约定写；如果你的工具使用了自定义目录，以你的实际目录为准。

### 0. 自动安装脚本

本目录提供自动安装脚本：

```text
install.py
```

脚本会检查用户目录下是否存在：

```text
~/.claude
~/.codex
~/.config/opencode
```

存在哪个工具目录，就安装对应的 skills、agents、prompts。不存在的工具目录会跳过，不会强行创建。

先预览：

```bash
python install.py --dry-run
```

确认无误后执行：

```bash
python install.py
```

覆盖已有文件前，脚本会先备份不同内容的旧文件，备份名类似：

```text
SKILL.md.bak-20260529-135457
```

### 1. 安装 Skills

把这些文件夹复制到 Claude / Codex 能读取 skill 的目录。

需要复制：

```text
skills/android-reverse/
skills/analysis-report/
skills/final-report/
skills/report-analysis-reviewer/
skills/project-record-tracker/
```

推荐目标：

```text
Claude Code:
~/.claude/skills/

Codex:
~/.codex/skills/
```

复制后示例：

```text
~/.claude/skills/android-reverse/SKILL.md
~/.claude/skills/analysis-report/SKILL.md
~/.claude/skills/final-report/SKILL.md
~/.claude/skills/report-analysis-reviewer/SKILL.md
~/.claude/skills/project-record-tracker/SKILL.md

~/.codex/skills/android-reverse/SKILL.md
~/.codex/skills/analysis-report/SKILL.md
~/.codex/skills/final-report/SKILL.md
~/.codex/skills/report-analysis-reviewer/SKILL.md
~/.codex/skills/project-record-tracker/SKILL.md
```

### 2. 安装 Claude agents

复制：

```text
agents/claude/android-reverse-agent.md
agents/claude/analysis-report-agent.md
```

推荐目标：

```text
Claude Code:
~/.claude/agents/
```

复制后示例：

```text
~/.claude/agents/android-reverse-agent.md
~/.claude/agents/analysis-report-agent.md
```

Claude 负责：

```text
android-reverse → analysis-report
```

### 3. 安装 Codex agents

复制：

```text
agents/codex/final-report-agent.md
agents/codex/report-analysis-reviewer-agent.md
```

推荐目标：

```text
Codex 项目目录:
.codex/agents/
```

复制后建议改名为 `.toml`：

```text
.codex/agents/final-report.toml
.codex/agents/report-analysis-reviewer.toml
```

Codex 负责：

```text
final-report → report-analysis-reviewer
```

### 4. 安装全局提示词

通用全局提示词：

```text
prompts/optimized/通用全局提示词.md
```

推荐用法：

- Codex 全局规则：放入你的全局 `AGENTS.md` 或等效全局配置。
- Claude 全局规则：放入你的全局 `CLAUDE.md` 或等效全局配置。
- opencode 全局规则：放入对应全局规则文件。

注意：

```text
prompts/global/
```

里面是旧平台模板，不是新的主入口。新工作优先使用：

```text
prompts/optimized/通用全局提示词.md
```

### 5. 安装项目提示词

Android 逆向项目通用提示词：

```text
prompts/optimized/逆向项目提示词.md
```

推荐目标：

```text
项目根目录/AGENTS.md
项目根目录/CLAUDE.md
```

如果同一个项目同时给 Codex 和 Claude 使用：

- Codex 项目根目录放 `AGENTS.md`
- Claude 项目根目录放 `CLAUDE.md`

可以把 `逆向项目提示词.md` 的内容复制进去。

### 6. 项目规则.md

具体项目规则由用户自己提供，不随安装脚本安装。

如果某个项目需要限定分析范围、排除范围、报告模板或证据文件，请在项目根目录放：

```text
项目根目录/项目规则.md
```

所有正式 agents、prompts、skills 都按同一约定处理：

```text
存在 项目规则.md → 先读取并应用项目约束
不存在 项目规则.md → 跳过项目约束，按用户问题和证据自然探索
```

本整理包提供一个示例：

```text
prompts/project/项目规则.md.example
```

需要时可以参考它自己创建项目内的 `项目规则.md`，但不要把示例文件安装到全局工具目录。

## 五、不要安装什么

以下内容只保留用于回查，不建议安装到正式工作目录：

```text
agents/archive/
prompts/archive/
prompts/global/
prompts/project/项目规则.md.example
prompts/project/claude项目CLAUDE.md
```

原因：

1. 这些是旧版或平台模板。
2. 里面可能包含旧的 `stage-report` 表述。
3. 正式规则已经沉淀到 `skills/` 和 `prompts/optimized/`。

## 六、日常使用方式

### 小型分析

```text
Claude 使用 android-reverse 分析目标，再用 analysis-report 精简版输出普通分析报告。
```

### 专题分析

```text
Claude 使用 android-reverse 分析专题，再用 analysis-report 标准版输出普通分析报告。
```

### 大型分析

```text
Claude 分阶段产出多份 analysis-report 阶段版。
Codex 使用 final-report 汇总。
Codex 使用 report-analysis-reviewer 审查。
```

### 有项目规则的项目

```text
在项目根目录提供 项目规则.md。
Claude 分析前读取 项目规则.md。
Codex 合并和审查前读取 项目规则.md。
```

### 项目记录和经历追溯

```text
使用 project-record-tracker 读取会话上下文、项目文档、报告、数据、工作目录文件和可用元数据。
输出 <项目名称>-项目记录.md。
用于追溯项目开始时间、完成时间、主要工作内容、关键产物、当前状态、简历项目经历素材和面试追问准备。
```

## 七、维护原则

1. 规则正文只维护在 `skills/`。
2. agent 只做平台入口、模型和工具权限配置。
3. 通用全局提示词只放跨项目规则。
4. 项目提示词只放项目路由和硬边界。
5. 具体项目包名、重点范围、排除范围放项目规则。
6. `stage-report` 已退役；需要阶段报告时使用 `analysis-report` 阶段版。
