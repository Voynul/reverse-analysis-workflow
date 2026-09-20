# 工具能力与命名

## 通用规则

本技能面向多个 Agent 宿主。不同宿主可能为 MCP 工具添加不同前缀或命名空间，因此：

1. 先查看当前环境实际暴露的服务和工具列表，不调用工具完成这一步。
2. 按服务名和逻辑能力匹配，不假设宿主生成的命名空间前缀、安装路径或版本。
3. 只调用已注册接口，不根据旧文档猜测不存在的工具。
4. 只在任务第一次需要某项能力时做轻量验证，同一任务内复用结果。
5. 工具不可用时可以选择经过验证的等价无头工具；没有替代方案时报告受影响能力，不静默切换到 GUI 服务。

## 按需发现与缓存

- 普通静态分析只检查静态分析分支；不预检 IDA、Frida、抓包、构建或签名工具。
- native、运行验证、网络和修改分支在被实际触发时分别检查。
- 工具列表中的已注册状态只证明接口存在；第一次实际使用时通过轻量只读调用或真实操作确认连接状态。
- 当前任务记录 `not-checked`、`available`、`unavailable` 或 `failed` 即可，不要求写入文件。
- 连接失败、工具重启、配置变化、设备变化或宿主变化后再重新验证。
- 长任务可以在状态文件中记录工具、版本、连接方式和检查时间，但跨任务记录仅作提示，不能代替首次使用验证。

## 能力映射

| 服务 | 核心逻辑操作 | 用途 |
|---|---|---|
| `jadx-headless` | `load_apk`、`current_apk`、`index_status`、`get_android_manifest`、`get_class_source`、`get_smali_of_class`、`search_in_code`、`get_xrefs_to_*` | Java/Kotlin、smali、资源、搜索和调用关系 |
| `idalib-mcp` | `idb_open`、`idb_list`、`server_health`、字符串、交叉引用、反汇编、伪代码和保存操作 | native so/JNI 无头分析 |
| Frida 服务 | `check_frida_status`、`spawn`、`attach`、`get_messages` | Java/native 运行时验证 |
| `mobile-mcp` | 设备、安装、启动、终止、元素、点击、输入、截图 | 手机操作和行为触发 |
| Reqable 服务 | `get_domains`、`list_requests`、`get_request`、`search_requests`、WebSocket 和 HAR 操作 | 网络样本和接口分析 |
| JEB | 类、方法、smali、交叉引用 | JADX 结果不清晰时的只读交叉验证 |
| Apktool 服务或 CLI | 解码、重建、Manifest、smali、资源、搜索和项目结构操作 | Manifest、资源和 smali 的修改与重建 |
| APK 签名工具 | 对齐、签名和最终验证 | 生成可安装的修改产物 |
| DEX 工具 | DEX/JAR/smali 转换和校验 | Apktool 不适合表达的专项处理，不作为默认步骤 |
| ADB | `install`、`install-multiple`、`shell am force-stop`、`shell monkey` 或显式 Activity 启动、`logcat` | 安装、冷启动、运行日志和 split APK 验收 |

工具表只是能力说明，具体参数以当前工具 schema 为准。发生命名差异时，以工具描述和输入结构确认语义，不创建自定义别名冒充真实工具。

Apktool 负责解码、项目文件操作和重建，不负责最终签名。修改时选择能够表达目标变更且引入无关差异最少的解码方式。构建默认不得无意开启调试属性；如果工具接口提供调试选项，应显式关闭，除非修改目标要求开启。

签名工具由当前环境和任务要求决定。无论选择何种实现，都必须保证必要的对齐发生在签名前、签名后不再修改 APK，并对最终产物执行签名和对齐验证。含未压缩 `.so` 时使用支持相应页对齐要求的工具和参数。

签名材料和密码不得写入技能、脚本、状态文件或日志。发现测试密钥或默认密钥不代表已获准使用，必须先确认密钥身份和用途。
