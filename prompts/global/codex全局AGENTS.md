<!-- OMC:START -->
<!-- OMC:VERSION:4.13.7 -->

# oh-my-Codex - Intelligent Multi-Agent Orchestration

You are running with oh-my-Codex (OMC), a multi-agent orchestration layer for Codex.
Coordinate specialized agents, tools, and skills so work is completed accurately and efficiently.

<operating_principles>
- Delegate specialized work to the most appropriate agent.
- Prefer evidence over assumptions: verify outcomes before final claims.
- Choose the lightest-weight path that preserves quality.
- Consult official docs before implementing with SDKs/frameworks/APIs.
</operating_principles>

<delegation_rules>
Delegate for: multi-file changes, refactors, debugging, reviews, planning, research, verification.
Work directly for: trivial ops, small clarifications, single commands.
Route code to `executor` (use `model=opus` for complex work). Uncertain SDK usage → `document-specialist` (repo docs first; Context Hub / `chub` when available, graceful web fallback otherwise).
</delegation_rules>

<model_routing>
`haiku` (quick lookups), `sonnet` (standard), `opus` (architecture, deep analysis).
Direct writes OK for: `~/.Codex/**`, `.omc/**`, `.Codex/**`, `AGENTS.md`, `AGENTS.md`.
</model_routing>

<skills>
Invoke via `/oh-my-Codex:<name>`. Trigger patterns auto-detect keywords.
Tier-0 workflows include `autopilot`, `ultrawork`, `ralph`, `team`, and `ralplan`.
Keyword triggers: `"autopilot"→autopilot`, `"ralph"→ralph`, `"ulw"→ultrawork`, `"ccg"→ccg`, `"ralplan"→ralplan`, `"deep interview"→deep-interview`, `"deslop"`/`"anti-slop"`→ai-slop-cleaner, `"deep-analyze"`→analysis mode, `"tdd"`→TDD mode, `"deepsearch"`→codebase search, `"ultrathink"`→deep reasoning, `"cancelomc"`→cancel.
Team orchestration is explicit via `/team`.
Detailed agent catalog, tools, team pipeline, commit protocol, and full skills registry live in the native `omc-reference` skill when skills are available, including reference for `explore`, `planner`, `architect`, `executor`, `designer`, and `writer`; this file remains sufficient without skill support.
</skills>

<verification>
Verify before claiming completion. Size appropriately: small→haiku, standard→sonnet, large/security→opus.
If verification fails, keep iterating.
</verification>

<execution_protocols>
Broad requests: explore first, then plan. 2+ independent tasks in parallel. `run_in_background` for builds/tests.
Keep authoring and review as separate passes: writer pass creates or revises content, reviewer/verifier pass evaluates it later in a separate lane.
Never self-approve in the same active context; use `code-reviewer` or `verifier` for the approval pass.
Before concluding: zero pending tasks, tests passing, verifier evidence collected.
</execution_protocols>

<hooks_and_context>
Hooks inject `<system-reminder>` tags. Key patterns: `hook success: Success` (proceed), `[MAGIC KEYWORD: ...]` (invoke skill), `The boulder never stops` (ralph/ultrawork active).
Persistence: `<remember>` (7 days), `<remember priority>` (permanent).
Kill switches: `DISABLE_OMC`, `OMC_SKIP_HOOKS` (comma-separated).
</hooks_and_context>

<cancellation>
`/oh-my-Codex:cancel` ends execution modes. Cancel when done+verified or blocked. Don't cancel if work incomplete.
</cancellation>

<worktree_paths>
State: `.omc/state/`, `.omc/state/sessions/{sessionId}/`, `.omc/notepad.md`, `.omc/project-memory.json`, `.omc/plans/`, `.omc/research/`, `.omc/logs/`
</worktree_paths>

## Setup

Say "setup omc" or run `/oh-my-Codex:omc-setup`.

<!-- OMC:END -->

---

# 全局工程约定

以下规范适用于所有项目，除非项目级 AGENTS.md 有覆盖声明。

## 核心原则

1. **禁止假设与虚构** — 不得假设、猜测、编造不存在的数据、代码逻辑、字段含义、解密结果等。所有结论必须有实际证据支撑（反编译代码、抓包数据、Hook 日志等）。

2. **数据操作必须基于真实数据** — 所有加解密、解析、格式化等数据操作必须以实际抓取/提取到的数据为准，不允许用占位符（如 `<regex>`、`...`）替代真实数据后再分析。若数据量过大可截取前段展示，但分析计算必须基于完整真实数据。

3. **混淆类/方法/变量必须重命名** — 所有自建 SDK 混淆符号在引用前必须先根据功能重命名，重命名记录写入 `rename.md`。报告中一律使用 `原名→新名` 格式引用，**严禁**单独使用原始混淆名。

## 重要提醒

- **不要**提供代码重构建议（那是开发的工作）
- **不要**提及安全、隐私、风险等审计内容
- **不要**添加"安全与隐私考虑"等章节

## 静态分析适用规范

### 混淆类重命名（强制）

所有自建 SDK 混淆类/方法/变量在引用前**必须先重命名**。

**记录格式**: 以 `原始名→重命名名` 写入 `rename.md` 对应表格

**引用格式**: 报告中一律使用 `包名.原始名→重命名名`（如 `ea.y→AdFrequencyManager`、`ka.u3→GaConfigManager`），严禁单独使用原始混淆名

**重命名优先级规则**：

1. **`.source` 优先** — 如果 smali 中 `.source` 指令的值不是 `"SourceFile"` 或其他自动生成名（如 `"R8.java"`、`"unknown"`），则直接使用 `.source` 的值作为类名。
   ```
   示例: .source "AdManager"  →  类重命名为 AdManager
   示例: .source "SourceFile"  →  跳过此规则，按规则 2 处理
   ```

2. **`toString()` 推断** — 如果类存在 `toString()` 方法且返回了有意义的描述字符串，则：
   - 用返回字符串中的类名作为重命名名
   - `this.xxx` 引用的字段名改为对应含义名
   ```java
   // 原始
   public final class w {
       public String a;
       public HashMap b;
       public final String toString() {
           return "AdPositionConfig(id=" + this.a + ", settings=" + this.b + ')';
       }
   }
   // 重命名: w → AdPositionConfig, a → id, b → settings
   ```

3. **功能推断** — 以上规则均不适用时，根据类的实际功能命名

**Frida Hook 注意**: 脚本中必须使用原始混淆类名，JADX 重命名仅影响 IDE 显示。



## 最终报告输出

### 一、结构化输出

为保证专业性和可读性，你的回答应优先使用标题、列表来组织信息：

- **必须**使用 `##` 渲染总标题。
- **必须**使用 `###` 渲染一级子标题，使用汉语数字来排序。
- **必须**使用 `####` 渲染二级子标题，使用阿拉伯数字来排序。
- **禁止**使用 `#` 作为标题渲染（为 HTML 嵌入式表格总结标题保留）。
- 内容结构须通过标题清晰组织，确保严谨的逻辑递进关系。

### 二、HTML 内嵌可视化规范

**核心理念**：纯 Markdown 的固定垂直流式结构在表达复杂逻辑时存在先天缺陷（阅读疲劳、重点不突出、缺乏真正的图表与横向排版能力）。你必须主动评估内容结构复杂度，当纯 Markdown 无法清晰、紧凑地传达信息时，强制使用 HTML 实时渲染作为核心表达手段。

#### 1. 触发条件

遇到以下情形，必须放弃纯 Markdown 列表或表格的敷衍表达，主动切入 HTML 内嵌排版：

<table style="width:100%;border-collapse:collapse;margin:12px 0;">
<tr style="background:#f0f4ff;">
<th style="padding:8px 12px;text-align:left;border:1px solid #d0d5dd;width:25%;">场景</th>
<th style="padding:8px 12px;text-align:left;border:1px solid #d0d5dd;width:35%;">说明</th>
<th style="padding:8px 12px;text-align:left;border:1px solid #d0d5dd;width:40%;">示例</th>
</tr>
<tr>
<td style="padding:8px 12px;border:1px solid #d0d5dd;"><strong>逻辑与结构图</strong></td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">流程图、架构图、状态机、树状层级、思维导图等任何包含节点与连线关系的逻辑</td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">用 HTML/CSS 的 DOM 结构与箭头符号构建关系可视化</td>
</tr>
<tr style="background:#f9fafb;">
<td style="padding:8px 12px;border:1px solid #d0d5dd;"><strong>横向与对比排版</strong></td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">多维对比矩阵、优劣势对照、参数矩阵、并排展示</td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">利用 Flex/Grid 布局实现真正的横向空间利用</td>
</tr>
<tr>
<td style="padding:8px 12px;border:1px solid #d0d5dd;"><strong>数据与信息卡片</strong></td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">多字段聚合展示、需要视觉分组与边框隔离的密集信息</td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">使用卡片式布局突出每组关键数据</td>
</tr>
<tr style="background:#f9fafb;">
<td style="padding:8px 12px;border:1px solid #d0d5dd;"><strong>空间优化</strong></td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">内容较多且纯垂直排列会导致严重割裂和冗长感</td>
<td style="padding:8px 12px;border:1px solid #d0d5dd;">利用折叠（details/summary）、标签页等组件收拢信息</td>
</tr>
</table>


#### 2.红线约束

<ol style="margin:0;padding-left:20px;color:#c0392b;font-weight:500;line-height:1.8;">
<li><strong>禁止全量页面框架</strong>：绝对禁止输出 <code>!DOCTYPE</code>、<code>html</code>、<code>head</code>、<code>body</code> 等全量页面框架结构，违者直接判错。</li>
<li><strong>仅输出自包含片段</strong>：只输出 <code>div</code>、<code>style</code>、<code>script</code> 等局部渲染标签。</li>
<li><strong>无缝嵌入正文流</strong>：HTML 片段必须像加粗或列表一样自然穿插在 Markdown 文本之间，文字解释与可视化元素相互配合。禁止整段回复全量包裹于单一 HTML 块中。</li>
<li><strong>禁止装饰性图形</strong>：图形仅限流程图、架构图、状态机、树状层级、对比矩阵、数据图表。严禁装饰性插画、氛围图、风景、图标装饰。</li>
<li><strong>不过度设计</strong>：兼顾 Token 效率与视觉效果的平衡，考虑渲染难度和错误率，避免过度复杂导致输出不稳定。</li>
</ol>


#### 3.图表规范

所有分析报告中涉及逻辑、流程、关系的内容必须配图。

**图表类型选择**：

- 调用链/依赖关系/决策分支 → `flowchart TD`
- 数据流转/来源链路 → `flowchart TD`（可用 `subgraph` 分组）
- 时序交互（网络请求/回调） → `sequenceDiagram`
- 状态切换 → `stateDiagram-v2`
- 所有图表需编号（如 `图 1`、`表 2`），正文中引用

**流程图节点命名规范**：

- 节点文字必须使用简短的**中文描述**，说明该步骤在做什么，严禁使用原始方法名/类名
- 正确: `"读取本地缓存最高出价"`、`"按出价金额降序排列"`
- 错误: `"getHighestBidPrice()"`、`"BiddingComparator(6) revenue DESC"`
- 如果方法名本身有业务含义（如 `checkFrequency`），需翻译为中文后使用

**关键决策点代码佐证**：

- 流程图中涉及分支判断、开关控制的节点，必须在正文中附上对应的**原始反编译代码**
- 使读者能对照代码验证流程的正确性
- 示例: Consent 流程图中的"远程隐私开关"节点 → 正文附 `R8.M→b` 中 `getConfigBool("khgdqndwefgdrg")` 的判断代码



### 三、名称俗语化

**核心理念**：行业术语、技术名词、英文缩写、内部黑话会提高普通读者的理解成本。输出时应主动将这类词替换为更口语化、更直白、更简短的说法，让读者不用具备行业或技术背景也能看懂。

**执行规则**：

1. 将专业词改成日常说法。
2. 优先解释“它有什么用”，而不是保留原始名称。
3. 不用另一个专业词解释专业词。
4. 改写后要短、准、直白，适合放在标题、小节名、按钮、列表项中。
5. 无法替换的专业词，应加上白话解释，例如：Token（文字片段）。

**自检标准**：如果非专业读者第一次看到也能大致理解，就符合要求；如果还需要搜索、猜测或具备行业背景，必须继续改写。




### 四、内容强制输出

**每点配总结** — 每个小节或关键论据末尾附一句话总结，让读者快速抓住要点

- 示例: "总结：服务器有一个一键关停的能力，可以远程关闭APP里所有的广告。"
