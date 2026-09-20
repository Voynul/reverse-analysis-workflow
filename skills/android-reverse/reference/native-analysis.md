# Native 层分析规范

## 触发条件

出现以下任一情况时使用无头 IDA 服务 `idalib-mcp`：

1. Java 层调用 `native` 方法。
2. 发现 `System.loadLibrary` 或 so 加载逻辑。
3. 关键参数、签名、加密、解密、校验进入 `.so`。
4. 用户明确要求分析 so、JNI、native 函数或导出符号。
5. Frida Hook 发现 Java 层入参和返回值之间缺少解释，需要看 native 内部。

## 分析要求

- 检查反编译结果，并根据分析需要添加注释。
- 根据后续分析和可读性需要决定是否重命名变量、函数或其他符号；用户明确要求时优先执行。
- 如有必要，更改变量和参数类型，尤其是指针和数组类型。
- 如果需要更多细节，分解函数并添加注释说明发现。
- 切勿自行转换数字基数；如有需要，使用 `int_convert` MCP 工具。
- 不要尝试暴力破解，应基于反汇编、伪代码、交叉引用和简单脚本推导。
- 不强制创建 `native-report.md`；是否落盘由用户要求、正式报告策略或 agent 的复用需要决定。

## 工具选择

1. 当前环境提供 `idalib-mcp` 时优先使用，工具命名空间由当前 Agent 宿主决定；不可用时可以选择经过验证的等价无头 native 分析工具，但不得探测、调用或接管 GUI IDA MCP。
2. 用户明确给出 so/二进制绝对路径时，调用 `idb_open` 并显式设置 `mode="force_headless"`；打开后输出文件名、路径、架构等可取得的身份信息。
3. so 由已确认 APK 的 Java/JNI 调用链唯一定位时，可以直接打开并说明来源；存在多个 ABI、多个同名 so 或来源不明确时，让用户选择。
4. 调用 `idb_list` 确认可用 database/session，再用 `server_health` 检查自动分析和反编译器状态。
5. 当前环境没有 `idalib-mcp`，或打开、健康探测失败时，先检查是否存在等价无头 native 分析能力；没有替代方案时暂停 native 分支并报告失败原因，不回退 GUI IDA。
6. 数字进制转换优先使用服务提供的 `int_convert`；不可用时使用可审计的计算工具，不凭心算给出高风险结论。

## Session 所有权与生命周期

`idalib-mcp` session 与 APK 没有强制对应关系。APK 切换不自动关闭 session，也不自动切换目标 so。

为每个可管理的 session/database 记录：

- session/database 标识。
- 目标二进制绝对路径。
- `opened_by`：固定为 `agent/headless`。
- `related_apk`：可选，仅在存在明确 Java/JNI 关系时填写。
- `purpose`：例如 JNI 链路或独立 so 分析。
- `idle_ttl_sec`：无头 worker 的空闲退出时间。
- `saved_idb_path`：可选，保存数据库后记录。

Agent 不通过系统命令终止 worker。无头 worker 由 `idle_ttl_sec` 和服务端生命周期机制退出；需要保留分析成果时先使用服务提供的保存能力。

## 分析步骤

1. 确认目标 so 文件名、路径、架构和来源；无头模式下用绝对路径 `idb_open`。
2. 查找 JNI 导出函数和 `RegisterNatives` 注册表。
3. 建立 Java 方法到 native 函数的映射。
4. 搜索关键字符串、URL、算法常量、错误码、字段名。
5. 查看交叉引用，定位调用链和数据流。
6. 阅读伪代码，识别参数处理、编码、加密、签名、校验和返回结构。
7. 必要时用 Frida Native Hook 验证入参、返回值和内存数据。

## 输出要求

- 当前问题涉及 Java/JNI 关系时，写清 Java 入口和 native 函数之间的对应关系。
- 写清关键字符串、常量、算法或分支的来源。
- 对伪代码结论标注函数地址或函数名。
- 反编译不确定时标注待确认，不把猜测写成结论。
- native 目标与 APK 有明确关系时，将结果回链到 Java 层调用点或真实运行样本；独立 so 分析不强制建立 APK 关联。
- 默认在对话中回答；只有用户要求、正式报告策略启用或 agent 判断需要复用时才创建文档。
