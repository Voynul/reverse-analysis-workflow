---
name: android-reverse
description: 对 Android 安装包、DEX、smali、so/JNI 及运行中目标进行逆向分析，包括反编译、混淆理解、动态 Hook、抓包、协议和算法还原，以及用户明确要求的 APK 修改、重建、签名和验收。不用于普通 Android 源码开发、源码审查、重构迁移、Gradle 修复或多个 demo 的源码整合；开发任务确需逆向取证时，仅用于该子任务。
---

# Android Reverse

使用本技能对 Android 安装包、反编译产物及运行中应用开展逆向分析，还原行为、逻辑、功能实现、网络协议、运行时参数、返回值、加解密和 native 层逻辑。

## 适用范围与触发边界

按任务目的判断是否使用本技能。项目名称、目录历史，以及 Android、Java/Kotlin、保活、FCM、Manifest 或运行时等词，均不能单独作为触发依据。

- 适用：从安装包、反编译产物、原应用运行现象或协议数据还原实现、条件和调用链。阅读反编译得到的 Java/Kotlin 仍属于逆向分析，无须每次重新反编译或进行 Hook。
- 不适用：基于已有可编辑源码的常规开发、源码审查、重构、迁移、构建修复和 demo 源码整合。任务附带编译、安装、普通运行调试或参考历史逆向报告，也不足以触发本技能。
- 混合任务：开发过程中确需对安装包、反编译产物或运行中目标进行逆向取证时，仅对该子任务使用本技能；开发部分按用户要求和项目开发规则执行。

## 职责边界

本技能负责分析方式、工具使用、目标身份确认、证据判断和内部工作状态。默认执行只读分析并直接在对话中回答；只有用户明确要求修改 APK 时才进入修改与验收模式。

本技能不强制生成 `rename.md`、`Question.md`、证据索引、普通报告、阶段报告或最终报告。需要正式报告时叠加 `analysis-report` 或 `final-report`；用户临时要求生成脚本、算法说明、调用链文档或其他文件时照常执行。

仅分析用户拥有、获准测试或明确用于研究、教学、竞赛的目标。修改模式不得覆盖原始 APK，必须保留目标身份、修改范围和验证结果。

## 核心原则

1. 证据优先：结论必须来自反编译代码、smali、抓包数据、Hook 日志、配置文件、解密结果、UI 操作记录或 native 分析证据。
2. 不猜测：证据不足时标为推断或待确认，不得写成确定结论。
3. 真实数据：加解密、字段解析和请求还原使用真实样本，不用占位数据冒充证据。
4. 用户介入优先：用户对目标、工具、命名、产物和路径的明确要求高于技能默认策略；证据真实性与安全边界不因用户偏好而降低。
5. 目标隔离：默认聚焦一个已确认目标；版本对比、split 集合或关联载荷分析可以处理多个文件，但必须分别确认身份并隔离证据。
6. 工具联动：静态定位、动态验证、网络确认、手机操作和 native 分析按需要组合使用。
7. 最小修改：修改模式只改变完成目标所需的最小范围，不把重构、去混淆或无关修复混入同一产物。
8. 可验证完成：分析完成、构建成功、安装成功和运行结果是不同状态，不得互相替代。

## 执行自由度

本技能提供默认策略、证据要求和安全不变量，不穷举可用工具、分析方法或执行顺序。

除授权边界、证据真实性、原始产物保护和用户明确要求外，Agent 可以根据目标结构、当前环境、工具能力和新证据，自主调整工具、顺序、组合方式和中间产物。发现更直接或更可靠的方法时，无需继续默认路线，但应说明影响结论的关键选择和验证方式。

参考文档中的工具名、操作名、步骤和模板用于能力提示，不构成封闭清单。工具实际接口、目标特征或证据与默认建议不一致时，以真实环境和可验证结果为准。

## 启动协议

先核对上述适用范围；仅对适用的任务或子任务执行以下最小启动检查：

1. 定位项目根目录；存在 `项目规则.md` 时先读取。
2. 如果 `.android-reverse/analysis-state.md` 存在且与当前目标匹配，读取并恢复状态；简单任务不为此自动创建状态文件。
3. 确定任务模式：默认 `analysis`；需要 Hook、设备操作或抓包时增加 `runtime-validation`；用户明确要求修改 APK 时使用 `patch-and-verify`。
4. 从用户请求确定交付物。未要求正式报告时默认直接回答，不为报告策略单独打断简单任务。
5. 确认目标文件的绝对路径和可取得的身份信息；修改模式还需记录文件大小和 SHA-256。
6. 只检查当前任务实际需要的能力；需要分阶段验证时参照 `reference/workflow-gates.md`，不把关卡当作所有任务的前置清单。

工作状态和中间产物规则见 `reference/workspace-state.md`；APK 层级归属见 `reference/package-recon.md`。

## 技能路由：选择经验专题

这里的技能路由是本技能内部的经验路由，不要求拆成多个独立 Skill。根据问题选择专题，可组合、跳过或返回；专题不与某个工具绑定。完整清单见 [经验索引](reference/experience-index.md)。

| 问题 | 按需读取 |
|---|---|
| 目标身份、逻辑归属、Java/Kotlin、混淆名称 | [结构侦察](reference/package-recon.md)、[静态分析](reference/static-analysis.md)、[Kotlin 名称](reference/topics/kotlin-names.md) |
| 加固、抽取壳、Java2C、自定义加载器 | [脱壳与载荷](reference/topics/unpacking.md)、[加载器](reference/topics/native-loader.md) |
| JS、AST、WebView、JSVMP | [JS AST](reference/topics/js-ast.md)、[JSVMP](reference/topics/jsvmp.md)、[系统交互](reference/topics/system-ipc.md) |
| React Native、Flutter/Dart、Unity/Mono/IL2CPP | [React Native](reference/react-native-hermes.md)、[Flutter/Dart](reference/flutter-dart.md)、[Unity/IL2CPP](reference/unity-il2cpp.md) |
| JNI、native、VMP、反分析、指令轨迹 | [native](reference/native-analysis.md)、[VM](reference/vm-protection.md)、[反分析](reference/topics/anti-analysis.md)、[轨迹](reference/topics/native-tracing.md) |
| 网络、算法、长连接、原函数调用 | [网络](reference/network-traffic.md)、[协议](reference/topics/protocols.md)、[算法](reference/algorithm-validation.md)、[RPC/模拟执行](reference/topics/rpc-emulation.md) |
| 广告、远程配置、账户限制、更新与本地数据 | [业务专题索引](reference/experience-index.md#业务与数据) |
| 修改、重建、split、第三方包与模块交付 | [修改验收](reference/patch-and-verify.md)、[DEX 修改](reference/topics/dex-patching.md)、[交付专题索引](reference/experience-index.md#修改与交付) |
| 设备、硬件/内核观测及少见运行时 | [高级专题索引](reference/experience-index.md#设备与高级观测) |
| 故障、反例、证据与历史经验 | [故障目录](reference/topics/failure-catalog.md)、[案例](reference/topics/cases.md)、[证据](reference/evidence-and-renaming.md) |

## 工具路由：选择实现并读取操作文档

只有需要实际操作时才选择工具并读取相应操作文档。当前环境的工具 schema、版本和能力优先；下表不是能力上限，也不要求安装表中工具。

| 已选择的实现 | 操作文档 |
|---|---|
| `jadx-headless`、JEB 或等价无头 DEX 分析服务 | [静态工具](reference/tools/jadx.md) |
| `idalib-mcp` 或等价无头 native 分析服务 | [native 工具](reference/tools/idalib.md) |
| Frida MCP、CLI 或原函数 RPC | [Frida](reference/tools/frida.md) |
| Reqable 或其他抓包实现 | [网络工具](reference/tools/network.md) |
| mobile-mcp、ADB 或设备侧接口 | [设备操作](reference/tools/device.md) |
| Apktool、归档工具、对齐与签名器 | [APK 构建签名](reference/tools/apk.md) |
| 离线脚本、DEX 索引/SQL、JS 解析器 | [离线工具](reference/tools/offline.md) |
| Dart/Unity 解析器、模拟执行与调试/跟踪工具 | [专项工具](reference/tools/specialists.md) |

不在技能加载时启动或检查全部工具。当前任务首次使用某项能力时轻量验证，之后复用；连接、配置、设备或宿主变化后才重新检查。缺少工具时可选择等价无头实现，只暂停确实受影响的分支。发现和缓存细则见 [工具能力](reference/tool-capabilities.md)。

Java/native 默认采用无头方式，不静默探测或接管 GUI。工具失败、未命中或不完整输出只能说明当前证据边界，不能证明目标逻辑不存在。

## 默认分析路线

按任务需要选择步骤，不要求全部执行，也不要求固定顺序。

1. 明确任务模式、交付物和目标身份。
2. 判断关键逻辑归属：DEX、资源、native、React Native/Hermes、Flutter、Unity、WebView 或服务端。
3. 静态定位入口并追踪上下游链路，标出关键分支、配置、缓存、网络和回调。
4. 根据需要理解混淆、建立语义名称或保存证据位置。
5. 证据不足时使用 Hook、设备操作、抓包或 native 分析补证。
6. 修改模式先建立对照基线，再实施最小修改、重建、安装和运行验收。
7. 输出结论，区分直接观察、推断、假设、已否定内容和待确认项；只有用户要求时才生成额外文档。

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
- 未要求正式报告时默认对话交付，不自动调用报告技能或创建状态文件；这不禁止生成用户即时要求的其他文档或必要的内部中间物。
- 普通、专题或阶段报告叠加 `analysis-report`；多份材料的最终汇总叠加 `final-report`。
- `.android-reverse/` 仅是本技能的默认内部中间物目录。用户指定路径、外部项目 plan、`项目规则.md`、上层调用技能和报告技能的文件规划优先级更高。
- 不迁移、复制或重定向外部已规划的文件；内部状态只记录其引用路径。
- 修改模式的产物必须写入新文件或独立输出目录，不覆盖用户提供的原始 APK、so 或证据。
