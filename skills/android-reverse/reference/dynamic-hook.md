# 动态 Hook 规范

## 适用场景

- 获取方法参数、返回值、异常和真实分支。
- 获取加密前明文、解密后明文、签名材料、序列化对象。
- 验证静态分析推断是否在运行时成立。
- 追踪 Java 到 native 的入参和返回值。
- 配合抓包确认请求字段来源。
- 必要时修改返回值观察行为变化，但结论中必须标注这是主动干预后的结果。

## 执行步骤

1. 先用静态分析确定 Hook 目标，包括原始类名、方法名、重载签名和调用时机。
2. Frida 脚本必须使用运行时原始名称；JADX/JEB 重命名只用于阅读。
3. Hook 时记录时间、线程、参数、返回值、异常和调用栈。
4. 输出建议使用 JSONL，便于后续筛选和报告引用。
5. 需要触发 UI 路径时，用 mobile-mcp 自动操作。
6. 需要确认网络影响时，同步使用 reqable MCP 抓包。

## Frida 连接流程

每次动态 Hook 前先确认 Frida Server 状态：

1. 使用 Frida MCP 检测 frida-server 是否运行。
2. 如果未运行，优先使用 Frida MCP 启动。
3. 如果 MCP 无法自动启动，通过 ADB 进入设备后手动启动。
4. 启动后再次检测连接状态。
5. 如果 MCP 仍不可用，但设备上已有 frida-server 进程，可回退 Frida CLI 直连。

手动启动常见流程：

```bash
adb shell
dbg
cd /data/local/tmp
./florida-server-16.5.9
```

注意：

- `dbg` 用于进入 root 权限环境；不要使用 `su -c` 或 `dbg -c` 的单行形式。
- `florida-server-16.5.9` 是重命名后的 frida-server 名称，实际文件名以设备为准。
- 如果连接失败，应提示用户开启或检查 Frida 服务，不得把连接失败当作运行时无对应逻辑。

## 常用操作速查

| 操作 | 工具 |
|---|---|
| 检测状态 | `mcp__frida__check_frida_status` |
| 启动服务 | `mcp__frida__start_frida_server` |
| 停止服务 | `mcp__frida__stop_frida_server` |
| 附加进程 | `mcp__frida__attach` |
| 启动 APP 并附加 | `mcp__frida__spawn` |
| 列出应用 | `mcp__frida__list_applications` |
| 获取前台应用 | `mcp__frida__get_frontmost_application` |
| 获取 Hook 输出 | `mcp__frida__get_messages` |

## 日志格式

推荐 JSONL：

```json
{"ts":"2026-01-01T00:00:00.000Z","type":"HOOK","class":"原始类名","method":"原始方法名","args":{},"ret":{},"stack":"可选"}
```

对大对象只截取报告展示片段，但原始日志应保留完整数据。不要把示例日志当成真实证据。

## Java Hook 模板

```javascript
Java.perform(function() {
  var TargetClass = Java.use("com.example.TargetClass");
  TargetClass.targetMethod.implementation = function(arg1, arg2) {
    console.log("[+] targetMethod args=" + arg1 + "," + arg2);
    var result = this.targetMethod(arg1, arg2);
    console.log("[+] targetMethod ret=" + result);
    return result;
  };
});
```

## 注意事项

- Hook 重载方法时必须写清参数类型。
- Frida 使用原始混淆名，报告使用 `原名→新名`。
- 修改返回值会改变行为，必须把原始结果和干预结果分开记录。
- Hook 日志只能证明运行时观察到的路径，不自动证明所有分支。
