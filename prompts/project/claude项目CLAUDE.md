# 工程约定

## 核心原则

1. **禁止假设与虚构** — 不得假设、猜测、编造不存在的数据、代码逻辑、字段含义、解密结果等。所有结论必须有实际证据支撑（反编译代码、抓包数据、Hook 日志等）。
2. **数据操作必须基于真实数据** — 所有加解密、解析、格式化等数据操作必须以实际抓取/提取到的数据为准，不允许用占位符（如 `<regex>`、`...`）替代真实数据后再分析。若数据量过大可截取前段展示，但分析计算必须基于完整真实数据。
3. **混淆类/方法/变量必须重命名** — 所有混淆符号在引用前必须先根据功能重命名（规则见静态分析→混淆类重命名），重命名记录写入 `rename.md`。报告中一律使用 `原名→新名` 格式引用，**严禁**单独使用原始混淆名。

## 重要提醒
- **不要**提供代码重构、修复建议（那是开发的工作）
- **不要**提及安全、隐私、风险等审计内容
- **不要**添加"安全与隐私考虑"等章节

### 名称俗语化

**核心理念**：行业术语、技术名词、英文缩写、内部黑话会提高普通读者的理解成本。输出时应主动将这类词替换为更口语化、更直白、更简短的说法，让读者不用具备行业或技术背景也能看懂。

执行规则：

1. 将专业词改成日常说法。
2. 优先解释"它有什么用"，而不是保留原始名称。
3. 不用另一个专业词解释专业词。
4. 改写后要短、准、直白，适合放在标题、小节名、按钮、列表项中。
5. 无法替换的专业词，应加上白话解释，例如：Token（文字片段）。

**自检标准**：如果非专业读者第一次看到也能大致理解，就符合要求；如果还需要搜索、猜测或具备行业背景，必须继续改写。


### 分析重点

分析本 APK (`com.open.web.ai.browser`) 时，优先聚焦**自建广告聚合 SDK**，避免过度深入公开聚合平台。

**重点关注（自建SDK）：**
- `com.openmediation.sdk` 及其内部所有类 — 自建聚合 SDK 核心
- 混淆包 `M8`、`ka`、`na`、`ma`、`oa`、`pa`、`ea`、`R8`、`S2`、`B3`、`A3`、`J2`、`Lb`、`T7`、`K8`、`N9` 等 — 自建广告逻辑
- 广告预加载策略、缓存管理、竞价/瀑布流调度、频控、UMP 交互、远程配置
- `BaseApplication`、`MainActivity`、`StartOpenAdActivity`、`InsertAdActivity` 等宿主层广告入口

**不必深入研究（公开聚合）：**
- `com.anythink.*` (TopOn) — 只确认接入方式和广告源列表即可
- `com.tradplus.*` (TradPlus) — 只确认接入方式即可
- `com.google.android.gms.ads.*` (AdMob) — 只关注被自建 SDK 调用的接口
- `com.applovin.*`、`com.vungle.*`、`com.mbridge.*`、`com.bytedance.*`、`com.facebook.*`、`sg.bigo.*` — 广告源 SDK，只关注被自建 SDK 适配层调用的接口

**参考文件：**

- `rename.md` — 混淆类/方法重命名映射表
- `result/analyze.md` — 广告聚合平台分析报告
- `result/network-analysis-report.md` — 网络协议分析报告
- `result/bidding-analysis.md` — 竞价/比价策略分析报告
- `result/preload-analysis.md` — 预加载策略分析报告
- `result/risk-control-analysis.md` — 风控策略分析报告
- `result/UMP_time-analysis.md` — UMP Consent 冷启动时序分析报告
- `result/cloaking-analysis.md` — Cloaking 策略分析报告
- `result/data-collection-analysis.md` — 数据采集与上报分析报告
- `result/delivery-strategy-analysis.md` — 投放行为策略分析报告
- `result/decrypt_jwd2.py` — jwd2 解密脚本
- `result/hook_startup_flow.js` — 启动流程 Frida Hook 脚本
- `result/preload_hook.js` — 预加载 Frida Hook 脚本
- `.omc/skills/android-re-tools/SKILL.md` — 逆向工具链 skill

---

## Tool Use Instructions

1. Always use relative paths from the workspace root (e.g., `src/index.js`). Do NOT use absolute paths or Windows-style backslashes (`\`), use forward slashes (`/`).
2. When using `str_replace_editor`:
- The `old_string` MUST match the file contents EXACTLY, including all spaces, indentation, empty lines, and line endings.
- Do not use placeholders (like `// ... rest of the code`) in the `old_string` or `new_string`.
- Ensure the output JSON block is fully completed and never truncated.
3. If you fail to edit a file due to string mismatches, use the `bash` tool to inspect or use standard CLI tools as a fallback.

## Large File Handling & Batch Writing (大文件与分批写入规范)

1. **Minimal Replace Range (最小化修改范围):** 
- Never rewrite an entire large file (e.g., >100 lines) to make small changes. 
- Keep the `old_string` and `new_string` block in the editor tool as small and precise as possible (ideally targeting under 20-30 lines of code per edit).
2. **Chunked Writing for Large Data (大数据/长代码分批写入):**
- If you need to generate a very large file, a long dataset, or extensive boilerplate code, DO NOT attempt to write it all in a single tool call.
- Split the writing task into logical steps/phases. Write the basic skeleton first, then incrementally insert modules/data chunks using multiple sequential `str_replace_editor` calls.
- After writing each chunk, verify the file's current state before proceeding to the next chunk.
3. **Use Scripts as an Alternative (巧用脚本生成大文件):**
- For writing very large repetitive data (e.g., 1000 lines of JSON mock data, database seeds, or long logs), instead of writing it directly, write a small Node/Python/Shell script to programmatically generate or append that file, then execute it via the `bash` tool.
4. **Targeted Reading (精准读取):**
- For large files (>500 lines), avoid reading the entire file at once. Use search/grep tools, or specify line ranges if the tool allows, to locate the target code before reading or editing.


## 静态分析

所有分析报告（如 `analyze.md`、`preload-analysis.md` 等）必须遵守以下规范。

### 语言

- 正文使用**中文**撰写
- 类名、方法名、变量名、包名、文件路径、技术名词、公司/组织/产品名保留原文
- 示例: `M8.AdManager.initOpenMediationSdk`、`com.openmediation.sdk`、`Waterfall`、`eCPM`

### 写作风格

- **去术语化** — 行业术语、技术缩写、内部代号会增加理解成本。输出时应主动替换为更直白、口语化的说法
  - 写"服务器可以远程关闭所有广告"，不写"`mTntpeIzbw` 全局总开关"
  - 写"今天广告次数用完了"，不写"`QqBrYcjqIQ` 超额永久禁用"
  - 写"隐私授权弹窗"，不写"UMP Consent"
  - 写"每展示一次预估能赚多少钱"，不写"eCPM"
- **每点配总结** — 每个小节或关键论据末尾附一句话总结，让读者快速抓住要点
  - 示例: "总结：服务器有一个一键关停的能力，可以远程关闭APP里所有的广告。"
- **不存在也要列出来** — 分析过程中搜索过但确认不存在的策略/机制，应在报告中单独列表说明，含搜索关键词和搜索范围，避免读者误以为是遗漏而非确实不存在

### 代码引用

- 每个关键论据必须附上对应的反编译代码片段
- 代码使用 ```java 代码块包裹，并添加中文注释说明关键逻辑
- 注释要简洁，点明核心逻辑即可
- 每个代码片段必须标注来源位置，格式: `包名.原始名→重命名名.方法名`
- 混淆类/方法/变量引用必须使用 `原名→新名` 格式，严禁单独使用原始混淆名
- 示例: `M8.t→AdManager.initOpenMediationSdk()`、`ea.y→AdFrequencyManager.checkFrequency()`

### 图表规范

所有分析报告中涉及逻辑、流程、关系的内容必须配图。

**图表类型选择**：
- 调用链/依赖关系/决策分支 → `flowchart TD`
- 数据流转/来源链路 → `flowchart TD`（可用 `subgraph` 分组）
- 时序交互（网络请求/回调） → `sequenceDiagram`
- 状态切换 → `stateDiagram-v2`
- 所有图表需编号（如 `图 1`、`表 2`），正文中引用

**流程图节点命名规范**：
- 节点文字必须使用简短的**中文描述**，说明该步骤在做什么，严禁使用原始方法名/类名
- 正确: `"读取本地缓存最高出价"`、`"按出价金额降序排列"`
- 错误: `"getHighestBidPrice()"`、`"BiddingComparator(6) revenue DESC"`
- 如果方法名本身有业务含义（如 `checkFrequency`），需翻译为中文后使用

**关键决策点代码佐证**：
- 流程图中涉及分支判断、开关控制的节点，必须在正文中附上对应的**原始反编译代码**
- 使读者能对照代码验证流程的正确性
- 示例: Consent 流程图中的"远程隐私开关"节点 → 正文附 `R8.M→b` 中 `getConfigBool("khgdqndwefgdrg")` 的判断代码

### 文件命名

- 分析报告按主题命名：`<topic>-analysis.md`
  - `analyze.md` — 广告 SDK/聚合平台概览
  - `preload-analysis.md` — 预加载策略分析
  - `bidding-analysis.md` — 竞价策略分析
  - `network-analysis-report.md` — 网络协议分析

### 混淆类重命名（强制）

所有自建 SDK 混淆类/方法/变量在引用前**必须先重命名**，由核心原则第 3 条强制要求。

**记录格式**: 以 `原始名→重命名名` 写入 `rename.md` 对应表格

**引用格式**: 报告中一律使用 `包名.原始名→重命名名`（如 `ea.y→AdFrequencyManager`、`ka.u3→GaConfigManager`），严禁单独使用原始混淆名

**重命名优先级规则**：

1. **`.source` 优先** — 如果 smali 中 `.source` 指令的值不是 `"SourceFile"` 或其他自动生成名（如 `"R8.java"`、`"unknown"`），则直接使用 `.source` 的值作为类名。
   ```
   示例: .source "AdManager"  →  类重命名为 AdManager
   示例: .source "SourceFile"  →  跳过此规则，按规则 2 处理
   ```

2. **`toString()` 推断** — 如果类存在 `toString()` 方法且返回了有意义的描述字符串，则：
   - 用返回字符串中的类名作为重命名名
   - `this.xxx` 引用的字段名改为对应含义名
   ```java
   // 原始
   public final class w {
       public String a;
       public HashMap b;
       public final String toString() {
           return "AdPositionConfig(id=" + this.a + ", settings=" + this.b + ')';
       }
   }
   // 重命名: w → AdPositionConfig, a → id, b → settings
   ```

3. **功能推断** — 以上规则均不适用时，根据类的实际功能命名

**Frida Hook 注意**: 脚本中必须使用原始混淆类名，JADX 重命名仅影响 IDE 显示。

---

## 网络分析

网络协议分析报告（如 `network-analysis-report.md`）除遵守静态分析规范外，还需遵守以下规则。

### 字段映射表

- 所有混淆字段名必须建立 **代码字段名 → 业务含义** 映射表，至少包含 `字段名`、`数据类型`、`业务含义`、`所属 URL`、`代码来源` 五列
- 字段含义必须关联其所属的**完整 URL**，同一字段名在不同 API 中含义不同时分开列出

### 请求/响应示例

- 每个 API 端点需展示**完整的请求和响应 JSON**，**必须标注完整的请求 URL**
- JSON 中关键字段添加行内注释说明含义，请求和响应分别展示

### 数据采样

- **同一条 URL 只分析最先出现的一条请求/响应数据**，避免重复数据膨胀
- 选取请求时优先 `status=200` 的正常响应，统计类数据不受此限制

### 加密字段解密过程

- 加密字段必须展示完整解密过程: **代码定位 → 算法分析 → Python 解密代码 → 解密结果验证**
- Python 解密代码使用 Python REPL 执行，列出解密后的完整数据结构

### 网络调用时序图

- 使用 `sequenceDiagram` 绘制客户端-服务端交互时序，包含 APP 层 → SDK 层 → HTTP 客户端 → 服务端 → 响应处理层
- 节点命名和代码佐证要求同上"图表规范"

### API 端点汇总表

- 每个域名下列出全部 API 端点，含请求量、方法、用途
