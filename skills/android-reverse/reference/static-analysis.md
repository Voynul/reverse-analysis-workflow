# 静态分析规范

## 工具选择

一次 APK 分析任务只选择一个 JADX 模式。用户明确指定 GUI 或无头时，以用户指定为准。

### GUI 探测与确认

1. 先探测 `jadx_mcp` 是否可以连接。
2. GUI 无法连接：
   - 用户已提供 APK 绝对路径时，使用 `jadx_headless`。
   - 用户未提供路径时，提醒用户提供路径或打开 JADX GUI。
3. GUI 可以连接但未加载 APK：提醒用户在 GUI 中加载 APK，或明确选择无头并提供绝对路径；不得自动回退。
4. GUI 已加载 APK：在执行正式分析前输出可取得的 APK 路径或文件名、包名、`versionName` 和 `versionCode`，等待用户确认。
5. 无法取得包名和版本信息时，说明缺失字段并等待用户决定，不能只凭类列表认定目标正确。
6. 用户确认对当前 APK 分析任务有效。每次恢复静态分析分支时做一次轻量预检；路径、包名或版本变化时立即暂停并重新确认。
7. GUI 生命周期由用户管理。Agent 可以在 GUI 开启期间使用 MCP，但不得主动启动、关闭 GUI、关闭工程或切换用户的 APK。

### 无头加载与确认

1. 用户明确给出的 APK 绝对路径本身构成目标选择，可以直接调用 `load_apk`。
2. 加载后用 `current_apk`、`index_status` 和 Manifest 输出路径、包名及版本信息；发现与用户描述不符时暂停。
3. 用户只给包名、功能描述或模糊目录时，不得自行挑选 APK。
4. 服务中残留的 APK 只有在 `analysis-state.md` 已确认它是当前目标时才可沿用。
5. 无头模式不要调用 GUI 专用接口：`fetch_current_class`、`get_selected_text`、`debug_*`、`rename_variable`。可用 `get_class_source`、`get_main_activity`、`get_xrefs_to_*` 等接口。

### 任务内锁定与故障回退

1. 已确认的 GUI/无头选择绑定当前 APK；同一分析任务内不要来回混用。
2. GUI 分析途中连接中断时，只执行一次只读健康重试。
3. 重试失败后说明失败位置和已完成内容。切换无头必须由用户确认；已知目标绝对路径时可提出切换选项。
4. 工具失败只能证明工具当前不可用，不能证明 APK 中不存在对应逻辑。
5. JADX 反编译不清晰、控制流异常、泛型或匿名类难读时，可自动使用 JEB 或 smali 对同一目标做只读交叉验证，并说明原因。
6. JADX 与 JEB 结果不一致时，用 smali、调用关系和运行时 Hook 结果辅助判断。

### 生命周期

1. 中间汇报、等待补充或继续同一 APK 的分析时保持无头服务运行。
2. 用户表示结束、当前项目任务完成、主动要求释放资源或 Codex 任务关闭时调用 `shutdown_jadx`。
3. 用户顺序切换 APK 时可以复用无头服务并重新加载目标，不要求重启 JVM。
4. 长时间无操作由 idle watchdog 退出；用户关闭“JADX Headless MCP - running”窗口也会终止服务。

## 常见入口

- `AndroidManifest.xml` 中的 Application、Activity、Service、Receiver、Provider。
- 用户给出的包名、类名、方法名、日志关键词、URL、字段名。
- SDK 初始化入口、点击事件、生命周期方法、网络客户端、加解密工具类。
- JNI 方法声明，例如 `native` 方法、`System.loadLibrary`、`RegisterNatives` 相关调用。

## 分析步骤

1. 查看 Manifest，确认组件、权限、入口和声明的 SDK 信息。
2. 搜索关键词，定位候选类、字符串、URL 和配置项。
3. 获取类源码和方法源码，阅读真实控制流。
4. 获取调用者和被调用者，补齐上游触发和下游结果。
5. 识别配置读取、分支判断、缓存读写、网络请求和回调。
6. 按后续分析需要理解混淆符号，并自主决定是否执行功能命名。
7. 对关键结论保存来源位置和代码片段。

## 混淆理解与命名

先理解混淆符号的功能，再决定是否需要工具内重命名或落盘。命名是提高分析效率和可读性的手段，不是每次分析的强制产物。

需重命名的典型模式：

| 模式 | 示例 | 说明 |
|---|---|---|
| 单字母 | `a`, `b`, `A` | 单字符类名、方法名、字段名 |
| 重复短串 | `aa`, `bb`, `dd` | 无业务含义的重复字符 |
| 数字字母拼接 | `0oo`, `a1`, `C0001` | 无意义编号或混合名 |
| 大小写乱序 | `oO0Oo`, `ll1lI` | 混淆生成名 |
| 无意义短串 | `xx`, `zz`, `m1` | 无法直接说明功能 |

命名优先级：

1. `.source` 优先：如果 smali 中 `.source` 不是 `"SourceFile"`、`"R8.java"`、`"unknown"` 等自动生成名，优先用它作为类名。
2. `toString()` 优先：如果 `toString()` 返回有意义结构，如 `AdPositionConfig(id=...)`，优先据此命名类和字段。
3. 字符串线索：日志、异常、常量、URL、字段名中出现业务词时优先参考。
4. 代码功能：根据继承关系、接口、调用方、被调用方、字段用途推断。
5. 不确定时：保留原名并标注疑似功能；需要持久化暂定名时可使用 `_TODO` 后缀。

命名风格：

- 类名使用 PascalCase，例如 `AdConfigManager`。
- 方法和变量使用 camelCase，例如 `parseAdResponse`、`encryptedBytes`。
- 方法名优先使用动作加对象，例如 `decryptPayload`、`loadRemoteConfig`。

## 命名记录

Agent 根据后续分析是否需要复用，自主决定是否在当前目标的内部工作目录创建 `rename.md`。用户明确要求重命名、提供可读名称或维护命名记录时优先执行。

推荐表格：

| 类型 | 原始名称 | 新名称 | 功能说明 | 证据位置 | 状态 |
|---|---|---|---|---|---|
| 类/方法/字段/变量 | 原名 | 新名 | 白话说明 | 类、方法、日志或报告位置 | 已确认/待确认 |

需要建立可回查映射时使用：

```text
包名.原名→新名
```

示例：

```text
ka.u3→GaConfigManager
ea.y→AdFrequencyManager
```

## 常用操作速查

| 任务 | JADX MCP | JEB MCP |
|---|---|---|
| 查看 Manifest | `get_android_manifest` | `get_manifest` |
| 搜索类名 | `search_classes_by_keyword` | `list_classes` / 字符串搜索 |
| 获取类源码 | `get_class_source` | `get_class_decompiled_code` |
| 获取方法源码 | `get_method_by_name` | `get_method_decompiled_code` |
| 获取所有类 | `get_all_classes` | 类列表相关工具 |
| 获取字段 | `get_fields_of_class` | `get_class_field` / 字段列表 |
| 获取方法列表 | `get_methods_of_class` | 方法列表相关工具 |
| 查调用关系 | `get_xrefs_to_*` | `list_cross_references` / `get_method_callers` |
| 查看 smali | `get_smali_of_class` | `get_method_smali_code` |
| 重命名类 | `rename_class` | `rename_class_name` |
| 重命名方法 | `rename_method` | `rename_method_name` |
| 重命名字段 | `rename_field` | `rename_class_field` |
| 重命名变量 | `rename_variable` | `rename_pseudo_code_variables` |


无头 JADX 补充：`get_main_activity_class` 会映射到 `get_main_activity`；`get_all_resource_file_names` 会映射到 `list_resource_files`。`rename_variable` 在无头中不可用；是否改用类、方法、字段或包重命名由分析需要决定，不为重命名展示效果切换 GUI。

## 搜索技巧

- JADX 的类搜索通常不适合直接输入带点完整路径，优先用短关键词。
- 查广告或聚合相关逻辑时，可搜索 `adapter`、`mediation`、`network`、`bid`、`impression`、`preload` 等关键词。
- 第三方公开 SDK 只作为边界和调用方确认，优先深入自建 SDK、混淆包和用户指定目标。

## 静态证据要求

每个关键判断必须记录：

- 类和方法位置。
- 原始混淆名；已经创建语义名称时同时记录可读名称。
- 判断条件或关键代码片段。
- 该代码影响的行为。
- 是否需要 Frida Hook、抓包或 native 分析继续验证。
