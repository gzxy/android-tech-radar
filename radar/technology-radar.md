# Android Technology Radar

Last updated: 2026-09-10  
Source: `reports/weekly/android-technology-radar-2026-09-10.md`  
Mode: first weekly baseline

本文件是活文档。每周由 `automation/android-radar-weekly` 覆盖更新。没有版本、成熟度或推荐变化的条目，不重写解释。

## Adopt

建议采用。

| Technology | Why | Since |
|---|---|---|
| Play Target API 36 | 2026-08-31 起上架阻断；延期仅到 2026-11-01 | 2026-09-10 |
| 16KB Page Size | 2027-02-01 起 target 35+ 64-bit 更新必须对齐 | 2026-09-10 |
| Android Studio Quail 4 | 当前稳定 IDE；内置 Android skills | 2026-09-10 |
| Configuration Cache | Isolated Projects 前置；40+ 模块仓非可选 | 2026-09-10 |
| Baseline + Startup Profile CI | 用 `Require` 门禁，不要手养 profile | 2026-09-10 |
| Android CLI + official skills | Agent 升 AGP / 迁 Nav3 的官方规程 | 2026-09-10 |
| Studio AQI Crash/Leak Agent | 唯一官方、就地、人在回路的 Crash/Leak 闭环 | 2026-09-10 |
| NDK r30 LTS | 有 native 时显式钉；AGP 默认仍是 28.2 | 2026-09-10 |

## Trial

建议 PoC。

| Technology | Why | Constraint |
|---|---|---|
| AGP 9.4.0 + New DSL / built-in Kotlin | AGP 10 最后准备窗口 | 先非主干；清 `applicationVariants` |
| Gradle Isolated Projects | 大仓 Studio sync 约 1.9× | 仅本地/IDE；禁止生产包 |
| Kotlin 2.4.20 | tooling release | 必须与 KSP/Hilt/Room/Compose 配对 |
| Compose 1.12.1 | UI 稳定线前进 | 非 breaking |
| Benchmark 1.5.0 | 重新校准启动/滚动基线 | `requireAot` 默认 true |
| R8 analyzer + keepRules | 不打包就能迭代 keep | 随 AGP 9.3/9.4 |
| Metro 1.0 | 编译税下降 50–80% 的报告 | 单 feature；Hilt 全家桶成本高 |
| ADK Kotlin 1.0 | 官方 Android/KMP Agent 运行时 | 不要自研编排；不要双运行时 |
| Maestro MCP | 唯一能留下确定性 CI 资产的 UI Agent | 与 Journeys 二选一 |
| KuiklyUI 2.27 | Compose DSL + KSP；鸿蒙/跨端 | 仅有跨端 KPI 时嵌入，不整包替换 |

## Assess

持续关注。

| Technology | Why |
|---|---|
| Android 17 Beta | 内存限额、后台音频硬化；设备升级即生效 |
| Navigation3 1.2.0-rc01 | 稳定线 1.1.7 已可给新屏幕；1.2 跟 RC |
| KSP 2.3.12 | 自定义 processor / backing fields |
| AGP 10 plugin inventory | 现在列清单，避免发布窗口被插件卡住 |
| KMP default module split | 仅已有或计划 KMP 的仓 |
| Circuit 0.38 | Screen 不再 Parcelable；已用必须升级 |
| Crashlytics MCP | Experimental；先值班机 |
| GitHub Agentic Workflows | 编译/依赖红灯自愈，先单个仓库 |
| Paparazzi 2.0-alpha05 | 组件库可 PoC；等稳定再全量 |
| MNN 3.6.1 | 与 LiteRT-LM / ADK 对比，选一条主线 |

## Hold

暂时不采用。

| Technology | Why |
|---|---|
| Isolated Projects 生产包 | 官方未背书 |
| Circuit/Metro 全量替换锁定 MVVM | 无平台压力 |
| Cloud Agent Instrumented/ANR | 模拟器未交付 |
| Jenkins + AI | 无 Android 一等闭环 |
| Tinker / Shadow / Atlas / AndFix / Robust | 热修复/插件化一代，不再是默认动态化 |
| Flipper / AffectedModuleDetector / ByteX | archived 或 Transform API 遗产 |
| ADK + MNN 双运行时 | 选一条主线 |

## Counts

| Ring | Count |
|---|---|
| Adopt | 8 |
| Trial | 10 |
| Assess | 10 |
| Hold | 7 |
