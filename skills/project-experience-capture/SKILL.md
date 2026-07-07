---
name: project-experience-capture
description: Extract the current task, investigation, implementation, or project into a reusable resume project-experience material file. Use when the user asks to save project experience, create resume material, summarize work for a resume, preserve a task/project as a portfolio item, generate a project-experience library entry, or says the output file should be named after the project.
---

# Project Experience Capture

## Goal

Turn the current work into a durable project-experience material file that can later be shortened into resume bullets, interview talking points, or portfolio summaries.

## Workflow

1. Identify the project name.
   - Prefer an explicit name from the user.
   - Otherwise infer a concise project name from the main artifact, repo, report title, product, or task theme.
   - Use the project name as the output filename: `<项目名称>.md`.

2. Choose the output location.
   - If the user gives a path, write there.
   - Otherwise write in the current workspace root.
   - Produce exactly one project-experience material document per invocation.
   - Do not also create or update `resume.md`, an index, a summary file, or a duplicate project file unless the user explicitly asks for that exact file as the only output.
   - If the user explicitly names `resume.md` as the output target, write only `resume.md` and do not create a separate `<项目名称>.md`.
   - If a same-named file exists, update it carefully instead of creating duplicates. Preserve user-written material unless it clearly conflicts with the new verified facts.

3. Gather evidence before writing.
   - Inspect relevant local files, reports, diffs, notes, code, command outputs, and conversation context.
   - Prefer project artifacts over memory. Use memory only for continuity, and verify drift-prone facts from the workspace when practical.
   - If evidence is insufficient for a claim, write it as a question, assumption, or “待补充”, not as fact.

4. Write a material-rich source document, not a final one-page resume entry.
   - Include enough detail for later tailoring.
   - Keep claims evidence-bounded.
   - Separate “what was done”, “how it was verified”, “what can be claimed in a resume”, and “what to avoid overstating”.
   - Extract personal abilities and strengths from the project evidence, not from generic self-evaluation.

5. Save the file and verify it exists.
   - After writing, check the filename, headings, and key terms.
   - Report the saved path and the major sections included.

## Output File Structure

Use this structure by default. Omit sections only when they truly do not apply.

```markdown
# <项目名称>

## 项目定位

## 一句话介绍

## 个人角色

## 技术栈和工具

## 项目背景

## 核心工作内容

### 1. <关键工作模块>

### 2. <关键工作模块>

### 3. <关键工作模块>

## 关键结论或成果

## 可量化或可验证成果

## 个人能力与特长提炼

## 可写进简历的完整版本

## 精简版简历项目

## 面试一句话版本

## 面试追问准备

## 表述注意事项

## 可裁剪方向
```

## Writing Rules

- Write in Chinese unless the user asks otherwise.
- Prefer concrete verbs: “还原”, “定位”, “验证”, “区分”, “梳理”, “输出”, “修正”.
- Prefer evidence-aware phrases: “确认”, “当前代码证据支持”, “抓包样本显示”, “需结合后续样本验证”.
- Avoid inflated claims: “破解”, “证明作弊”, “保证收益”, “稳定保活”, “完全自动化”, “全量覆盖”.
- For sensitive or adversarial work, frame the experience as analysis, auditing, compliance, risk review, or mechanism reconstruction.
- Do not invent metrics. If useful metrics are absent, add a “可补充量化指标” subsection with suggestions.
- Keep a distinction between:
  - implemented work vs analyzed work,
  - code evidence vs network evidence,
  - confirmed conclusions vs reasonable inference,
  - resume-safe wording vs interview-only detail.
- When summarizing personal abilities, bind each ability to concrete project behavior or evidence. Avoid unsupported traits such as “责任心强” unless the project material shows repeated verification, iteration, ownership, or delivery pressure.

## Ability Extraction Guidance

Add a “个人能力与特长提炼” section to every project material file unless the user asks for project bullets only.

Use this format:

```markdown
## 个人能力与特长提炼

| 能力/特长 | 项目中的体现 | 简历可用表述 |
| --- | --- | --- |
| 复杂问题拆解能力 | <具体证据> | <可放入个人优势/自我评价的句子> |
```

Prefer abilities that can be defended in an interview:

- 复杂系统拆解能力：can map a large workflow into modules, dependencies, and edge cases.
- 证据化分析能力：can separate code evidence, runtime evidence, network evidence, and inference.
- 逆向与调试能力：can use static analysis, dynamic hooks, logs, packet captures, and cross-validation.
- 技术表达能力：can turn complex mechanisms into readable diagrams, reports, and plain-language explanations.
- 边界意识和风险意识：can avoid overclaiming, name unverified assumptions, and preserve evidence boundaries.
- 自驱推进能力：can continue through ambiguity, tool issues, incomplete samples, and multi-round revisions.
- 跨领域学习能力：can quickly understand unfamiliar domains such as advertising, Android lifecycle, sync services, billing, or privacy fields.
- 审校和质量意识：can detect contradictions, repair terminology drift, and keep final documents consistent.

Do not list more than 6-8 abilities for one project. Merge overlapping abilities and prioritize those most relevant to the target role.

## Resume Bullet Guidance

When generating resume-ready bullets inside the material file:

- Make bullets outcome-oriented but not exaggerated.
- Mention tools only when they strengthen the claim.
- Highlight hard parts: ambiguity, cross-source verification, edge cases, production-like constraints, scale, or stakeholder readability.
- Include a concise “面试追问准备” section so the user can defend the claims.

## Filename Rules

- Filename must be based on the project name: `<项目名称>.md`.
- Remove characters invalid for the local filesystem: `\ / : * ? " < > |`.
- Preserve Chinese project names when useful.
- If the inferred name is too long, use a concise title under 40 characters.

## Final Response

Keep the final response short:

- State the file path.
- List 3-6 major sections included.
- Mention any important assumptions or missing evidence.
