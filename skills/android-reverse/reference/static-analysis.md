# 静态分析规范

## 工具选择

1. 优先使用 JADX MCP 分析 Java/Kotlin 层代码。
2. JADX 反编译不清晰、控制流异常、泛型或匿名类难读时，使用 JEB MCP 交叉验证。
3. JADX 与 JEB 结果不一致时，以 smali、调用关系和运行时 Hook 结果辅助判断。
4. 关键结论至少要有一种反编译代码证据；复杂混淆逻辑建议使用双工具或 Hook 补证。

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
6. 对混淆符号执行功能命名。
7. 对关键结论保存来源位置和代码片段。

## 混淆命名强制规则

遇到无意义类名、方法名、字段名、变量名时，必须先根据功能重命名，再在结论或报告中引用。

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
5. 不确定时：使用 `_TODO` 后缀，并在待确认中说明。

命名风格：

- 类名使用 PascalCase，例如 `AdConfigManager`。
- 方法和变量使用 camelCase，例如 `parseAdResponse`、`encryptedBytes`。
- 方法名优先使用动作加对象，例如 `decryptPayload`、`loadRemoteConfig`。

## rename.md 记录

每次重命名后必须立即写入当前任务目录下的 `rename.md`，不要等全部完成后批量补。

推荐表格：

| 类型 | 原始名称 | 新名称 | 功能说明 | 证据位置 | 状态 |
|---|---|---|---|---|---|
| 类/方法/字段/变量 | 原名 | 新名 | 白话说明 | 类、方法、日志或报告位置 | 已确认/待确认 |

报告引用格式：

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

## 搜索技巧

- JADX 的类搜索通常不适合直接输入带点完整路径，优先用短关键词。
- 查广告或聚合相关逻辑时，可搜索 `adapter`、`mediation`、`network`、`bid`、`impression`、`preload` 等关键词。
- 第三方公开 SDK 只作为边界和调用方确认，优先深入自建 SDK、混淆包和用户指定目标。

## 静态证据要求

每个关键判断必须记录：

- 类和方法位置。
- 原始混淆名和可读名称。
- 判断条件或关键代码片段。
- 该代码影响的行为。
- 是否需要 Frida Hook、抓包或 native 分析继续验证。
