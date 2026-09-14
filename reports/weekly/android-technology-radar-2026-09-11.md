# Android Technology Radar

日期：2026-09-11

周期：相对 `snapshots/weekly/2026-09-10.md` / `watchlist/weekly.md` 的增量周报。  
本周新日报只有 `open-source`（2026-09-11）。`android-official` / `engineering` / `ai-android` 仍停在 2026-09-10，与周副本字节一致，不重写未变结论。

## 1. Executive Summary

本周 Android 工程最值得关注的不是又一批版本号，而是开源监控补上的三条官方轨道：

1. **Google 把「App 当成端上 MCP Server」写成了官方路径。** `android/appfunctions`（189★，基线漏收）+ Jetpack `1.0.0-alpha10` + `android/skills` 里的 `device-ai/appfunctions`。文档 2026-09-08 更新：AppFunctions = MCP tool 的 Android 等价物，Android 16+。Gemini 对接仍是 EAP——现在做的是函数注册和契约，不是等联调再设计 API。
2. **进程内 Agent 和系统级 Tool 是两条线。** ADK Kotlin 仍是 1.0.1，但 main 已补 MCP reject 保活和 `Plugin.onRunError`。AppFunctions 让系统 Agent 调进 App；ADK 让 App 自己跑 Agent。不要揉成一个「大 AI 项目」。
3. **Dagger 正式改口：KSP 已稳定。** 不是新 release（仍是 2.60.1），是开发者指南 + CI：Dagger 2.60+ / KSP 2.3.9+ 起 KSP 为稳定路径。叠加 09-09 的 KSP 2.3.12，kapt→KSP 不再是「等等看」。
4. **上架与工具链窗口没有变化，仍在咬人。** Play target 36（延期到 2026-11-01）、16KB（2027-02-01）、AGP 9.4→10、Isolated Projects 本地 PoC——官方/工程监控本周无新日报，执行优先级不变。
5. **国内大厂没有新发版。** Kuikly 仍 2.27.0，Lynx 仍 4.1.0。值得改动作的只有：MNN 去掉硬编码 STS / 遥测并补 Qwen3-TTS decode；Lynx develop 上的 TransferView 不要追。

## 2. Top 10 Changes

| Technology | Category | Source | What Changed | Impact | Recommendation |
|---|---|---|---|---|---|
| AppFunctions（端上 MCP） | Official / AI | open-source | 样品仓首次入库；文档定义 AppFunctions = 移动 MCP；alpha10 + 官方 Skill | 有助理/系统集成 KPI 的 App 现在就能注册只读函数 | Trial（与 ADK 拆开） |
| Dagger / Hilt KSP | Official / Build | open-source | 文档宣布 KSP 稳定（2.60+ / 2.3.9+） | 新模块禁止 kapt 的理由已经足够 | Adopt |
| ADK Kotlin 1.0.1+ | AI / OSS | open-source | main：MCP reject 保活、`onRunError`、unknown-tool 回主线 | 生产失败路径在补，但未打 1.0.2 | Trial（钉 1.0.1，等 1.0.2） |
| compose-lints 1.6.0 | Engineering | open-source | 基线漏收的 Slack 生产 Compose lint | 稳定性 / slot / modifier 误用可进 CI，不进 APK | Adopt |
| MNN 3.6.1 HEAD | Domestic / AI | open-source | 去 STS/遥测；Qwen3-TTS KV-cache decode | 已用工具脚本的团队有安全债；端侧语音进同一引擎 | Assess（跟 main 换脚本；TTS 另开，勿双运行时） |
| Paparazzi main | Testing | open-source | 过滤 `HideFromAccessibility`；删除库内 synthetic WindowInsets | 已跑 a11y 截图的模块 legend 可能变干净，不是业务 UI 变了 | Assess |
| Circuit 工具链 | Architecture | open-source | 当天跟上 Compose 1.12.1 / Benchmark 1.5.0 | 大厂样板 24h 吸收官方补丁；**不是又一次 0.38 breaking** | Assess（已用则对齐这两包） |
| Lynx develop | Domestic OSS | open-source | TransferView 所有权 API 出现后，DevTool/iOS 提交被回滚 | 嵌入式宿主 API 在长，主干不稳 | Trial*（钉 4.1.0，等 4.2） |
| dsh-kuikly-expert / AnimaX | Domestic OSS | open-source | 腾讯 DeepSeek Kuikly skill；Lynx 自研 Lottie/Alpha 引擎 | 生态信号，不是业务排期 | 观察，不进雷达主环 |
| Play 36 / 16KB / AGP 10 | Official | android-official（无新日报） | 相对上周快照无 Version/Signal/Rec 变化 | 仍是发布阻断与工具链窗口 | Adopt / Trial（结论不变） |

## 3. Domestic Big Tech Open Source

本周无 P0/P1 新版本号。热修复 / 插件化继续沉寂。华为 / 百度 / 小米 / 快手 / 网易 / 京东再扫一轮，仍没有可迁入大型 Android 工程的新开源。

### Tencent

- **KuiklyUI 仍是 2.27.0。** HEAD 只是 OHOS 拷贝目录和 CDN 地址。Compose DSL 正式发版、Roadmap 上的 MCP Server 都还没到。
- **新观察：`Tencent-TDS/dsh-kuikly-expert`（13★）。** 2026-08 一次性提交，把四条 Kuikly skill 打成 DeepSeek Harness 插件。说明 TDS 在同时喂 Cursor/官方 Skills 和 DeepSeek 两套 Agent。只观察，不排期。
- **KuiklyUI-AI / MMKV / libpag / Hippy：** 无版本变化。libpag 修了 PAGX 导出滤镜，不影响 Android 宿主接入。

### Alibaba / Ant Group

- **MNN 3.6.1 未发版，main 有两类高信号提交。** 安全：去掉工具链硬编码 STS、关闭遥测——用官方转换/调优脚本的团队应跟 main。能力：Qwen3-TTS talker / code-predictor 的 KV-cache decode，并修乱码。端侧语音开始进同一推理栈。
- ARouter / SoloPi：无新变化。interceptor 修复仍是遗产续命。

### ByteDance

- **Lynx 仍是 4.1.0。** develop 上出现 Android `TransferView` 所有权/生命周期 API，随后同一夜回滚了 DevTool CDPResponder 和 iOS 异步 UI。**钉 4.1.0，4.2（路线图 2026-10）前不要跟 develop。**
- **新观察：`lynx-family/animax`（30★，1.1.0）。** Lynx 自己的 C++ Lottie / Alpha Video 引擎。已上 Lynx 的团队有意义；纯 Compose 继续用 Lottie Android / libpag。
- btrace / CodeLocator / BlockFramework：无新版本。

### Meituan / Kuaishou / Others

- Logan / KOOM / 一代热修复：无复活。
- 小米 MACE 继续被 MNN / LiteRT 甩开。

## 4. Android Official

本周 `android-official` **无新日报**，与 `reports/daily/android-official-2026-09-10.md` 字节一致。执行结论不变：

- Play target 36：2026-08-31 起强制，延期窗口到 **2026-11-01**。
- 16KB：2027-02-01 起 target 35+ 的 64-bit 更新必须 ELF 对齐。
- 工具链地板：Studio Quail 4 + AGP 9.4.0 + Kotlin 2.4.20 + NDK r30 + KSP 2.3.12。
- Android 17 Beta 4.1：内存限额 / 后台音频硬化，设备升级即生效。

开源侧唯一叠加到官方面的新证据：Dagger 文档把 KSP 标成稳定；`android/skills` 已含 AppFunctions 四段生命周期 skill。这两条改变「怎么用官方工具」，不改变版本号。

## 5. Architecture

无新架构框架发版。Metro 1.0、Navigation 3 稳定线 1.1.7、Circuit 0.38 Parcelable breaking、KMP 默认模块拆分——相对上周快照 Rec 不变。

本周只补一条工程证据：**Circuit 在 24 小时内吃下 Compose 1.12.1 和 Benchmark 1.5.0。** 这是样板仓跟官方补丁的速度，不是又一次 Circuit API 断裂。已用 Circuit 的工程对齐这两包；新模块 PoC 条件不变。**Circuit 全量替换锁定 MVVM：仍 Hold。**

Dagger KSP 稳定改变的是 DI 工具链，不是换 DI 框架。新模块禁止 kapt；旧 Hilt 模块按批次迁，不必为了 KSP 去换 Metro。

## 6. Engineering Productivity

`engineering` 本周无新日报。Isolated Projects（仅本地/IDE）、AGP 9.4 / New DSL / built-in Kotlin、Configuration Cache——结论与 2026-09-10 相同，不占篇幅。

本周新增、立刻能做、不必 PoC：

- **`slackhq/compose-lints` 1.6.0：** Slack 生产 Compose lint，正在加强 modifier / slot 复用的控制流分析。Lint 依赖，不进 APK。接到现有 Lint / CI，看一周噪音再调 baseline。
- **Dagger/Hilt kapt→KSP：** 开一个模块级迁移 PR，装上 `android/skills`，不要让 Agent 自由改 annotation processor。

## 7. Performance

官方性能 API / Baseline / Benchmark 默认值本周无新日报。Benchmark 1.5.0 `requireAot=true`、16KB 镜像回归、Startup Profile CI——执行优先级不变。

开源侧只影响已接入团队：

- **Paparazzi：** a11y legend 对齐 Compose `HideFromAccessibility`；库不再提供 synthetic WindowInsets fixture。已上 2.0-alpha 的模块预期 legend 变干净；**不要在库里造 WindowInsets。**
- **MNN TTS：** 若已有端侧模型，可加一项 Qwen3-TTS 延迟对比。不是全员性能课题。
- **AnimaX：** 只对已上 Lynx 的动画路径有意义。

## 8. AI + Android

`ai-android` 本周无新日报。Crash AQI / Leak Agent / Maestro MCP / Cloud Agent 模拟器未交付——闭环判断不变。

开源侧把「SDK + Skill + MCP」从口号写成了**三条官方轨道**：

| 轨道 | 仓库 | 做什么 | 本周动作 |
|---|---|---|---|
| 进程内 Agent | `google/adk-kotlin` 1.0.1 | App 自己跑模型、调 `@Tool` / MCP Toolset | 继续 PoC；把 MCP 拒绝和未知 tool 写成测试；**等 1.0.2 再升生产依赖** |
| 系统级 Tool | AppFunctions + `android/appfunctions` | App 被 Gemini / 系统 Agent 调用 | 有助理 KPI 则立刻做 2–3 个只读 `@AppFunction` + `adb shell cmd app_function` |
| 怎么写这两套 | `android/skills`（含 AppFunctions skill） | 发现功能 → 生成实现 → 优化 KDoc → ADB 调试 | 装 skill，不要让模型自由写 manifest |

2026 下半年评估「我们要不要做 App 内 AI」，先问清楚是 **App 里跑 Agent**，还是 **让系统 Agent 跑进 App**。两套 API、两套权限、两个 PoC。

## 9. Watchlist Diff

相对 `watchlist/weekly.md`（2026-09-10）与 `snapshots/weekly/2026-09-10.md`。

### Added

进入周雷达决策面：

- **AppFunctions**（Trial）— 官方端上 MCP；样品仓 + Jetpack alpha10 + Skill。
- **Dagger/Hilt KSP**（Adopt）— 文档盖章稳定；新模块禁止 kapt。
- **compose-lints 1.6.0**（Adopt）— Slack 生产 Compose lint，直接接 CI。
- **AppFunctions + ADK 揉成一个里程碑**（Hold）— 两条线不要绑死。

领域 Watchlist 新增、但**不进雷达主环**（观察）：

- `Tencent-TDS/dsh-kuikly-expert`
- `lynx-family/animax`

### Updated

Version / Signal 变、Rec 不变：

- **ADK Kotlin：** 1.0.1 之后 main 超前（MCP reject 保活 / `onRunError`）。Rec 仍 Trial。
- **android/skills：** 确认含 AppFunctions 四段 skill。Rec 仍 Adopt。
- **MNN：** 去 STS/遥测 + Qwen3-TTS decode。Rec 仍 Assess。
- **Paparazzi：** a11y hidden 过滤；去掉 synthetic insets。Rec 仍 Assess。
- **Circuit：** 对齐 Compose 1.12.1 / Benchmark 1.5.0。Rec 仍 Assess。
- **Lynx：** TransferView 出现在 develop 并伴随回滚。Rec 仍条件 Trial，钉 4.1.0。

官方 / 工程 / AI 其余条目：Version / Signal / Rec 均未变，不重写。

### Downgraded

无新增降级。热修复 / 插件化 / Flipper / ByteX 维持 Hold。

### Removed

无。无新增 archived。不从周雷达推荐面再删条目。

## 10. PoC Candidates

最多 5 个。本周用新信号换掉「Metro 单模块」（Metro Rec 仍 Trial，但不是本 24h 最高优先级）。

### 1. AppFunctions 只读函数

```text
Technology
Jetpack AppFunctions 1.0.0-alpha10 + android/appfunctions + android/skills device-ai/appfunctions

Problem
系统助理要调用 App 里已经存在的业务（查订单 / 建草稿），而不是再做一个聊天 WebView，也不是把整棵 UI 交给截图 Agent。

Expected Benefit
在 Gemini EAP 打开之前先把函数契约、权限（EXECUTE_APP_FUNCTIONS）和 KDoc 测完；避免联调窗口才设计 API。

PoC Scope
独立 :appfunctions 模块，compileSdk 36，KSP。2 个 @AppFunction（搜索 + 创建草稿）+ adb shell cmd app_function 自测 + 官方 skill 走一遍 KDoc。不要承诺「下个版本就能被 Gemini 调到」。不要和 ADK 做成同一个里程碑。

Estimated Difficulty
中。权限模型是系统级，不是普通互调。

Success Criteria
两个函数能被 Testing Agent / ADB 调通；Skill 生成的 manifest 可审；不引入第二套推理运行时。
```

### 2. Gradle Isolated Projects（本地）

```text
Technology
Gradle Isolated Projects（9.7 incubating）

Problem
Configuration Cache 只能跳过「配置未变」的重复构建。IDE sync、改 build logic、第一次 CI 配置仍要配完所有 project。

Expected Benefit
大仓 Android Studio sync 下降 ≥20%（官方万级模块约 1.9×）。

PoC Scope
前置：Configuration Cache 从 warn→fail。打开 org.gradle.isolated-projects=true（或 diagnostics），量 Studio sync 与 --dry-run 配置时间，记录不兼容插件。不用于 release 流水线。

Estimated Difficulty
中。第三方插件是主阻力。

Success Criteria
sync 下降 ≥20%，且无静默错误；产出不兼容插件清单。
```

### 3. AGP 9.4 / AGP 10 就绪审计

```text
Technology
AGP 9.4.0 + android.newDsl=true + android.builtInKotlin=true

Problem
AGP 10 将删除 applicationVariants / Transform / newDsl 与 builtInKotlin opt-out。等到 10.0 再迁会集中爆 ClassCastException。

Expected Benefit
把发布阻断变成可排期的插件债；同时拿到 API 37 与 R8 analyzer。

PoC Scope
非主干升 AGP 9.4.0 + Gradle 9.7.1。全仓打开 New DSL。CI 扫 applicationVariants / BaseExtension / kotlin-android。每个第三方 Gradle 插件标「已兼容 / 可升级 / 必须替换」。

Estimated Difficulty
中高。DFM flavor 1:1 与自定义插件是硬点。

Success Criteria
零 opt-out 能编过 debug；警告清单可在一个迭代内清完。
```

### 4. Google ADK for Kotlin 1.0（继续，不重写）

```text
Technology
google/adk-kotlin 1.0.1

Problem
商业 Android 应用要把 Agent 做进进程：工具调用、session、端侧隐私、云端复杂推理。内部自研编排会和官方 API 重复。

Expected Benefit
同一套 LlmAgent 接 LiteRT-LM 或 Firebase AI；KSP @Tool 类型安全；Room session 可测试。1.0.1 之后的失败路径说明 1.0.2 会很快。

PoC Scope
继续上周范围。今天不要为 unreleased main 改 API。把 MCP 拒绝和未知 tool 写成测试夹具，等 1.0.2。不要上 ML Kit beta 的 tool calling。

Estimated Difficulty
中。KSP 进现有模块即可。

Success Criteria
工具调用可单测；未知 tool / MCP reject 走容错；不引入第二套推理运行时。
```

### 5. Crash Agent 闭环

```text
Technology
Android Studio AQI Fix with AI + Firebase Crashlytics MCP

Problem
On-call 前 30–90 分钟耗在「打开控制台 + 对 stacktrace + 搜代码」。ANR/竞态仍要人盯，但 NPE/生命周期类 Crash 是重复劳动。

Expected Benefit
把分诊压到「批准 diff」；issue 留下 note。

PoC Scope
选 3 个已有 mapping 的高用户数 Crashlytics issue。路径 A：Studio AQI。路径 B：Cursor/Claude + /crashlytics:connect。

Estimated Difficulty
低。Experimental MCP 限制在排障，不写进 SLA。

Success Criteria
2/3 给出可编译 diff；至少 1 个能被现有单测或手工复现验证；Agent 在 issue 留下 note。
```

明确不做的 PoC：Cloud Agent 里启动模拟器、ANR 自动修复、Jenkins AI、同时上 ADK + MNN、把 AppFunctions 和 ADK 绑成一个里程碑、追 Lynx develop / TransferView、dsh-kuikly-expert / animax 独立业务排期。compose-lints 和 Dagger KSP **不必 PoC**，直接接 CI / 开迁移 PR。

## 11. Technology Radar

未变条目不重写解释。本周环位变化见各条「Since / 变化」。

### Adopt

- Play Target API 36（含 edge-to-edge / Predictive Back / 大屏回归）
- 16KB Page Size 合规（native / 第三方 so 盘点 + 16KB 镜像回归）
- Android Studio Quail 4
- Configuration Cache（Isolated Projects 前置，40+ 模块仓非可选）
- Baseline Profile + Startup Profile CI（`BaselineProfileMode.Require`）
- Android CLI + `android/skills` / `kotlin-agent-skills`（本周确认含 AppFunctions skill）
- Studio AQI Fix with AI + LeakCanary Fix with Agent（人在回路的 Crash/Leak）
- NDK r30 LTS（有 native 时显式钉版本，不要吃 AGP 默认 28.2）
- **Dagger / Hilt KSP**（新模块禁止 kapt；旧模块分批。Dagger 2.60+ / KSP 2.3.9+）
- **compose-lints 1.6.0**（Slack 生产 Compose lint，直接接 CI）

### Trial

- AGP 9.4.0 + `android.newDsl=true` + `android.builtInKotlin=true`（AGP 10 最后窗口）
- Gradle Isolated Projects（仅本地 / IDE sync / 非生产 CI）
- Kotlin 2.4.20（必须与 KSP / Hilt / Room / Compose Compiler 配对）
- Jetpack Compose 1.12.1
- Benchmark 1.5.0（独立分支，预期 `requireAot` 让旧用例失败）
- AGP R8 analyzer + keepRules source set
- Metro 1.0（单 feature，验证编译时间与 Hilt interop）
- Google ADK for Kotlin 1.0（钉 1.0.1；MCP 失败写成测试；等 1.0.2）
- Maestro MCP（主路径冒烟，留下可进 CI 的 YAML；与 Journeys 二选一）
- KuiklyUI 2.27（仅已有鸿蒙/跨端 KPI 的团队做嵌入式 View PoC）
- **AppFunctions 1.0.0-alpha10**（只读函数 + ADB 自测；与 ADK 拆开；Gemini 仍 EAP）

### Assess

- Android 17 Beta（内存限额、后台音频、本地网络——设备升级即生效）
- Navigation3 1.2.0-rc01（稳定线 1.1.7 已可 Adopt 新屏幕；1.2 跟 RC）
- KSP 2.3.12（自定义 processor / backing fields；Hilt/Dagger 路径已升到 Adopt）
- AGP 10.0 第三方插件盘点
- KMP 默认模块拆分（仅已有或计划 KMP 的仓）
- Slack Circuit 0.38（已用必须升级；本周只是工具链对齐）
- Firebase Crashlytics MCP（Experimental，先值班机）
- GitHub Agentic Workflows（编译/依赖红灯自愈，先单个仓库）
- Paparazzi 2.0.0-alpha05（本周 a11y 修复降低误报，不是 2.0 稳定信号）
- Alibaba MNN 3.6.1（跟 main 换工具脚本；TTS 另开对比；勿与 ADK 双栈）

### Hold

- Isolated Projects 打生产包（官方未背书）
- Circuit / Metro 全量替换已锁定的 MVVM + Hilt
- Cursor Cloud Agent 做 Instrumented / ANR（模拟器未交付）
- Jenkins + AI 插件当 Android 闭环
- 新项目选用 Tinker / Shadow / Atlas / AndFix / Robust / Walle
- 新项目选用 Flipper / AffectedModuleDetector / ByteX
- 同时上 ADK + MNN 双推理运行时
- **把 AppFunctions 和 ADK 揉成一个里程碑**

## 12. Next Week

下周最值得继续跟踪的方向：

1. **AppFunctions 契约窗口** — 只读函数能否在 ADB / Testing Agent 上跑通；Gemini EAP 是否有公开进展。
2. **ADK Kotlin 1.0.2** — MCP reject / `onRunError` 是否进稳定包；不要提前改生产依赖。
3. **Play target 36 与 16KB 执行进度** — 延期窗口只到 2026-11-01；native 依赖对齐清单是否闭环。
4. **AGP 9.4 升级与 Isolated Projects 本地数字** — 非主干是否编过；Studio sync 与不兼容插件是否有第一手数据。
5. **Kuikly Compose DSL 正式发版 / Lynx 4.2** — 都还没到。不到点不要把 develop HEAD 当发版。

无新官方数字、推荐不变的 Watchlist：**不要重写本章。**

## 13. Sources

一手资料与本周监控报告：

- `reports/daily/open-source-2026-09-11.md`（本周唯一新日报）
- `reports/daily/open-source-2026-09-10.md`
- `reports/daily/android-official-2026-09-10.md`（无增量）
- `reports/daily/engineering-2026-09-10.md`（无增量）
- `reports/daily/ai-android-2026-09-10.md`（无增量）
- `reports/weekly/android-technology-radar-2026-09-10.md`
- https://developer.android.com/ai/appfunctions （Last updated 2026-09-08）
- https://developer.android.com/ai/appfunctions/add-appfunctions
- https://developer.android.com/jetpack/androidx/releases/appfunctions
- https://github.com/android/appfunctions
- https://github.com/android/skills/tree/main/device-ai/appfunctions
- https://github.com/google/adk-kotlin （`245a74a2b3` MCP reject；`77aea89604` onRunError；`93c4beb889` unknown tool）
- https://github.com/google/dagger/commit/099c3c8f40 （KSP stable docs）
- https://github.com/cashapp/paparazzi/pull/2430
- https://github.com/cashapp/paparazzi/pull/2431
- https://github.com/slackhq/compose-lints/releases/tag/1.6.0
- https://github.com/alibaba/MNN
- https://github.com/lynx-family/lynx
- https://github.com/Tencent-TDS/dsh-kuikly-expert
- https://github.com/lynx-family/animax
- https://developer.android.com/google/play/requirements/target-sdk
- https://developer.android.com/guide/practices/page-sizes
- https://developer.android.com/build/releases/agp-9-4-0-release-notes
