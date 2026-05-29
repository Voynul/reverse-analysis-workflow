# 网络数据分析规范

## 适用场景

- 获取 HTTP/HTTPS 请求和响应。
- 分析域名、接口、请求方法、状态码、请求体、响应体。
- 分析 WebSocket 消息。
- 确认加密字段、压缩字段、签名字段和业务字段。
- 把抓包样本与静态代码、Hook 日志对应起来。

## 标准流程

1. 获取域名列表，区分业务域名、广告域名、统计域名、资源域名和第三方 SDK 域名。
2. 按关键词、域名、状态码、方法筛选请求。
3. 对关键请求读取完整 header、query、body、response。
4. 同一 URL 多次出现时优先选正常响应样本；如果样本差异影响结论，应保留多个样本。
5. 将字段含义回链到代码、Hook 日志或解密结果。
6. 对加密字段记录算法定位、输入输出、解密代码和验证结果。

## 常用操作速查

| 任务 | 工具 |
|---|---|
| 查看所有域名 | `mcp__reqable__get_domains` |
| 列出请求 | `mcp__reqable__list_requests` |
| 获取请求详情 | `mcp__reqable__get_request` |
| 搜索请求 | `mcp__reqable__search_requests` |
| 分析 API 结构 | `mcp__reqable__analyze_api` |
| WebSocket 会话 | `mcp__reqable__list_websocket_sessions` |
| 分析 WebSocket | `mcp__reqable__analyze_websocket_session` |
| 搜索 WebSocket 消息 | `mcp__reqable__search_websocket_messages` |
| 生成请求代码 | `mcp__reqable__generate_code` |
| 健康检查 | `mcp__reqable__health_report` |
| 导入 HAR | `mcp__reqable__import_har` |

## 分析模板

分析广告或统计请求：

```text
1. 获取全部域名。
2. 搜索 ad、track、impression、bid、event、config 等关键词。
3. 按目标域名查看请求列表。
4. 读取关键请求详情。
5. 对照静态代码或 Hook 日志确认字段来源。
```

分析 WebSocket：

```text
1. 列出 WebSocket 会话。
2. 选择目标会话并分析消息方向和类型。
3. 搜索关键字段或明文片段。
4. 与 UI 操作时间和 Hook 日志对齐。
```

## 证据要求

每个关键接口至少记录：

- 完整 URL。
- 请求时机。
- 请求方法和状态码。
- 关键请求字段和白话含义。
- 关键响应字段和白话含义。
- 来源证据：抓包编号、Hook 日志、代码位置或解密结果。

## 注意事项

- 不要用占位 JSON 冒充真实请求或响应。
- HTTPS 解密失败时，只能说明当前可见的域名、路径或状态码。
- 如果通过 Frida 绕过证书校验后才获得样本，报告中说明样本采集条件。
- 抓包只能证明网络层观察到的样本，不自动证明字段生成逻辑；字段来源需要回链代码或 Hook。
