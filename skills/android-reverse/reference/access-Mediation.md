# APK 广告聚合平台分析报告

**应用包名:** `com.open.web.ai.browser`  
**版本:** 1.8.7 (versionCode: 10108007)  
**分析日期:** 2026-05-11

---

## 一、概览

该 APK 共接入了 **4 个广告聚合/中介平台**，覆盖了 **6 个主要广告源 SDK**。

| 聚合平台 | 类型 | 角色 |
|---------|------|------|
| TopOn (AnyThink) | 主流聚合平台 | **主聚合层** |
| TradPlus | 主流聚合平台 | 辅助聚合层 |
| Google AdMob | 自有聚合能力 | 聚合层 / 广告源 |
| AppLovin MAX | 自有聚合能力 | SDK 自带聚合框架 |

---

## 二、直接接入的广告源 SDK

以下广告 SDK 作为独立 SDK 直接存在于 APK 中（不依赖于聚合平台的 adapter 桥接）：

| 广告源 | SDK 包名 | 说明 |
|--------|---------|------|
| **Google AdMob** | `com.google.android.gms.ads` | Google 移动广告 |
| **AppLovin** | `com.applovin.sdk` / `com.applovin.mediation` | AppLovin 广告平台 (含 MAX) |
| **Mintegral (MBridge)** | `com.mbridge.msdk` | Mintegral 移动广告 |
| **Pangle (穿山甲)** | `com.bytedance.sdk.openadsdk` | 字节跳动广告平台 |
| **Vungle (Liftoff)** | `com.vungle.ads` | Liftoff 视频广告 |
| **Bigo Ads** | `sg.bigo.ads` | Bigo 广告平台 |
| **Facebook Audience Network** | `com.facebook.ads` | Meta 广告网络 |

---

## 三、各聚合平台接入的广告源详情

### 3.1 TopOn (AnyThink) — 主聚合平台

TopOn 是当前 APK 的主要聚合平台，adapter 类数量最多、覆盖面最广。

**核心包路径:** `com.anythink.*`

| 序号 | 广告源 | Adapter 类 | 说明 |
|------|--------|-----------|------|
| 1 | Google AdMob | `com.anythink.network.admob.AdmobATAdapter` | Google 移动广告 |
| 2 | Google AdMob | `com.anythink.network.admob.GoogleAdATAdapter` | Google 广告 (另一适配形式) |
| 3 | Google AdX | `com.anythink.network.adx.AdxATAdapter` | Google Ad Exchange |
| 4 | Bigo Ads | `com.anythink.network.bigo.BigoATAdapter` | Bigo 广告 |
| 5 | Directly (直投) | `com.anythink.network.directly.DirectlyATAdapter` | 直投广告 (自有直客) |
| 6 | Facebook (Meta) | `com.anythink.network.facebook.FacebookATAdapter` | Meta 广告网络 |
| 7 | MyOffer (自有) | `com.anythink.network.myoffer.MyOfferATAdapter` | TopOn 自有广告源 |
| 8 | OnlineApi | `com.anythink.network.onlineapi.OnlineApiATAdapter` | 在线 API 广告 |
| 9 | Pangle (穿山甲) | `com.anythink.network.pangle.PangleATAdapter` | 字节跳动 Pangle |
| 10 | Toutiao (头条) | `com.anythink.network.toutiao.TTATAdapter` | 字节跳动头条 (旧版 Pangle 兼容) |
| 11 | Vungle (Liftoff) | `com.anythink.network.vungle.VungleATAdapter` | Liftoff 视频广告 |

> **TopOn 合计接入 10 个广告源** (AdMob/AdX 算作 2 个渠道，Toutiao/Pangle 作为 2 个独立 channel)。

---

### 3.2 TradPlus — 辅助聚合平台

TradPlus 是辅助聚合平台，APK 中可见的核心 adapter 类较少。

**核心包路径:** `com.tradplus.ads.*`

| 序号 | 广告源 | 可见 Adapter 类 | 说明 |
|------|--------|-----------|------|
| 1 | Vungle (Liftoff) | `com.tradplus.ads.vungle.VungleTradPlusBanner` | Liftoff Banner 广告 |

> **说明:** TradPlus 支持通过服务端配置动态加载广告源，无需在 APK 中编译所有 adapter。APK 中包含核心 SDK 和基础 adapter，其余广告源可通过服务端下发实现对接。

**TradPlus SDK 核心类:**
- `com.tradplus.ads.open.TradPlusSdk` — SDK 入口
- `com.tradplus.ads.mgr.TradPlusMgr` — 管理类
- `com.tradplus.ads.core.AdMediationManager` — 广告中介管理
- `com.tradplus.ads.base.network.TPOpenResponse.AdsourceImpConfigBean` — 广告源配置
- `com.tradplus.ads.base.network.TPOpenResponse.AdsourceRequestConfig` — 广告源请求配置

---

### 3.3 Google AdMob Mediation — Google 聚合层

Google AdMob 具备自身的聚合中介能力，以下为 AdMob 接入的广告源 adapter：

**核心包路径:** `com.google.ads.mediation.*`

| 序号 | 广告源 | Adapter 类 | 说明 |
|------|--------|-----------|------|
| 1 | AppLovin | `com.google.ads.mediation.applovin.AppLovinMediationAdapter` | AppLovin 广告 |
| 2 | Facebook (Meta) | `com.google.ads.mediation.facebook.FacebookMediationAdapter` | Meta 广告网络 |
| 3 | Mintegral | `com.google.ads.mediation.mintegral.MintegralMediationAdapter` | Mintegral 广告 |
| 4 | Pangle (穿山甲) | `com.google.ads.mediation.pangle.PangleMediationAdapter` | 字节跳动 Pangle |
| 5 | Vungle (Liftoff) | `com.google.ads.mediation.vungle.VungleMediationAdapter` | Liftoff 视频广告 |

> **Google AdMob Mediation 合计接入 5 个第三方广告源。**

---

### 3.4 AppLovin MAX — SDK 自带聚合框架

AppLovin SDK 内置了 MAX 聚合框架，但在此 APK 中仅发现其自身的核心 adapter，未发现接入其他广告源的具体 adapter 类。

**核心包路径:** `com.applovin.mediation.*`

| 序号 | 组件 | 类 | 说明 |
|------|------|-----|------|
| 1 | AppLovin 自身 | `com.applovin.mediation.ApplovinAdapter` | AppLovin SDK 自身广告 |
| 2 | MAX 框架 | `com.applovin.mediation.adapter.MaxAdapter` | MAX 聚合框架接口 |
| 3 | MAX 参数 | `com.applovin.mediation.adapter.parameters.MaxAdapterParameters` | MAX adapter 参数 |

> **说明:** AppLovin MAX 在此 APK 中主要作为 AppLovin SDK 自带的聚合框架存在，未检测到加载其他广告源的 MAX adapter。其他聚合平台（如 TopOn、AdMob）通过自己的 adapter 接入 AppLovin 作为广告源。

---

## 四、广告源 SDK 接入关系汇总

以下表格展示每个广告源 SDK 被哪些聚合平台作为广告源接入：

| 广告源 SDK | TopOn | TradPlus | AdMob Mediation | AppLovin MAX |
|-----------|-------|----------|-----------------|--------------|
| Google AdMob | ✅ | — | — (自身) | — |
| Google AdX | ✅ | — | — | — |
| AppLovin | — | — | ✅ | ✅ (自身) |
| Mintegral | — | — | ✅ | — |
| Pangle (穿山甲) | ✅ | — | ✅ | — |
| Toutiao (头条) | ✅ | — | — | — |
| Vungle (Liftoff) | ✅ | ✅ | ✅ | — |
| Bigo Ads | ✅ | — | — | — |
| Facebook (Meta) | ✅ | — | ✅ | — |
| Directly (直投) | ✅ | — | — | — |
| MyOffer (自有) | ✅ | — | — | — |
| OnlineApi | ✅ | — | — | — |

---

## 五、广告聚合关系图

```
┌─────────────────────────────────────────────────────────┐
│                   APK: com.open.web.ai.browser           │
└─────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   TopOn       │    │   TradPlus    │    │  AdMob        │
│  (主聚合平台)  │    │  (辅助聚合)    │    │  Google 聚合   │
└───────────────┘    └───────────────┘    └───────────────┘
  │  │  │  │  │  │       │                  │  │  │  │  │
  │  │  │  │  │  │       │                  │  │  │  │  │
  ▼  ▼  ▼  ▼  ▼  ▼       ▼                  ▼  ▼  ▼  ▼  ▼
┌──────────────────────────────────────────────────────────┐
│  广告源 SDK (Ad Sources)                                 │
│  ┌────────┬────────┬──────────┬────────┬────────┬──────┐│
│  │AdMob   │AppLovin│Mintegral │Pangle  │Vungle  │Bigo  ││
│  │AdX     │        │          │Toutiao │        │      ││
│  │Facebook│        │          │        │        │      ││
│  │Directly│        │          │        │        │      ││
│  │MyOffer │        │          │        │        │      ││
│  │Online  │        │          │        │        │      ││
│  │  API   │        │          │        │        │      ││
│  └────────┴────────┴──────────┴────────┴────────┴──────┘│
└──────────────────────────────────────────────────────────┘
```

---

## 六、Omid SDK（广告可见性监测）

APK 中还包含了多个 Omid SDK 库，用于广告可见性监测 (Open Measurement)：

| Omid SDK | 关联平台 |
|----------|---------|
| `com.iab.omid.library.applovin` | AppLovin |
| `com.iab.omid.library.bigosg` | Bigo |
| `com.iab.omid.library.bytedance2` | Pangle (字节跳动) |
| `com.iab.omid.library.mmadbridge` | Mintegral/MBridge |
| `com.iab.omid.library.toponad` | TopOn (AnyThink) |
| `com.iab.omid.library.tradplus` | TradPlus |
| `com.iab.omid.library.vungle` | Vungle |

> **总结:** 该 APK 使用了 **TopOn 作为主聚合平台**（接入 10 个广告源渠道），**TradPlus 作为辅助聚合**（接入 Vungle），同时 Google AdMob 自身作为聚合层接入 5 个广告源。AppLovin MAX 框架存在但主要用于自有广告。共覆盖 Google AdMob/AdX、AppLovin、Mintegral、Pangle/Toutiao、Vungle、Bigo、Facebook/Meta 等 7 大类广告源 SDK。
