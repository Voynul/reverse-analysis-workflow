---
name: android-reverse
description: 使用 JADX/JEB、Frida、mobile-mcp、Reqable 和 IDA 对 Android APK、Java/Kotlin、smali、运行时行为、网络协议及 native so/JNI 进行证据驱动的逆向分析。用于 APK 分析、反编译、动态 Hook、抓包、算法还原、混淆理解、JNI/native 分析和自动化触发；负责目标确认、工具路由、分析方法与中间状态，不负责强制生成正式报告。
---

# Android Reverse

使用本技能分析 Android APK 的行为、逻辑、功能实现、网络协议、运行时参数、返回值、加解密和 native 层逻辑。

## 职责边界

本技能负责分析方式、工具使用、目标身份确认、证据判断和内部工作状态。默认直接在对话中回答当前问题。

本技能不强制生成 `rename.md`、`Question.md`、证据索引、普通报告、阶段报告或最终报告。需要正式报告时叠加 `analysis-report` 或 `final-report`；用户临时要求生成脚本、算法说明、调用链文档或其他文件时照常执行，不受“无需正式报告”限制。

## 核心原则

1. 证据优先：结论必须来自反编译代码、smali、抓包数据、Hook 日志、配置文件、解密结果、UI 操作记录或 native 分析证据。
2. 不猜测：证据不足时标为推断或待确认，不得写成确定结论。
3. 真实数据：加解密、字段解析和请求还原使用真实样本，不用占位数据冒充证据。
4. 用户介入优先：用户对目标、工具、命名、产物和路径的明确要求高于技能默认策略；证据真实性与安全边界不因用户偏好而降低。
5. 单目标分析：一次分析任务只处理一个 APK；同一会话可以在前一 APK 完成后由用户主动切换到另一个 APK，但不并行混合取证。
6. 工具联动：静态定位、动态验证、网络确认、手机操作和 native 分析按需要组合使用。

## 启动协议

使用本技能前按顺序执行：

1. 定位项目根目录；存在 `项目规则.md` 时先读取。
2. 读取 `.android-reverse/analysis-state.md`；如果是已确认目标的延续任务，恢复其状态。
3. 确认当前 APK 是否需要正式报告。用户话术已经明确时直接记录，不重复询问；未明确时先询问。
4. 确认当前目标 APK 的绝对路径、包名、`versionName` 和 `versionCode`。
5. 确认或恢复该目标的工具模式，再开始实际分析。

正式报告策略按单个 APK 分析任务记录。用户切换 APK 后重新确认；用户也可以声明项目级默认值或随时覆盖已有选择。

工作状态和中间产物规则见 `reference/workspace-state.md`。

## 工具路由

| 场景 | 首选工具 | 补充工具 | 参考文档 |
|---|---|---|---|
| Java/Kotlin 逻辑、Manifest、调用链 | JADX GUI MCP（`jadx_mcp`），不可用则无头 JADX（`jadx_headless`） | JEB MCP、smali | `reference/static-analysis.md` |
| 参数、返回值、明文、分支、运行时调用栈 | Frida MCP | Frida CLI | `reference/dynamic-hook.md` |
| 启动、点击、滑动、截图、触发流程 | mobile-mcp | ADB | `reference/mobile-automation.md` |
| HTTP/HTTPS、WebSocket、HAR、接口字段 | reqable MCP | Hook 日志、解密结果 | `reference/network-traffic.md` |
| so、JNI、native 加解密、签名、校验 | 无头 IDA（`idalib-mcp`），不可用再 GUI `ida` | Frida Native Hook | `reference/native-analysis.md` |
| 证据判断、混淆理解、语义命名 | 对话与内部分析材料 | 按需生成命名或证据文件 | `reference/evidence-and-renaming.md` |

本机 Frida CLI 已隔离在 Conda 的 `android` 环境。回退 CLI 时必须使用 `scripts/run-frida.ps1`，不得依赖全局 PATH 中存在 `frida`；具体调用规则见 `reference/dynamic-hook.md`。

### JADX 选择

Java/Kotlin 静态分析一次只使用一个 JADX 模式，详细决策见 `reference/static-analysis.md`。

1. 用户明确指定 GUI 或无头时，以用户指定为准。
2. `jadx_mcp` 无法连接且用户已提供 APK 绝对路径时，使用 `jadx_headless`。
3. GUI 已连接但未加载 APK 时，提醒用户加载或明确选择无头，不自动回退。
4. GUI 已加载 APK 时，先输出路径（可取得时）、包名和版本信息，等待用户确认后再分析。
5. 已确认的工具选择绑定当前 APK；工具中断后不得静默切换。
6. 无头模式只加载用户明确选择的绝对路径；服务生命周期按项目任务阶段管理。

### IDA 选择

so / JNI / native 分析优先无头，详细规则见 `reference/native-analysis.md`。

1. 优先使用 `idalib-mcp`；不可用时才考虑 GUI `ida`。
2. IDA session 不强制绑定 APK，APK 切换不自动关闭 session 或切换目标 so。
3. Agent 只自动关闭自己为某个分析分支创建、且关闭策略明确的 session。
4. 用户或外部打开的 GUI、database/session 由用户管理。
5. 回退 GUI 时先输出当前二进制身份信息并等待用户确认，不因 GUI 已打开就直接分析。

如果任务需要某个 MCP 工具，但工具未启用、命名空间不存在、连接失败或服务未启动，应先按 JADX / IDA 回退规则处理；其他工具仍应暂停该分支，提示用户开启对应服务并附上失败原因。不得把 MCP 工具不可用当作目标 APK 没有对应逻辑的证据。

## 标准流程

1. 明确问题：确认要分析行为、接口、参数、返回值、算法、UI 触发、网络协议、so 逻辑还是完整链路。
2. 静态定位：优先在项目约束和用户指定范围内查找入口；证据不足时再扩展到 Manifest、组件、类名、字符串、URL、日志和导出函数。
3. 追踪链路：向上找触发入口，向下找执行结果，标出关键分支、配置、缓存、网络和回调。
4. 理解混淆：根据分析需要决定是否进行工具内重命名或落盘记录；用户要求可读命名时优先执行。
5. 动态验证：按需 Hook 参数、返回值、异常、解密函数和 Java/native 边界。
6. 触发行为：需要运行态操作时说明动作及影响，再用 mobile-mcp 或 ADB 执行。
7. 网络确认：用 Reqable、Hook 日志或解密结果获取真实请求、响应、字段和时序。
8. Native 分析：需要时使用 IDA 建立 Java/JNI/native 映射，并按 session 所有权管理资源。
9. 输出结论：直接回答当前问题，列明证据、已确认内容、推断和待确认项；只有用户要求时才生成额外文档。

## 项目约束接口

项目根目录可以提供 `项目规则.md` 作为项目约束输入。存在则必须使用，不存在则跳过，不得自行编造。

| 约束项 | 用途 |
|---|---|
| 分析对象 | APK 包名、版本、样本路径或目标模块 |
| 优先范围 | 优先分析的包名、混淆包、类、组件、接口、功能主题 |
| 排除范围 | 只做边界确认、不深入分析的公开 SDK、三方库或无关模块 |
| 重点问题 | 本项目最关注的行为、链路、字段、配置、广告位或 native 逻辑 |
| 证据文件 | 已有普通分析报告、阶段报告、抓包、Hook 日志、解密结果、配置文件 |
| 命名记录 | `rename.md` 或其他混淆命名表 |
| 输出要求 | 是否需要生成普通分析报告、阶段版报告、Question.md 或证据索引 |

使用规则：

1. 项目约束用于收窄分析范围，不用于替代证据。
2. 边界外内容只在解释调用关系或排除误解时检查。
3. 如果项目约束与真实代码或数据冲突，应说明冲突并以原始证据为准。
4. 如果项目约束证据不足，应标为待确认或进入补证方向。

## 产出与文件边界

- 默认只给出对话结论，不自动创建正式报告。
- 用户选择“不需要正式报告”时，在 `analysis-state.md` 记录，并且不自动调用报告技能；这不禁止生成用户即时要求的其他文档或必要的内部中间物。
- 普通、专题或阶段报告叠加 `analysis-report`；多份材料的最终汇总叠加 `final-report`。
- `.android-reverse/` 仅是本技能的默认内部中间物目录。用户指定路径、外部项目 plan、`项目规则.md`、上层调用技能和报告技能的文件规划优先级更高。
- 不迁移、复制或重定向外部已规划的文件；内部状态只记录其引用路径。
