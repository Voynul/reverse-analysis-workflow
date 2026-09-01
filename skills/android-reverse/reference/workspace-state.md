# Android Reverse 工作状态规范

## 定位

`.android-reverse/` 是 `android-reverse` 技能存放内部状态和中间产物的默认工作目录，不是项目正式交付目录，也不能改变外部调用者已有的文件规划。

文件存放优先级从高到低为：

1. 用户明确指定的路径。
2. 外部项目 plan、`项目规则.md` 或上层调用技能指定的路径。
3. 报告类技能规定的输出位置。
4. `android-reverse` 默认的 `.android-reverse/` 内部目录。

外部已经规划的报告、脚本、证据、命名文件或其他产物继续写入其指定位置。不要将它们迁移、复制或重定向到 `.android-reverse/`；需要使用时只在内部状态中记录引用路径。

只有能够可靠确定项目根目录时才创建 `.android-reverse/`。无法确定时，不要在任意当前目录创建工作区；暂时在当前 Codex 任务上下文维护状态，并说明状态无法跨任务持久化。

## 推荐结构

    .android-reverse/
    ├── analysis-state.md
    └── targets/
        └── <包名>_<版本号>_<APK文件名>/
            ├── rename.md
            ├── notes.md
            ├── scripts/
            └── evidence/

`analysis-state.md` 用于恢复目标确认、工具选择和资源所有权。目标目录名中的 Windows 非法字符应替换为安全分隔符。目标目录中的其他文件按需创建，不要求目录或文件全部存在。

## analysis-state.md

至少记录以下状态：

- 当前活动 APK 的绝对路径。
- 包名、`versionName` 和 `versionCode`。
- 用户是否已经确认目标。
- 当前选择的 JADX 模式及确认状态。
- 正式报告策略：`required`、`not-required` 或 `pending`。
- 报告策略的作用域：当前 APK 或用户明确指定的项目级默认值。
- 外部 plan、项目规则或上层技能指定的文件路径引用。
- Agent 可管理的 IDA session/database 所有权、用途和关闭策略。
- 当前目标状态：分析中、已完成或已中止。

样本身份只使用 APK 绝对路径、包名、`versionName` 和 `versionCode`，不要求计算文件哈希。

## 正式报告策略

使用 `android-reverse` 前确认当前 APK 是否需要正式报告：

- 用户已经明确说明时直接记录，不重复询问。
- 用户未说明时先询问。
- `not-required` 表示不自动调用 `analysis-report` 或 `final-report`，不表示禁止生成其他文档。
- 用户可以随时修改报告策略；修改后立即更新状态。
- 用户切换 APK 后重新确认。只有用户明确声明时才把选择作为项目级默认值。

## 目标切换

一次分析任务只处理一个 APK，不并行分析多个 APK。

下列情况视为用户主动切换：

- 用户明确说切换到另一个 APK。
- 用户提供新的 APK 绝对路径并要求开始新的分析。

GUI 中检测到 APK 变化但用户没有说明时，不视为授权；先输出新 APK 的身份信息并等待确认。用户只提到另一个包名、版本或文件名作为比较对象时，也不要自动切换。

切换前：

1. 将旧目标标记为已完成或已中止。
2. 保存 Agent 判断需要复用的轻量中间材料。
3. 不因 APK 切换关闭无关联的 IDA session。
4. 为新目标重新确认正式报告策略、APK 身份和工具模式。
5. 创建新的目标工作目录，避免中间产物混用。

## IDA session 状态

IDA session 与 APK 没有强制对应关系。仅记录 Agent 能明确识别的 session：

| 字段 | 说明 |
|---|---|
| session/database | 工具返回的标识 |
| binary_path | 目标二进制绝对路径 |
| opened_by | `agent` 或 `user/external` |
| related_apk | 可选的 APK 路径或包名 |
| purpose | JNI 链路、独立 so 分析等 |
| close_policy | 分支完成后关闭或保持打开 |

Agent 只自动关闭自己创建且关闭策略明确的 session。用户或外部管理的 session 不因 APK 切换而关闭。

## 清理

- 默认保留 `analysis-state.md`、命名记录、分析笔记、脚本和关键证据。
- 清理可重新生成的大体积临时文件、重复二进制和解压目录。
- 不删除用户提供的 APK、so、正式报告或用户明确要求保留的文件。
- 用户要求清理时，先解析并列出准确目标范围，再执行删除。
