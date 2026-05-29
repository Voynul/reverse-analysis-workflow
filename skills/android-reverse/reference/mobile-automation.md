# 手机自动化规范

## 适用场景

- 启动、停止、冷启动、热启动 APP。
- 点击、滑动、输入、返回、切换前后台。
- 触发广告展示、登录、授权弹窗、页面跳转、网络请求。
- 截图确认 UI 状态。
- 配合 Frida 和 Reqable 批量采集运行时数据。

## 标准流程

1. 选择目标设备。
2. 确认目标 APP 包名。
3. 根据任务选择冷启动、热启动或指定页面操作。
4. 每次关键操作后等待界面稳定。
5. 需要证据时截图或记录 UI 元素。
6. 读取 Frida 日志和 Reqable 请求，与操作时间对齐。

## 常用操作速查

| 任务 | 工具 |
|---|---|
| 列出设备 | `mobile_list_available_devices` |
| 列出 APP | `mobile_list_apps` |
| 启动 APP | `mobile_launch_app` |
| 终止 APP | `mobile_terminate_app` |
| 安装 APK | `mobile_install_app` |
| 截图 | `mobile_take_screenshot` |
| 保存截图 | `mobile_save_screenshot` |
| 获取界面元素 | `mobile_list_elements_on_screen` |
| 点击坐标 | `mobile_click_on_screen_at_coordinates` |
| 双击 | `mobile_double_tap_on_screen` |
| 长按 | `mobile_long_press_on_screen_at_coordinates` |
| 滑动 | `mobile_swipe_on_screen` |
| 输入文字 | `mobile_type_keys` |
| 系统按键 | `mobile_press_button` |
| 打开 URL | `mobile_open_url` |

## 自动化模板

冷启动并触发页面：

```text
1. 终止 APP，确保完全停止。
2. 如需 Hook，先 spawn 或 attach。
3. 启动 APP。
4. 等待首页或开屏加载。
5. 获取界面元素或截图。
6. 点击目标按钮、Tab 或广告位。
7. 记录操作时间、截图和 Hook/抓包日志。
```

循环采集：

```text
1. 冷启动。
2. 等待预加载。
3. 浏览几个页面。
4. 切到后台。
5. 等待指定时间。
6. 回到前台。
7. 读取 Hook 日志和网络请求。
8. 重复 N 轮。
```

## 操作建议

- 优先用元素文本或描述定位；WebView 无法列出元素时使用坐标。
- `mobile_list_elements_on_screen` 返回的坐标通常是元素中心点。
- 操作之间等待 1 到 3 秒，复杂页面等待更久。
- 每次点击、滑动、输入都记录目的。
- 复杂流程写成可重复步骤，便于复现。
- 截图只证明 UI 状态，不直接证明代码逻辑；需要结合 Hook、抓包或反编译证据。
