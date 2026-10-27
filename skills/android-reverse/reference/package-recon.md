# APK 结构与逻辑归属

## 目标

在深入分析或修改前判断关键逻辑实际所在层级，避免长期在错误代码层搜索。结论分为 `Observed`、`Inferred`、`Hypothesis` 或 `Refuted`，并记录证据。

## 归属矩阵

| 层级 | 常见证据 | 后续路由 |
|---|---|---|
| DEX | 目标组件、类、字符串、调用链和分支位于 classes*.dex | `jadx-headless`、JEB、smali、Frida Java Hook |
| 资源/配置 | Manifest、XML、assets、原始资源或本地配置控制行为 | 资源读取、差异检查、运行验证 |
| native/JNI | `native` 方法、`System.loadLibrary`、JNI 导出或 `RegisterNatives` | `idalib-mcp`、Frida Native Hook |
| React Native/Hermes | RN 加载入口、JS bundle、Hermes 字节码或相关引擎库 | 确认实际加载产物，再按需读取 `react-native-hermes.md` |
| Flutter/Dart | Flutter 引擎、Dart snapshot、业务库及 Flutter assets | 按需读取 `flutter-dart.md`，确认 Dart 与平台侧的业务边界 |
| Unity/Mono/IL2CPP | UnityPlayer、托管程序集或 native 与 metadata 产物 | 按需读取 `unity-il2cpp.md`，区分后端及实际加载版本 |
| WebView/JavaScript | WebView 加载 URL、assets 中脚本、JS bridge | Java/JS bridge、资源和网络联合分析 |
| 服务端/远程配置 | 本地只存在请求、响应消费或配置入口，决策值来自网络 | 抓包、Hook、配置时序和服务端边界说明 |

运行时归属与保护方式可以叠加。发现私有字节码、虚拟状态和解释器分发的关联线索时，可再读取 `vm-protection.md`；不把 VMP 视为与 Flutter、Unity 或 JNI 互斥的类型。

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

## `native` 声明增多时的分流

方法没有 DEX 实现不等于它正在等待解密。可以结合目标方法的声明、注册关系和加载前后证据区分：

| 候选形态 | 有助于区分的证据 | 分析方向 |
|---|---|---|
| 普通 JNI 或局部下沉 | 目标方法关联 native 实现，其余相关业务仍可在 DEX 中追踪 | 聚焦 Java/JNI 交接和对应 native 函数 |
| Java2C 等代码翻译 | 成组业务方法转为 `native`，且有对应的编译实现或注册关系支持 | 以 DEX 声明作为索引，追踪 `.so` 内的实现和回调 Java 的路径 |
| 抽取或按需恢复 | 目标方法在加载或调用前后出现代码恢复、替换或额外载荷 | 定位恢复时机，再决定如何取得可用代码 |

这些形态可以并存，按目标方法判断。native 比例、壳名称、`JNI_OnLoad` 或空符号搜索都不能单独确定形态；反编译失败也不能单独证明存在 VMP。尚未确认时保留候选，不套用固定比例或由静态外观断言运行时一定没有 DEX。

方法参考：`apk-reverse-codeberg-mirror` 中 `apk-reverse` 的 Java2C/JNI 分流思路；仅吸收多证据判别，不继承其阈值或确定性处置。

## 输出要求

归属结论至少包含：

- 主要控制层和辅助层。
- 入口证据与跨层边界。
- 当前置信度和未排除的替代解释。
- 下一步分析或修改应该作用的文件、模块或运行时节点。

如果证据显示关键决策位于服务端，只能说明客户端可观察和可控制的边界，不把客户端修改描述为已改变服务端逻辑。
