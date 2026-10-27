# 经验专题路由

按问题选择经验，不按工具名决定经验范围。多个专题可以同时适用，索引不限制 Agent 的其他方法；普通任务只读取相关条目。工具操作独立见 [工具路由](tool-capabilities.md)。

## 侦察与代码定位

| 问题或线索 | 经验 |
|---|---|
| 目标身份、SDK、加载入口、运行时归属 | [包结构](package-recon.md) |
| Java/Kotlin、字符串、组件与调用链 | [静态分析](static-analysis.md) |
| Kotlin 注解、调试信息与候选原名 | [名称恢复](topics/kotlin-names.md) |
| 壳、按需恢复、内存 DEX、dump 质量 | [脱壳与载荷](topics/unpacking.md) |
| Java2C、JNI 下沉与交接 | [归属分流](package-recon.md)、[native](native-analysis.md) |
| 自定义容器、linker、重定位、SO dump | [加载器](topics/native-loader.md) |

## JS 与跨平台运行时

| 问题或线索 | 经验 |
|---|---|
| 字符串表、AST、控制流重写 | [JS AST](topics/js-ast.md) |
| JS 私有载荷、栈机/寄存器机与宿主状态 | [JSVMP](topics/jsvmp.md) |
| RN bundle、Hermes、JS/native 交接 | [React Native](react-native-hermes.md) |
| Dart snapshot、对象池、AOT 与平台通道 | [Flutter/Dart](flutter-dart.md) |
| Mono、IL2CPP、资源与受保护 metadata | [Unity/IL2CPP](unity-il2cpp.md) |
| APK 中的 Python、pyc、Pyarmor 类载荷 | [Python 载荷](topics/python-payload.md) |

## native 与观测

| 问题或线索 | 经验 |
|---|---|
| JNI、函数、类型、调用与数据流 | [native](native-analysis.md) |
| 参数、返回值、加载时机与运行调用栈 | [动态 Hook](dynamic-hook.md) |
| attach 后退出、零事件、检测与环境歧义 | [反分析](topics/anti-analysis.md) |
| 主动退出、自毁、完整性响应 | [native 终止](topics/native-tamper.md) |
| DBI、软件轨迹、平坦化、差分与缺失事件 | [native 跟踪](topics/native-tracing.md) |
| native/Dex VM、虚拟状态、IR、opcode 差分 | [VM 保护](vm-protection.md) |
| 只需要函数结果、模拟执行与原进程 RPC | [调用与模拟](topics/rpc-emulation.md) |
| 等待调试器、远程协议、映射内断点 | [远程调试](topics/remote-debugging.md) |

## 业务与数据

| 问题或线索 | 经验 |
|---|---|
| 广告、弹窗、服务端 UI 配置、重新启用 | [广告与配置](topics/ads-remote-config.md) |
| 登录、绑定、游客、会员、次数与权限归属 | [账户与限制](topics/accounts-limits.md) |
| 版本检查、强制升级、自更新与热更新 | [更新路径](topics/updates.md) |
| SharedPreferences、DataStore、MMKV、SQLite、回写 | [运行数据](topics/runtime-data.md) |
| 网络样本、接口字段与代码来源 | [网络分析](network-traffic.md) |
| TLS、锁定机制、信任链与功能局部失败 | [TLS](topics/tls.md) |
| Protobuf、gRPC、QUIC、长连接与编码体 | [协议](topics/protocols.md) |
| 请求签名、证书派生输入、算法复现 | [算法验证](algorithm-validation.md) |
| Binder、Intent、WebView bridge、SELinux、证明链 | [系统 IPC](topics/system-ipc.md) |

## 修改与交付

| 问题或线索 | 经验 |
|---|---|
| 修改声明、归档保留、对照、签名和行为验收 | [修改与验收](patch-and-verify.md) |
| DEX 指令/字符串、smali、方法重写及局部审计 | [DEX 修改](topics/dex-patching.md) |
| split、动态模块、统一签名与集合安装 | [多包集合](topics/split-packages.md) |
| 已修改包、额外组件、重签名与注入审计 | [第三方构建](topics/third-party-builds.md) |
| 用户允许模块交付或持久化 Hook | [模块交付](topics/module-delivery.md) |

## 设备与高级观测

| 问题或线索 | 经验 |
|---|---|
| 实际设备、进程 ABI、日志、Shell、网络与状态 | [环境诊断](topics/device-environment.md) |
| UI 操作、触发与可比较运行样本 | [运行触发](mobile-automation.md) |
| MT/APK MCP、Termux 等设备侧工作 | [设备侧工具经验](topics/on-device.md) |
| root 暴露、用户态/内核边界与注入原理 | [内核观测](topics/kernel-observation.md) |
| watchpoint、ETE/TRBE、SPE/BRBE 与符号化 | [硬件与差分](topics/hardware-tracing.md) |

## 证据、故障与维护

关键结论见 [证据与命名](evidence-and-renaming.md)。需要恢复任务时使用 [可选工作状态](workspace-state.md)，阶段判断参照 [工作关卡](workflow-gates.md)，均不要求简单任务创建文件。

[故障目录](topics/failure-catalog.md) 提供按症状查询的入口，[案例](topics/cases.md) 保留成功、失败与反例的使用方式，不以命中某条经验自动停止或替用户改变目标。

来源核对和脚本处置在 [移植清单](../maintenance/migration.json)；它是维护记录，不是每个任务需要读取的材料。上游 67 份参考的可复用内容已分别整合，不要求安装或访问来源仓库。
