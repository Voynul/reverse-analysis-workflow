# Android Reverse Skill 合并说明

## 合并来源

本目录整合了以下三个版本：

| 来源目录 | 定位 | 处理方式 |
|---|---|---|
| `android-re-tools` | 早期工具链清单版 | 吸收工具速查、组合流程、Mobile/Reqable 注意事项 |
| `android-reverse` | 工具链增强版 | 吸收 MCP 失败处理、长版静态重命名规则、`.source` 和 `toString()` 规则 |
| `android-reverse2` | 可复用总控版 | 作为主骨架，保留证据优先、native、网络、命名记录和输出边界 |

## 最终取舍

1. 保留一个主 skill：`android-reverse`。
2. 使用 `android-reverse2` 的总控结构。
3. 合并旧版 `static-analysis.md` 中更细的重命名规则和工具速查。
4. 将旧版 `reqable.md` 合并为 `network-traffic.md`。
5. 将旧版 Mobile MCP 详细操作表合并进 `mobile-automation.md`。
6. 将 Frida Server 启动流程和 JSONL 日志规范合并进 `dynamic-hook.md`。
7. 保留 native 分析为独立参考文档。

## 废弃内容

- 不再保留 `referce` 这个拼写错误目录名。
- 不再同时维护 `reqable.md` 和 `network-traffic.md` 两套网络文档。
- 不再让主 `SKILL.md` 承载大段工具细节，细节统一放入 `reference/`。
- 不把普通分析报告、阶段报告、最终报告、报告审查规则写进本 skill；需要时叠加 `analysis-report`、`final-report` 或 `report-analysis-reviewer`。

## 建议替换方式

确认本目录内容可用后，可将旧版本归档：

```text
_archive/
  android-re-tools.old/
  android-reverse.old/
  android-reverse2.old/
```

再把本目录改名为：

```text
android-reverse/
```
