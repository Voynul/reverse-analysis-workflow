# android-reverse

面向 Android 安装包、反编译产物及运行中应用的 Agent Skill，提供逆向分析经验、按需工具操作说明和可选离线辅助脚本。

它帮助 Agent 定位业务实现、建立证据链、选择分析方法，以及完成用户明确要求的 APK 修改与验收。技能保留 Agent 根据目标、环境和新证据调整路线的空间，不要求按固定工具或阶段顺序完成所有任务。

本项目为自用技能，沿用通用 Agent Skills 的 `SKILL.md` 入口，不绑定某一家 Agent 宿主。本文供使用者了解项目；Agent 的执行入口是 [SKILL.md](SKILL.md)，专项材料按需加载。

[项目功能](#项目功能) · [参考项目与来源](#参考项目与来源) · [两类路由](#两类路由) · [目录结构](#目录结构) · [文档清单](#文档清单) · [脚本清单](#脚本清单) · [使用与环境](#使用与环境) · [维护与验证](#维护与验证) · [已知边界](#已知边界)

## 项目功能

| 方向 | 覆盖内容 |
|---|---|
| 安装包与静态分析 | APK/DEX 身份、Manifest、组件、SDK、调用链、smali、混淆理解和 Kotlin 候选名称恢复 |
| 动态取证 | Java/native 参数、返回值、调用栈、加载时机、运行路径、消息链路与观测条件 |
| 保护与反分析 | 壳、抽取恢复、Java2C/JNI 下沉、自定义加载器、完整性响应、主动终止和反分析诊断 |
| JS 与跨平台运行时 | JS AST、JSVMP、React Native/Hermes、Flutter/Dart、Unity/Mono/IL2CPP、受保护 metadata |
| native 与虚拟化 | JNI 绑定、ELF 映射与重定位、SO dump、DBI、轨迹差分、解释器状态、VMP 与局部语义恢复 |
| 协议与算法 | HTTP、Protobuf/schema、gRPC、QUIC、WebSocket 状态链、TLS、请求签名、加解密和证书派生输入 |
| 业务与运行数据 | 广告、远程 UI 配置、更新、账户与限制归属、SharedPreferences、DataStore、MMKV、SQLite 和缓存回写 |
| 修改与交付 | DEX/smali 修改、补丁审计、归档保留、对齐、签名、split 集合、第三方包审计及模块式交付 |
| 平台与高级观测 | Binder、Intent、WebView bridge、SELinux、设备证明边界、远程调试、硬件观察与内核路线判断 |
| 证据与复用 | 声明状态、可选工作记录、50 类故障索引、案例与反例、来源追溯和离线回归 |

上述是经验覆盖范围。某个专题有文档，不代表已附带完整工具、已在当前设备跑通，或能保证恢复任意目标。

默认只做分析并在对话中交付；只有用户明确要求修改 APK 时进入修改模式。普通 Android 源码开发、重构、Gradle 修复或 demo 整合，不因出现 Android 技术词就触发本技能。开发任务需要逆向取证时，仅对对应子任务使用。

## 参考项目与来源

### 直接移植与方法参考

| 项目 | 采用方式 | 在本项目中的内容 |
|---|---|---|
| [apk-reverse：Codeberg 上游](https://codeberg.org/reverse-skill-lab/apk-reverse)；实际使用的 [apk-reverse-codeberg-mirror 镜像](https://git.42x.shop/tl0/apk-reverse-codeberg-mirror) | 从本地下载快照整合经验，并选择性迁入代码 | 覆盖侦察、保护、JSVMP、反分析、运行时、协议、修改、设备与案例等内容；67 份参考文档、65 个源码条目均有处置记录，其中 15 个 Python 脚本迁为离线辅助工具 |
| [newliver666/apk-reverse](https://github.com/newliver666/apk-reverse) | 历史来源标识 | 下载项目的说明保留此 GitHub 地址；与本次 Codeberg 镜像来源合并理解，不另计一次代码移植 |
| [owen800q/mobile-reverse-skill](https://github.com/owen800q/mobile-reverse-skill) | 方法参考；审阅提交 `d905f7d2d46bd4fa0d1bac7041ef9497d4463cad` | React Native/Hermes 定位、请求签名的字节级验证、JNI 候选确认及 native 离线执行判断；未引入其整套工作流、知识库或签名重建器 |

本次 `apk-reverse` 移植的逐文件来源、原文件 SHA-256、去向、取舍理由、代码调整和验证范围，见 [maintenance/migration.json](maintenance/migration.json)。来源仓库地址用于识别项目；实际移植内容以记录的本地快照为准，不依赖远程仓库当前状态。

上游 65 个源码条目中，15 个已迁入，另外 50 个保留方法或由现有工具路线承担。后者没有作为本项目的可运行脚本发布，不应根据上游文件名调用本地不存在的实现。

### 相关工具项目与评估边界

| 项目 | 与本项目的关系 |
|---|---|
| [Samael-Z/jadx-headless-mcp](https://github.com/Samael-Z/jadx-headless-mcp)、[1013503897/jadx-headless-mcp](https://github.com/1013503897/jadx-headless-mcp)、[zinja-coder/jadx-ai-mcp](https://github.com/zinja-coder/jadx-ai-mcp) | 配套本地 `jadx-headless` 工具的开发参考。本技能使用它暴露的无头能力；这些 MCP 服务的实现未打包进技能目录 |
| [APKLab/APKLab](https://github.com/APKLab/APKLab) | 做过工具与工作流评估，未直接迁入 APKLab 代码，也不依赖其 VS Code GUI 扩展 |
| Apktool、Android Build Tools、Frida、Reqable、JEB、IDA/idalib、mobile-mcp 等 | 可选择的外部实现。具体使用取决于宿主已注册接口及环境，不等于技能已安装或随附这些工具 |

迁入代码及相应测试的上游 MIT 许可文本保存在 [scripts/offline/LICENSE.apk-reverse](scripts/offline/LICENSE.apk-reverse)。该文件对应迁入部分的来源声明，不表示所有外部工具或方法来源使用同一许可证。

## 两类路由

### 技能路由：选择经验

回答当前问题涉及什么机制、如何定位与验证，例如 JSVMP、React Native、IL2CPP、反分析或长连接。完整入口在 [reference/experience-index.md](reference/experience-index.md)。

### 工具路由：选择实现

回答本次操作使用什么工具、如何加载目标、理解输出及处理生命周期。入口在 [reference/tool-capabilities.md](reference/tool-capabilities.md)，具体操作放在 `reference/tools/`。

两者是多对多关系。一个 React Native 目标的签名可能同时涉及 Hermes、JSVMP 和 native；Agent 可组合这些经验，再选择已有静态产物、无头服务、局部运行观测或离线执行。工具不可用不会使对应经验失效。

工具发现按需进行：先利用宿主已暴露的接口，首次使用某项能力时轻量验证，任务内复用结果；连接、配置、设备或宿主变化后再检查。默认不扫描、启动或安装全部工具。

## 目录结构

```text
android-reverse/
├── README.md                     使用者说明与完整文件导航
├── SKILL.md                      Agent 入口、执行原则、经验路由与工具路由
├── reference/
│   ├── experience-index.md       经验专题索引
│   ├── tool-capabilities.md      工具发现、缓存与操作文档索引
│   ├── *.md                     基础经验、运行时、证据与可选工作状态
│   ├── topics/                  28 份专项经验与故障案例
│   └── tools/                   8 份工具操作文档
├── scripts/
│   ├── run-frida.ps1             旧有 Windows/Conda 本机兼容适配器
│   └── offline/                 15 个离线辅助脚本及上游许可
└── maintenance/
    ├── migration.json           完整来源、去向、调整与验证记录
    ├── validate_skill.py        只读结构、引用、覆盖与语法检查
    ├── run_tests.py             离线回归入口
    ├── pytest.ini               回归配置
    └── tests/                   测试、隔离适配器与合成 DEX 夹具生成器
```

当前参考文档共 53 份：17 份基础文档、28 份专题文档和 8 份工具文档。README 与维护材料供使用者或维护者查阅，不要求每次任务全部加载。

## 文档清单

### 入口与基础文档

下表除 `SKILL.md` 外，文件均位于 `reference/`。

| 文件 | 功能 |
|---|---|
| [SKILL.md](SKILL.md) | 适用边界、授权与证据原则、执行自由度、任务模式，以及两类独立路由 |
| [experience-index.md](reference/experience-index.md) | 按问题查找经验专题，可组合多个主题，不形成封闭能力清单 |
| [tool-capabilities.md](reference/tool-capabilities.md) | 按需发现工具、任务内缓存、等价无头实现和工具操作文档索引 |
| [package-recon.md](reference/package-recon.md) | APK 结构、关键逻辑归属、跨层边界及 Java2C/JNI/抽取恢复候选判别 |
| [static-analysis.md](reference/static-analysis.md) | Java/Kotlin、Manifest、字符串、调用链和静态证据的分析方法 |
| [native-analysis.md](reference/native-analysis.md) | JNI 绑定、native 参数与类型、地址空间、算法线索和可选离线执行 |
| [dynamic-hook.md](reference/dynamic-hook.md) | 运行观察、目标签名、参数与返回值、原始名称和主动干预的证据边界 |
| [mobile-automation.md](reference/mobile-automation.md) | 冷/热启动、界面触发、条件等待及可比较运行样本的组织 |
| [network-traffic.md](reference/network-traffic.md) | 关键请求与响应读取、字段溯源、网络样本与代码/Hook 的对应 |
| [algorithm-validation.md](reference/algorithm-validation.md) | 请求签名与加解密的输入输出配对、字节语义、证书派生输入和复现范围 |
| [react-native-hermes.md](reference/react-native-hermes.md) | 实际 bundle 定位、可读 JS 与 Hermes 字节码区分、版本和加载来源核对 |
| [flutter-dart.md](reference/flutter-dart.md) | Flutter/Dart 构建形态、snapshot 兼容、对象池、字符串及 AOT 调用定位 |
| [unity-il2cpp.md](reference/unity-il2cpp.md) | Mono/IL2CPP 后端、native/metadata 配对、异常 metadata 及运行取证 |
| [vm-protection.md](reference/vm-protection.md) | native/DEX VM 识别、虚拟状态、handler、切片、差分、IR 与可调用程序抽取 |
| [patch-and-verify.md](reference/patch-and-verify.md) | 修改声明、对照、归档保留、重建签名、等长审计及安装到行为验收 |
| [evidence-and-renaming.md](reference/evidence-and-renaming.md) | `Observed`、`Inferred`、`Hypothesis`、`Refuted`，命名依据与来源/目标证据分层 |
| [workflow-gates.md](reference/workflow-gates.md) | 按模式和风险选择阶段检查与完成条件，不要求所有任务逐关执行 |
| [workspace-state.md](reference/workspace-state.md) | 可选 `.android-reverse/` 状态、目标隔离、交接、会话记录和清理边界 |

### 侦察、保护与代码定位专题

以下文件均位于 `reference/topics/`。

| 文件 | 功能 |
|---|---|
| [unpacking.md](reference/topics/unpacking.md) | 区分壳、按需恢复、native 下沉和解码异常；载荷取得、dump 去重及质量验证 |
| [native-loader.md](reference/topics/native-loader.md) | 自定义加载器、检查器与实现依赖、ELF 重定位、映射、dump 时机与修复边界 |
| [kotlin-names.md](reference/topics/kotlin-names.md) | Kotlin metadata、调试信息和其他名称线索；候选映射与功能证据交叉确认 |
| [dex-patching.md](reference/topics/dex-patching.md) | 原位、方法级和 smali 修改的选择；指令边界、字符串、控制流及最终落点审计 |

### JS、运行观测与反分析专题

| 文件 | 功能 |
|---|---|
| [js-ast.md](reference/topics/js-ast.md) | JS 字符串表、别名、常量与控制流重写；作用域、副作用、求值顺序和变换验证 |
| [jsvmp.md](reference/topics/jsvmp.md) | JS 私有载荷、栈机/寄存器机、PC、宿主环境、闭包/异常/返回语义及局部恢复 |
| [anti-analysis.md](reference/topics/anti-analysis.md) | 区分环境、工具、脚本、消息投递和目标检测；无注入、观察与干预的可比较条件 |
| [native-tamper.md](reference/topics/native-tamper.md) | 主动退出、abort、信号、冻结及完整性响应归因，避免把进程存活当业务正常 |
| [native-tracing.md](reference/topics/native-tracing.md) | DBI 和指令轨迹的观测目标、覆盖健康、差分、切片与平坦化分析 |
| [rpc-emulation.md](reference/topics/rpc-emulation.md) | 原函数 RPC、指令模拟、Android/JNI 模拟与独立实现的选择、状态及验证 |
| [remote-debugging.md](reference/topics/remote-debugging.md) | 原生调试连接、暂停/恢复时序、实际 ABI、APK 内映射与断点未绑定诊断 |
| [python-payload.md](reference/topics/python-payload.md) | Android 关联 Python、pyc/pyz 和受保护载荷的识别、版本与恢复边界 |

### 业务、数据与协议专题

| 文件 | 功能 |
|---|---|
| [ads-remote-config.md](reference/topics/ads-remote-config.md) | 广告链和回调、服务端 UI、多层配置、缓存及修改持续性 |
| [accounts-limits.md](reference/topics/accounts-limits.md) | 分开页面入口、客户端提交与服务端资源/权限，解释登录、绑定、游客及限制 |
| [updates.md](reference/topics/updates.md) | 版本比较、提示、自更新、动态模块、热更新及远程重新启用路径 |
| [runtime-data.md](reference/topics/runtime-data.md) | SharedPreferences、DataStore、MMKV、SQLite、blob、内存缓存与写回来源 |
| [tls.md](reference/topics/tls.md) | 握手、证书链、信任策略、Java/native 栈及局部联网失败诊断 |
| [protocols.md](reference/topics/protocols.md) | Protobuf 候选类型/schema、gRPC framing、QUIC、长连接状态链及不透明 body |
| [system-ipc.md](reference/topics/system-ipc.md) | Binder/AIDL、Intent、WebView bridge、SELinux 以及设备证明与远端信任边界 |

### 交付、设备与高级观测专题

| 文件 | 功能 |
|---|---|
| [split-packages.md](reference/topics/split-packages.md) | base/split/动态模块身份、集合签名与安装、资源合并和设备匹配限制 |
| [third-party-builds.md](reference/topics/third-party-builds.md) | 审计第三方修改包的新增组件、归档差异、加载关系及行为候选 |
| [module-delivery.md](reference/topics/module-delivery.md) | LSPosed/Xposed 的作用域、Hook 语义、构建、框架激活与交付依赖 |
| [device-environment.md](reference/topics/device-environment.md) | PID/ABI/存活、前台、日志、Shell、时钟、代理和设备状态诊断 |
| [on-device.md](reference/topics/on-device.md) | 设备侧 MT/APK MCP、Termux 等工作位置的选择和产物核对 |
| [kernel-observation.md](reference/topics/kernel-observation.md) | root/用户态/内核层次、暴露、接口依赖、主动干预及生成到运行的验证分层 |
| [hardware-tracing.md](reference/topics/hardware-tracing.md) | 硬件观察点、ETE/TRBE、SPE/BRBE、地址符号化与轨迹差分的前提和边界 |

### 故障与案例

| 文件 | 功能 |
|---|---|
| [failure-catalog.md](reference/topics/failure-catalog.md) | 50 类故障、误判与反例的查询入口；按症状选择补证方向 |
| [cases.md](reference/topics/cases.md) | 五类来源案例的通用经验，以及按需保存可复用案例的方法 |

### 工具操作文档

以下文件均位于 `reference/tools/`。它们解释选定工具后的操作，不替代经验专题。

| 文件 | 功能 |
|---|---|
| [jadx.md](reference/tools/jadx.md) | JADX/JEB 或等价无头服务的目标核对、索引覆盖、smali 降级、分页及生命周期 |
| [idalib.md](reference/tools/idalib.md) | 无头 native 会话、概览、查询、类型/注释、缓存与数据库保存 |
| [frida.md](reference/tools/frida.md) | MCP/CLI 连接、版本与 bridge、spawn/attach、重载、RPC 会话和消息健康 |
| [network.md](reference/tools/network.md) | Reqable 等实际接口、捕获记录、原始报文、重放及设置变更边界 |
| [device.md](reference/tools/device.md) | mobile-mcp、元素/坐标、ADB 参数、设备身份、安装、日志和设备侧接口 |
| [apk.md](reference/tools/apk.md) | Apktool 的 `-s/-r`、MCP 工作区、调试选项、归档、对齐、签名及密码处理 |
| [offline.md](reference/tools/offline.md) | 已迁入脚本、输入输出边界、外部 DEX 索引/SQL 与 JS 解析器选择 |
| [specialists.md](reference/tools/specialists.md) | Dart/Unity 前端、模拟执行、调试器、软件轨迹与硬件生产端的实际能力核对 |

## 脚本清单

### 离线辅助脚本

以下 15 个文件位于 `scripts/offline/`，使用 Python 标准库，不主动连接手机或线上服务。其中部分操作会写输出，仍须按具体参数选择独立文件或目录，保护原始证据。

| 文件 | 功能 | 主要边界 |
|---|---|---|
| [apk_diff.py](scripts/offline/apk_diff.py) | 比较两个 APK 的条目新增、删除、内容与压缩方式变化 | 采用流式哈希，拒绝重复条目名；不检查全部 ZIP 元信息、布局、签名或安装合法性 |
| [dexutil.py](scripts/offline/dexutil.py) | DEX 结构、方法、指令和头部完整性的基础解析库，也可查看指定方法 | 有限解码与结构检查；不是官方 verifier，不保证支持任意 DEX 变体 |
| [dex_strings.py](scripts/offline/dex_strings.py) | 从单个 DEX 或含 DEX 的目录提取字符串、URL、类描述符并做过滤或差分 | 显示数量与长度有界；字符串表不等于业务引用或运行使用 |
| [dex_classdiff.py](scripts/offline/dex_classdiff.py) | 比较两份 DEX 的类名集合与 access flags | 普通标志变化也会影响结果；类名和标志一致不能证明方法体一致 |
| [dex_find_insn.py](scripts/offline/dex_find_insn.py) | 按类、方法及指令语义过滤器定位 DEX 中的候选位置和上下文 | 不完整解码后的偏移需要交叉核对；归档内的 DEX 成员按接口明确选择 |
| [dex_dump_validate.py](scripts/offline/dex_dump_validate.py) | 分析 DEX dump 的结构、完整性、类/方法、内容哈希及方法体形态，输出启发式排序 | 排名、stub 比例和最小方法体形态不能证明哪份是原始载荷或目标保护类型 |
| [java2c_probe.py](scripts/offline/java2c_probe.py) | 汇总 APK/DEX/ELF 的 native 声明、比例、符号和工具链形态指标 | 输出保留 `unconfirmed` 与候选判断；不会仅凭密度或 `JNI_OnLoad` 确认 Java2C/动态注册 |
| [kotlin_name_recovery.py](scripts/offline/kotlin_name_recovery.py) | 从已有反编译 Java 源码提取候选 Kotlin 名称，建立并查询映射 | 构建映射必须显式指定新输出目录；不自动重命名，不保证所有 metadata 版本均支持 |
| [js_obf_detect.py](scripts/offline/js_obf_detect.py) | 根据 JS 文本和可选提示评估混淆家族、残留特征及处理建议 | 正则与文本评分是启发式；不是 AST 解析、改写或 VMP 确认工具 |
| [jsvmp_loader_decode.py](scripts/offline/jsvmp_loader_decode.py) | 解码特定 Base64/hex/字节到 varint、ZigZag 整数流的载荷链 | 先从目标 loader 确认编码链；不支持任意 JSVMP，也不恢复完整指令语义 |
| [blob_decode.py](scripts/offline/blob_decode.py) | 对指定值或 XML 键尝试编码、旋转、压缩组合，并支持按参数重新编码 | 输出为格式候选；结构可读或评分较高不等于业务语义或密码算法已确认 |
| [protobuf_decode_raw.py](scripts/offline/protobuf_decode_raw.py) | 无 schema Protobuf 解析、候选展开、消息拆分、JSON 及再编码对照 | 字段类型、嵌套和 packed 解释存在歧义；再编码一致不能证明业务含义 |
| [trace_addr2sym.py](scripts/offline/trace_addr2sym.py) | 根据 ELF64、映射/基址和地址列表进行地址换算与符号定位 | 文件偏移与虚拟地址要明确；strip 或最近符号输出不能当成精确函数执行证明 |
| [trace_diff.py](scripts/offline/trace_diff.py) | 对兼容格式轨迹做重复压缩、块统计、首个分歧和差异区域分析 | 需对齐构建、地址空间及输入条件；轨迹差异不是自动因果证明 |
| [vm_handler_slice.py](scripts/offline/vm_handler_slice.py) | 基于轨迹及可选分发器/映射做 handler 分段、签名聚类与轨迹整理 | 依赖同目录 `trace_diff.py`；自动分发器和聚类结果为候选，不等于虚拟语义恢复 |

这些脚本中的多数字段和参数沿用上游接口，迁移时对部分行为做了修正。具体代码调整和文件哈希见 [移植记录](maintenance/migration.json)，当前输入方式以脚本 `--help` 为准。

### 本机兼容适配器

[scripts/run-frida.ps1](scripts/run-frida.ps1) 是历史保留的 Windows/Conda 适配器：查找 Conda 中名为 `android` 的环境，再调用其中的命令。它不是通用环境要求，也未参与本次 15 个离线脚本的回归。

该文件不在默认工具路由中。其他环境可使用实际 Frida CLI 或 MCP，无须创建同名 Conda 环境。使用此适配器前应核对它的路径发现、环境名称和所传命令。

### 命令示例

以下文件名仅用于说明调用形式，应替换为当前任务已选定的真实输入。示例不表示项目已用这些文件完成过分析。

```text
# 查看具体工具的真实参数
python scripts/offline/apk_diff.py --help

# 比较 APK 的条目内容与压缩方式
python scripts/offline/apk_diff.py original.apk modified.apk --summary

# 在 DEX 字符串表中筛选
python scripts/offline/dex_strings.py classes.dex --find "http"

# 解析已经取得的二进制 Protobuf 消息
python scripts/offline/protobuf_decode_raw.py message.bin --json

# 对照两份已有轨迹
python scripts/offline/trace_diff.py diff --a before.log --b after.log --json
```

解析输出还需结合真实代码、调用与协议上下文。某个脚本能成功运行，与它能完整回答当前问题是两件事。

## 使用与环境

### 让 Agent 使用

把完整 `android-reverse/` 目录放到支持 Agent Skills 的宿主可发现位置，或按宿主规则建立链接。保留 `SKILL.md`、参考文档和需要使用的脚本；只复制入口文件会丢失按需材料。

先向 Agent 指定分析目标、问题、已有材料与期望交付物。没有要求正式报告时可直接对话回答；没有要求修改 APK 时不自动进入重建流程。

| 模式 | 适用任务 | 主要结果 |
|---|---|---|
| `analysis` | 解释、定位、调用链、算法与行为还原 | 有来源的结论、推断及待确认项 |
| `runtime-validation` | 需要设备、Hook、抓包或运行样本补证 | 触发条件、原始样本及主动干预条件 |
| `patch-and-verify` | 用户明确要求修改、重建或输出可安装 APK | 修改范围、产物身份，以及构建到目标行为的独立验收结果 |

已有反编译产物可以直接用于分析。任务需要比较多个版本、split 集合或关联载荷时，可以分别确认身份并隔离证据，不要求始终只处理一个文件。

### 依赖按操作选择

| 操作 | 需要的能力 |
|---|---|
| 阅读已有产物与经验文档 | 对应文件读取与分析能力，不需要启动全部 MCP |
| 使用随附离线脚本 | 兼容的 Python 解释器；部分脚本使用 Python 3.10+ 语法 |
| Java/Kotlin 安装包静态分析 | 当前可用的无头 DEX 分析服务、CLI 或已有产物 |
| native/JNI 分析 | 无头 native 工具或其他能够回答问题的解析/反汇编能力 |
| 动态验证 | 所需设备、权限、进程与兼容的 Hook/抓包/调试实现；是否需要 root 由具体路径决定 |
| 修改与签名 | 能表达变更的构建/归档实现、对齐和签名工具；安装验收还需对应设备能力 |
| Flutter、Unity、硬件或内核专题 | 与目标版本、格式、ABI 和设备匹配的专项实现，不由文档存在推定可用 |
| 维护回归 | Python 与可用的 pytest；部分扩展测试还需样本或 C 编译器 |

本项目不随附 MCP 服务端、JAR、解码器二进制、Android SDK、Frida server、签名密钥、内核驱动或完整 AST 重写器。外部工具由当前环境提供，缺失时可选择等价无头能力。

`analysis-report`、`final-report` 是本机可选的报告技能，只有用户要求相应报告且环境提供时才组合使用；它们不包含在此目录中，也不是逆向分析的必需依赖。

`.android-reverse/` 是分析任务中的可选状态目录，与技能安装目录不同。简单任务不自动创建；复杂任务需要持久化时，优先遵守用户或项目已指定的路径。

## 维护与验证

### 维护文件

| 文件 | 功能 |
|---|---|
| [maintenance/migration.json](maintenance/migration.json) | 67 份上游参考、65 个源码条目的来源哈希、处置、目标文件、调整及验证记录 |
| [maintenance/validate_skill.py](maintenance/validate_skill.py) | 检查入口 frontmatter、文档链接与标题锚点、参考可达性、移植映射、离线脚本语法及上游许可文件 |
| [maintenance/run_tests.py](maintenance/run_tests.py) | 运行离线 pytest，禁用无关全局插件与缓存写入；缺少 pytest 时说明未执行，不自动安装 |
| [maintenance/pytest.ini](maintenance/pytest.ini) | 指定测试目录、结果说明与测试标记 |
| [maintenance/tests/conftest.py](maintenance/tests/conftest.py) | 离线脚本白名单、模块加载、临时工作目录、子进程与测试夹具适配 |
| [maintenance/tests/fixtures/make_fixture_dex.py](maintenance/tests/fixtures/make_fixture_dex.py) | 生成引用关系已知的合成 DEX，供解析和定位回归；不作为真实应用或完整运行时验证样本 |

### 回归测试文件

| 文件 | 验证内容 |
|---|---|
| [test_apk_diff.py](maintenance/tests/test_apk_diff.py) | 等长内容修改、仅压缩方式变化、重复 ZIP 条目拒绝及相同归档 |
| [test_offline_cli.py](maintenance/tests/test_offline_cli.py) | 15 个帮助入口、合成 DEX 解析/定位/差异、候选判定边界、显式输出要求及二进制编码 |
| [test_dexutil.py](maintenance/tests/test_dexutil.py) | DEX 基础读取、指令宽度、分支及头部完整性；依赖未随附样本的用例跳过 |
| [test_blob_decode.py](maintenance/tests/test_blob_decode.py) | 外层编码、压缩、旋转搜索与命令行路径 |
| [test_protobuf_decode_raw.py](maintenance/tests/test_protobuf_decode_raw.py) | wire 解析、候选解释、已知向量及再编码对照 |
| [test_js_obf_detect.py](maintenance/tests/test_js_obf_detect.py) | 文本家族检测、阈值、提示与残留统计 |
| [test_jsvmp_loader_decode.py](maintenance/tests/test_jsvmp_loader_decode.py) | Base64/hex、varint、ZigZag 的已知向量和往返 |
| [test_kotlin_name_recovery.py](maintenance/tests/test_kotlin_name_recovery.py) | 注解与名称候选来源、跳过规则及映射输出 |
| [test_trace_addr2sym.py](maintenance/tests/test_trace_addr2sym.py) | ELF 地址换算、strip/未映射区间与输入适配；部分测试依赖 C 编译器 |
| [test_trace_diff.py](maintenance/tests/test_trace_diff.py) | 轨迹格式、重复压缩、对齐与差分输出 |
| [test_vm_handler_slice.py](maintenance/tests/test_vm_handler_slice.py) | 分发器候选、分段、聚类、未闭合片段及可选 opcode 映射 |

### 运行检查

在项目根目录、使用具备所需依赖的解释器执行：

```text
python -B maintenance/validate_skill.py
python -B maintenance/run_tests.py
```

维护命令是人工维护入口，不是 Agent 每次开始分析都要运行的步骤。`validate_skill.py` 当前检查 `SKILL.md` 与 `reference/` 的文档结构，不将本 README 当成运行时参考，也不检验远程来源网址的可访问性。

增加经验文档时更新经验索引；增加工具操作或脚本时更新工具路由与接口说明。新脚本先检查副作用，再在隔离目录中验证实际输入输出。上游文件变更不自动同步覆盖本地修改。

### 已记录的结果

截至 **2026 年 10 月 26 日的移植验证记录**：

- 离线回归：210 项通过，7 项跳过。
- 5 项跳过依赖未随附的上游样本；2 项跳过因测试环境缺少 C 编译器。
- `SKILL.md` 与参考文档共 54 份，242 个链接的结构检查通过。
- 整份技能复制到另一目录后，结构检查和离线回归仍通过；环境为同一 Windows 主机、Python 3.13。
- 随附许可、来源映射、脚本语法和参考可达性检查通过。

这些结果不等于 210 个真实应用成功案例。测试覆盖的是已知向量、解析、命令行和隔离夹具；跳过项不算通过。同主机换目录也不等于 Linux、macOS 或所有 Python 版本都已验证。

尚未完成真实设备、内核/硬件路线的整套验收，也未进行同模型、同任务、同工具下的有技能/无技能效果对照。因此不以文件数量、测试数量或方法覆盖宣称一定提高 Agent 能力。

## 已知边界

- 工具连接成功、索引完成、反编译成功、脚本退出成功与业务结论正确分别判断。
- 启发式评分、一个匹配样本、局部 verifier 检查或方法骨架，不能升级为完整恢复。
- 只观察的 Hook 也可能改变时序、代码或映射；原始条件与干预条件应能区分。
- 硬件、内核、运行时桥接和远程调试方法有设备与版本前提，当前未附带相应生产端或驱动。
- 构建、签名、安装、启动与目标行为各有证据要求，状态文件和正式报告按任务需要决定。
- 修改产物不覆盖原始 APK、SO 或证据；技能不因任务结束自动清理用户文件。
- 仅处理任务授权范围内的目标、设备、账户和操作。读取方法或具备工具，不自动获得修改、提权或发送真实请求的权限。

需要追溯某个来源条目为什么迁入、合并或未打包，直接查阅 [完整移植记录](maintenance/migration.json)；需要开始具体分析，从 [SKILL.md](SKILL.md) 及当前问题对应的经验入口选择即可。
