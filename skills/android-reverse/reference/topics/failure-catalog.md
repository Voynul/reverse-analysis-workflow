# 故障与反例索引

按症状查阅，不因匹配某行就停止任务、固定原因或执行修改。编号对应来源项目的 50 类经验，表中是候选与补证方向，不是当前目标结论。

| 编号 | 症状或误判 | 核对方向 / 专题 |
|---|---|---|
| P1 | 清理 META-INF 后启动异常 | 非签名运行资源，[修改验收](../patch-and-verify.md) |
| P2 | 字符串替换后 DEX 被拒绝 | 编码、引用与排序，[DEX 修改](dex-patching.md) |
| P3 | smali 往返表面正常但运行失败 | 重组差异、code item 与控制，[DEX 修改](dex-patching.md) |
| P4 | 重复重写后异常 | 输入身份、共享表和最终字节，[修改验收](../patch-and-verify.md) |
| P5 | 破坏接口后整个页面挂起 | 异常与回调链，[广告与配置](ads-remote-config.md) |
| P6 | 某功能修改影响无关业务 | 共享 helper 消费者，[DEX 修改](dex-patching.md) |
| P7 | 本地会员标志正常但功能失败 | 状态与真实授权，[账户](accounts-limits.md) |
| P8 | 本地数据修改后无栈异常 | schema、类型与边界，[运行数据](runtime-data.md) |
| P9 | 原包环境故障被归于补丁 | 原构建对照，[设备环境](device-environment.md) |
| P10 | 静态与运行结果矛盾 | 身份、路径、输入与条件，[证据](../evidence-and-renaming.md) |
| P11 | 当前设备有效，重装后失效 | 数据依赖与交付物，[运行数据](runtime-data.md) |
| P12 | Shell 成功但设备结果错误 | 宿主/设备展开与权限，[设备环境](device-environment.md) |
| P13 | 签名验证输出被误读 | 真实方案、目标平台与命令，[APK 工具](../tools/apk.md) |
| P14 | 相同大小 dump 被误当重复 | 内容哈希与来源，[脱壳](unpacking.md) |
| P15 | Frida 版本/API 问题被归于目标 | 客户端、服务端和 bridge，[Frida 工具](../tools/frida.md) |
| P16 | 局部 TLS 失败被归于修改 | 真实客户端与信任路径，[TLS](tls.md) |
| P17 | 自动化截图被当作全部证明 | 前台身份与底层证据，[运行触发](../mobile-automation.md) |
| P18 | 安装报告成功但构建未替换 | 包身份、最终文件及安装集合，[验收](../patch-and-verify.md) |
| P19 | 内部信号代替用户目标效果 | 实际行为与交付条件，[验收](../patch-and-verify.md) |
| P20 | 未捕获被写成不存在 | 采集健康和覆盖，[反分析](anti-analysis.md) |
| P21 | 多变量同时改变后错误归因 | 选择能区分假设的对照，[证据](../evidence-and-renaming.md) |
| P22 | 等待依赖人工动作却无期限轮询 | 明确等待条件与依赖，[工作状态](../workspace-state.md) |
| P23 | 编辑值反复恢复 | 内存、默认写入及远程同步，[运行数据](runtime-data.md) |
| P24 | 文件已变但运行没变 | 旧构建、缓存与加载副本，[验收](../patch-and-verify.md) |
| P25 | 搜索零命中被当删除 | 编码、格式和查询范围，[静态分析](../static-analysis.md) |
| P26 | 自建脚本错误变成目标结论 | 独立解析与控制，[证据](../evidence-and-renaming.md) |
| P27 | 重签后接口普遍失败 | 证书派生输入及其他上下文，[算法](../algorithm-validation.md) |
| P28 | 旧事件被当作新崩溃 | PID、时间及日志缓冲，[设备环境](device-environment.md) |
| P29 | 修改的静态数据非实际 UI 来源 | 缓存、配置与消费者，[广告与配置](ads-remote-config.md) |
| P30 | 对照无法区分假设却得出结论 | 输入/状态的区分力，[算法](../algorithm-validation.md) |
| P31 | 阻断退出后进程活着但冻结 | 持锁、自旋和语义，[native 终止](native-tamper.md) |
| P32 | 未解析 stub 就重定向 | 符号、调用约定与来源，[native](../native-analysis.md) |
| P33 | 半途解码停止却报告无调用 | 指令覆盖与边界，[DEX 修改](dex-patching.md) |
| P34 | 主动终止被当普通缺陷 | 信号、来源与原包对照，[native 终止](native-tamper.md) |
| P35 | 阻断一条终止路径就宣布通过 | 多重检查及业务继续，[native 终止](native-tamper.md) |
| P36 | 只信任受保护 ELF 节表 | 程序头和实际加载，[加载器](native-loader.md) |
| P37 | checksum/类错误被追到无关类 | 最终 DEX 完整性和运行解析，[DEX 修改](dex-patching.md) |
| P38 | 重打包后资源安装失败 | 压缩与实际对齐要求，[APK 工具](../tools/apk.md) |
| P39 | 只有数字安装错误就判断壳拒绝 | 对应平台与原始错误，[split](split-packages.md) |
| P40 | 截图不是目标应用 | 前台、安装器和权限窗口，[运行触发](../mobile-automation.md) |
| P41 | 改分支后方向与意图相反 | 条件、目标与两臂验证，[DEX 修改](dex-patching.md) |
| P42 | 解码错位后所有偏移仍被信任 | 格式表和指令边界，[DEX 修改](dex-patching.md) |
| P43 | 观察点命中却找不到参数 | 调用阶段、栈、对象和寄存器位置，[硬件观测](hardware-tracing.md) |
| P44 | 一个观察脚本故障影响其后全部探针 | 安装健康与消息链路，[反分析](anti-analysis.md) |
| P45 | 过滤 maps 破坏自己的加载 | 合法消费者和环境干预，[加载器](native-loader.md) |
| P46 | Java TLS Hook 无明文 | native/其他协议路径，[协议](protocols.md) |
| P47 | 两个工具对同一文件意见不一 | 版本、格式覆盖与独立样本，[静态分析](../static-analysis.md) |
| P48 | 目标运行正常但 SO 断点不绑定 | APK 内映射、地址空间及版本，[远程调试](remote-debugging.md) |
| P49 | 复现输出错误来自提取阶段 | 位宽、编码与状态对照，[算法](../algorithm-validation.md) |
| P50 | 看似自定义密码实际是可抵消包装 | 真实变换链和数据流，[协议](protocols.md) |

按题意选择检查，不强制逐行阅读。上游案例及未实测机制只作方法来源；具体判断仍使用当前任务的证据状态。
