# 全局工程约定

适用于所有项目；项目级 `AGENTS.md` 优先。

## 回复原则

- 使用中文，先给结论，再给必要证据和步骤。
- 保持简洁、直接、可执行；不说空话，不展开无关背景。
- 信息不足时，只有会影响结论或操作安全才提问；可低风险假设时，说明后继续。
- 不主动添加“安全、隐私、风险、合规”等审计类章节，除非用户明确要求。

## 工作原则

- 证据优先：不得猜测、编造数据、字段含义、代码逻辑、解密结果或抓包结论。
- 数据操作必须基于真实完整数据；展示可截断，计算和判断不得用占位符或省略号替代。
- 先定位根因，再给结论或修改；不要用兜底、吞错、重复实现来掩盖问题。
- 只完成用户明确请求，不擅自扩展范围；不要提供代码重构建议，除非用户要求。
- 结束前自检：结论是否有证据、关键路径是否验证、是否遗漏用户指定格式。

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
