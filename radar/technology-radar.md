# Android Technology Radar

Last updated: 2026-09-14  
Source: `reports/weekly/android-technology-radar-2026-09-14.md`  
Mode: incremental vs `snapshots/weekly/2026-09-11.md`

本文件是活文档。每周由 `automation/android-radar-weekly` 覆盖更新。没有版本、成熟度或推荐变化的条目，不重写解释。

## Adopt

建议采用。

| Technology | Why | Since |
|---|---|---|
| Play Target API 36 | 2026-08-31 起上架阻断；延期仅到 2026-11-01 | 2026-09-10 |
| 16KB Page Size | 手机/平板 2027-02-01；Wear 2026-09-15 | 2026-09-10 |
| Android Studio Quail 4 | 当前稳定 IDE；内置 Android skills | 2026-09-10 |
| Configuration Cache | Isolated Projects 前置；40+ 模块仓非可选 | 2026-09-10 |
| Baseline + Startup Profile CI | 用 `Require` 门禁，不要手养 profile | 2026-09-10 |
| Android CLI + official skills | Agent 升 AGP / 迁 Nav3 / 写 AppFunction 的官方规程；Quail 4 已预装 | 2026-09-10 |
| Studio AQI Crash/Leak Agent | 唯一官方、就地、人在回路的 Crash/Leak 闭环 | 2026-09-10 |
| NDK r30 LTS | 有 native 时显式钉；AGP 默认仍是 28.2 | 2026-09-10 |
| Dagger / Hilt KSP | 文档盖章稳定（Dagger 2.60+ / KSP 2.3.9+）；新模块禁止 kapt | 2026-09-11 |
| compose-lints 1.6.0 | Slack 生产 Compose lint；不进 APK，直接接 CI | 2026-09-11 |
| R8 Analyzer + Play DEX 25% | 开了 minify ≠ 达标；Tinder 28%→50%，冷启动 -47%；分数进 CI | 2026-09-14 |
| Play Memory / Bitmap P90 看板 | 2027-02 按 RAM 档 + 进程态执法；先看见再专项 | 2026-09-14 |
| Benchmark 1.5.0 | 已稳定；`requireAot` / `requireMainThread` 默认 true | 2026-09-14 |
| AGP 9.4.0 + New DSL | 当前 9.x 稳定线；模块级 `newDsl.optOut`；DFM 1:1 | 2026-09-14 |

## Trial

建议 PoC。

| Technology | Why | Constraint |
|---|---|---|
| Gradle Isolated Projects | 大仓 Studio sync 约 1.9× | 仅本地/IDE；钉 9.7.1；禁止生产包 |
| Kotlin 2.4.20 | tooling release | 必须与 KSP/Hilt/Room/Compose 配对 |
| Compose 1.12.1 | UI 稳定线前进 | 非 breaking |
| Metro 1.4.3 | 编译税下降 50–80% 的报告；1.4.3 补 Hilt interop | 单 feature；Hilt 全家桶成本高 |
| ADK Kotlin 1.0 | 官方 Android/KMP Agent；main 已有 AppFunctionsToolset | 钉 1.0.1；等 1.0.2；不要自研编排 |
| Maestro MCP | 唯一能留下确定性 CI 资产的 UI Agent | 与 Journeys 二选一 |
| KuiklyUI 2.27 | Compose DSL + KSP；鸿蒙/跨端 | 仅有跨端 KPI 时嵌入，不整包替换 |
| AppFunctions alpha11 | 官方端上 MCP；样品 + ADK Toolset 对齐 | 只读函数；系统 Gemini 仍 EAP |
| android-profiler / Perfetto | 读 `.perfetto-trace` 出可复现 SQL | 只试分析；自动修+复测 Hold |

## Assess

持续关注。

| Technology | Why |
|---|---|
| Android 17 Beta | 内存限额、后台音频硬化；设备升级即生效 |
| Navigation3 1.2.0-rc01 | 稳定线 1.1.7 已可给新屏幕；1.2 跟 RC |
| KSP 2.3.12 | 自定义 processor / backing fields（Hilt/Dagger 路径已 Adopt） |
| AGP 10 plugin inventory | 现在列清单，避免发布窗口被插件卡住 |
| KMP default module split | 仅已有或计划 KMP 的仓 |
| Circuit 0.38 | Screen 不再 Parcelable；Parcelable breaking 未撤回 |
| Crashlytics MCP | Experimental；先值班机 |
| GitHub Agentic Workflows | 编译/依赖红灯自愈，先单个仓库 |
| Paparazzi 2.0-alpha05 | 修了 `--parallel cleanRecord` 竞态；等稳定再全量 |
| MNN 3.6.1 | RVV/FlashAttention 不是换栈；与 LiteRT-LM / ADK 选一条主线 |
| Remote Compose alpha19 | 官方 SDUI；活动/卡片可 spike；无 RC |
| Studio Rabbit 1 | 有 iOS/Flutter/RN 源工程才看；Canary |

## Hold

暂时不采用。

| Technology | Why |
|---|---|
| Isolated Projects / Gradle 9.8 RC 生产包 | 官方未背书 |
| Circuit/Metro 全量替换锁定 MVVM | 无平台压力 |
| Cloud Agent Instrumented/ANR | 模拟器未交付 |
| Jenkins + AI | 无 Android 一等闭环 |
| Tinker / Shadow / Atlas / AndFix / Robust | 热修复/插件化一代，不再是默认动态化 |
| Flipper / AffectedModuleDetector / ByteX | archived 或 Transform API 遗产 |
| ADK + MNN 双运行时 | 选一条主线 |
| AppFunctions + 系统 Gemini 同一生产里程碑 | 契约可共用；EAP 不能绑死迭代 |
| Remote Compose 进核心流程 | 仍 alpha |
| Kotlin Toolchain 替换 Gradle / ARouter snapshot | 无大仓落地；unpublished |

## Counts

| Ring | Count |
|---|---|
| Adopt | 14 |
| Trial | 9 |
| Assess | 12 |
| Hold | 10 |
