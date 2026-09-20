# APK 结构与逻辑归属

## 目标

在深入分析或修改前判断关键逻辑实际所在层级，避免长期在错误代码层搜索。结论分为 `Observed`、`Inferred`、`Hypothesis` 或 `Refuted`，并记录证据。

## 归属矩阵

| 层级 | 常见证据 | 后续路由 |
|---|---|---|
| DEX | 目标组件、类、字符串、调用链和分支位于 classes*.dex | `jadx-headless`、JEB、smali、Frida Java Hook |
| 资源/配置 | Manifest、XML、assets、原始资源或本地配置控制行为 | 资源读取、差异检查、运行验证 |
| native/JNI | `native` 方法、`System.loadLibrary`、JNI 导出或 `RegisterNatives` | `idalib-mcp`、Frida Native Hook |
| Flutter | Flutter 引擎、Dart AOT 库、Flutter assets | Flutter/Dart AOT 专项分析，不把 Java 壳当业务主体 |
| Unity/IL2CPP | UnityPlayer、global-metadata、libil2cpp | Unity/IL2CPP 专项分析 |
| WebView/JavaScript | WebView 加载 URL、assets 中脚本、JS bridge | Java/JS bridge、资源和网络联合分析 |
| 服务端/远程配置 | 本地只存在请求、响应消费或配置入口，决策值来自网络 | 抓包、Hook、配置时序和服务端边界说明 |

## 快速侦察

1. 查看 Manifest、入口组件、权限、Application 和启动 Activity。
2. 查看 DEX 数量、ABI、so、assets、资源和已知框架标记。
3. 搜索目标行为相关字符串、URL、错误信息和配置键。
4. 追踪 Java 到 JNI、WebView、网络或远程配置边界。
5. 必要时用一次最小运行触发确认真实加载模块和请求时序。

## 加固与动态加载

出现以下信号时，不应只依赖静态 DEX：

- 入口代码极少，业务类在运行后出现。
- 自定义 ClassLoader、DexClassLoader、内存 DEX 或加密资源加载。
- 壳特征、异常 Application、早期 native 初始化或动态解密。
- 同一行为在静态代码中只有桥接入口，没有实现。

此时记录壳层、加载时机、落地或内存载荷证据，并决定使用 Frida、dex dump、native 跟踪或运行时调用栈补证。

## 输出要求

归属结论至少包含：

- 主要控制层和辅助层。
- 入口证据与跨层边界。
- 当前置信度和未排除的替代解释。
- 下一步分析或修改应该作用的文件、模块或运行时节点。

如果证据显示关键决策位于服务端，只能说明客户端可观察和可控制的边界，不把客户端修改描述为已改变服务端逻辑。
