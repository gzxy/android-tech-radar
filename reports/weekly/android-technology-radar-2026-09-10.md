# Android Technology Radar

日期：2026-09-10

周期：首次周报基线（相对空雷达）。数据来自当日四路监控：`android-official`、`engineering`、`open-source`、`ai-android`。重复技术已合并，优先保留一手资料与可执行工程结论。

## 1. Executive Summary

本周 Android 工程最值得关注的不是又多了一批仓库，而是四件事叠在同一窗口：

1. **上架门槛已经在咬人。** Play 自 2026-08-31 起强制 target API 36（可延期至 2026-11-01）；16KB 页大小将在 2027-02-01 阻断 target 35+ 的 64-bit 更新。这是发布阻断，不是技术预告。
2. **工具链刚完成一轮稳定发布，并锁死 AGP 10 窗口。** Studio Quail 4 + AGP 9.4.0 + Kotlin 2.4.20 + NDK r30 + KSP 2.3.12。9.4 是升到 AGP 10 前的最后准备窗口——legacy Variant API / `newDsl` / `builtInKotlin` opt-out 会被删除。
3. **能让大仓变快的，是构建模型而不是再写一套 MVI。** Gradle Isolated Projects（9.7 incubating）让 5000+ 模块 Android 仓 Studio sync 约 1.9×；前置条件是 Configuration Cache。官方明确：不要用它打生产包。
4. **Android 工程正在变成「SDK + Agent Skill + MCP」。** Google ADK Kotlin 1.0、`android/skills`、Studio AQI Crash/Leak 闭环、腾讯 KuiklyUI-AI、字节 Lynx AI-ready Roadmap 同时出现。框架评估要同时看 API、第一方 Skill、以及 Agent 能否安全改工程。
5. **国内大厂把精力从热修复/插件化挪到了跨端与端侧 AI。** Lynx 4.1.0 月更兑现，KuiklyUI 2.27.0 把 Compose DSL 页面注册做成 KSP；Tinker / Shadow / Atlas / AndFix 不再是新项目默认方案。

## 2. Top 10 Changes

| Technology | Category | Source | What Changed | Impact | Recommendation |
|---|---|---|---|---|---|
| Play Target API 36 | Official / Policy | android-official | 2026-08-31 起新应用与更新必须 target 36；延期窗口到 2026-11-01 | 上架阻断；触发 edge-to-edge、Predictive Back、大屏自适应 | Adopt |
| 16KB Page Size | Official / Native | android-official | 2027-02-01 起 target 35+ 的 64-bit 更新必须 ELF 16KB 对齐 | 未对齐 so / 第三方 SDK 无法更新 | Adopt |
| AGP 9.4.0 → 10 | Official / Build | android-official + engineering | 9.4.0 支持 API 37，提供 `newDsl.optOut`；10.0 将删除 legacy Variant API | 自定义 Gradle 插件 / DFM 在 10.0 会直接编不过 | Trial（先消警告） |
| Gradle Isolated Projects | Engineering | engineering + open-source | 9.7 升 incubating；Now in Android 已开 project isolation | 大仓 IDE sync 1.4–1.9×；生产包未背书 | Trial（仅本地/IDE） |
| ADK for Kotlin 1.0 | AI / OSS | open-source + ai-android | 2026-09-07 GA，09-10 补 1.0.1；未知 tool 改为返回可用列表 | Android 首次有官方、KMP、可端侧的 Agent 运行时 | Trial |
| android/skills + Studio Agent | AI / Tooling | ai-android + official | Quail 4 内置 Android skills；AQI Fix with AI / LeakCanary Fix with Agent | Crash/Leak 分诊与机械迁移可进人在回路的流程 | Adopt |
| Android 17 Beta | Official / Platform | android-official | Beta 4.1；内存限额、后台音频硬化、本地网络权限 | 部分行为在设备升级后全量生效，不依赖 target 37 | Assess |
| Lynx 4.1.0 / KuiklyUI 2.27.0 | Domestic OSS | open-source | Lynx 按 Roadmap 月更并落地 Autolink；Kuikly Compose 侧 KSP 页面注册 | 跨端从「替代 RN」变成原生嵌入 + 鸿蒙/16KB 必选 | Trial（有跨端 KPI） |
| Metro 1.0 | Architecture | engineering | Kotlin compiler plugin DI，去掉 KSP/KAPT 源码生成 | 迁移团队报告编译耗时下降 50–80%；Hilt 全家桶成本高 | Trial（单 feature） |
| Circuit 0.38 / Benchmark 1.5 | Architecture / Perf | open-source + official | Screen 不再是 Parcelable；`requireAot` 默认 true | 导航状态持久化 breaking；性能 CI 可能因默认值变严而红 | Assess / Trial |

## 3. Domestic Big Tech Open Source

国内监控结论：活着的主线是 **跨端框架 + 端侧推理 + 16KB/鸿蒙兼容**。热修复、插件化、渠道包工具没有第二家在加码。

### Tencent

- **KuiklyUI 2.27.0**：KMP 一套代码打 Android / iOS / Harmony / Web / 小程序。本版 Compose 侧 `KuiklyModulePages` + KSP，页面注册从手写变成编译期生成。2026 Roadmap 把 MCP / Skills / Figma→代码写成主航道。
- **KuiklyUI-AI**（126★）：官方 Skills/Rules。星标低，但是腾讯 TDS 自己在补「AI 怎么正确写 Kuikly」——和 Google `android/skills` 是同一类基础设施。
- **MMKV 2.4.2**：跨端 mmap KV，仍是商业 App 默认候选存储。本版修过多端过期时间常量与 UTF-8 一致性。
- **libpag 4.5.94 / Hippy 3.3.7 LTS**：动画引擎几乎日更；Hippy 仍在修 Android RecyclerView 复用崩溃。叙事已让位给 Kuikly。
- **Tinker / Shadow**：只有修补。新项目不要再以它们为默认动态化方案。

### Alibaba / Ant Group

- **MNN 3.6.1**：定位已写成 on-device LLM / Edge AI，持续修 OpenCL。和 Google ADK + LiteRT-LM 是同一赛道的国内选项，不要两套都上。
- **ARouter**：官方 release 仍停在 2020 的 1.5.1，但 2026-09-05 合并了 interceptor 状态隔离。这是遗产路由库被新系统逼着修，不是路由技术复活。已接入则合入修复；新项目不要新选。
- **SoloPi v1.0.2**（蚂蚁）：无线自动化测试，8 月还在修 overlay 权限。没有完善 UI 自动化的团队仍有 PoC 价值。
- **vlayout / Tangram / Atlas / AndFix**：archived 或死亡。

### ByteDance

- **Lynx 4.1.0**：4.0 之后按月发 4.0.1 / 4.0.2 / 4.1.0，Roadmap 节奏兑现。3.8 引入 Autolink：npm 包装 `lynx.lib.json`，Android 用 Gradle plugin 自动注册 Native Module。
- **btrace 3.1.0**：Perfetto 级方法追踪，本版加 Harmony。对「为什么慢」有用。
- **CodeLocator 2.0.5**：已跟 K2，之后无新版本。
- **BlockFramework**（150★）：开源后几乎没动，先观察不要上生产。
- **ByteX / AlphaPlayer**：已 archived。Transform API 时代的字节码平台不要再评估。

### Meituan / Kuaishou / Others

- **Logan 1.2.12、KOOM**：两边都为 16KB page size 打过补丁。这是 Android 15+ 设备的硬门槛，不是特性。
- **Walle / Robust / Shield**：渠道包和热修复一代，已不活跃。
- 华为 / 百度 / 小米 / 快手新框架：本周未扫到「持续维护 + 可迁入大型 Android 工程」的新开源。小米 MACE 已被 MNN / LiteRT 时代甩开。

## 4. Android Official

一手资料结论（不以搜索摘要为准）：

### 已生效

- **Play target 36：** 未达标更新无法提交。target 36 后 `windowOptOutEdgeToEdgeEnforcement` 在 Android 16 设备上失效；未迁移 Predictive Back 时 `onBackPressed` 不再被调用。
- **大屏（sw>=600dp）：** target 36 忽略方向/比例/可调整大小限制（仍可 opt-out）。**target 37 将取消 opt-out。** 现在不改，明年变成硬失败。

### 2027-02-01 硬截止

- 未 16KB 对齐的 `arm64-v8a` / `x86_64` `.so` 将阻止 Play 更新。Java/Kotlin-only 应用通常已兼容，但仍需 16KB 模拟器回归。含 so 的应用必须现在排期。

### 工具链（最近 14 天稳定发布）

| 组件 | 版本 | 日期 | 工程含义 |
|---|---|---|---|
| Android Studio | Quail 4 2026.1.4 | 2026-09-01 | Quail 最终稳定版；内置 Android skills；Otter 2 Cloud services 已废弃 |
| AGP | 9.4.0 | 2026-09-01 | 支持 API 37；要求 Gradle 9.6+；AGP 10 预演 |
| Kotlin | 2.4.20 | 2026-09-07 | tooling release；不要和 KSP 拆开升 |
| NDK | r30 LTS `30.0.16248370` | 2026-09-08 | AGP 9.4 默认仍是 28.2，有 native 必须显式钉 |
| KSP | 2.3.12 | 2026-09-09 | 最低 AGP 8.12；backing fields 双重 opt-in |
| Compose UI | 1.12.1 | 2026-09-09 | 1.12.0 含可变字体 / WCG，本版为补丁 |
| Benchmark | 1.5.0 | 2026-09-09 | `requireAot` 默认 true，旧 microbenchmark 可能红 |
| Navigation3 | 1.2.0-rc01 | 2026-09-09 | 稳定线仍是 1.1.7；1.2 进入 RC |

### Android 17（现在就要测）

即使尚未 target 37：后台音频非法生命周期调用会静默失败；泄漏/异常内存会话会被系统杀掉（`ApplicationExitInfo` 含 `MemoryLimiter:AnonSwap`）。target 37 额外：`ACCESS_LOCAL_NETWORK`、CT 默认、Native `System.load()` 必须只读、`static final` 不可反射改写。

样板工程水位：Now in Android 已是 Gradle 9.7.1 + AGP 9.3.2 + project isolation + configuration-cache=fail。大厂如果还停在 AGP 8 + 手写 `kotlin-android`，差距已经是工程结构问题。

## 5. Architecture

去重后只保留能改变大型商业 App 结构成本的信号。

### Metro 1.0 — Trial（单 feature）

Kotlin compiler plugin DI，FIR 做分析与类头生成，IR 做其余 codegen，无 KSP 额外 pass。对比 Hilt/Dagger：少一层 annotation processor，多 compile-time 环检测。落地成本中高：Hilt WorkManager / Navigation / ViewModel 扩展要逐项替换或走 interop；`metrox-android` 要求 minSdk 28。**适合 PoC，不适合本周全量切。**

### Navigation 3 — Adopt（新 Compose 流程）/ Assess（1.2 RC）

Nav3 稳定于 2025-11-19，把 back stack 变成应用拥有的 Compose state，是新 Compose 流程的默认选择，可与 Nav2 并存迁移。1.2.0-rc01 本周进入 RC，新版本特性继续 Assess。

### Circuit 0.38 — Assess

`Screen` / `PopResult` 不再是 Parcelable。必须改用 kotlinx-serialization saver、`ParcelableScreen` 或 `CircuitSaver.NoOp`。不支持的值从静默丢弃改为失败。已用 Circuit 必须排期升级；新模块可以 PoC。已经在用 Mavericks/RIBs 且稳定的大仓，不必为了跟风而换。**Circuit 全量替换锁定 MVVM：Hold。**

### KMP 默认结构 — Assess

AGP 9 硬约束：`kotlin-multiplatform` 不能和 `com.android.application` 同模块，必须拆 `androidApp` + `shared`（`com.android.kotlin.multiplatform.library`）。已有 KMP 仓必须评估；纯 Android 仓不必为了对齐结构而拆。

未收录：又一篇 Clean Architecture / 垂直切片博客、无官方数据的「新 MVI 框架」、通用 SDUI 教程。

## 6. Engineering Productivity

### Gradle Isolated Projects — Trial（本地 / IDE）

配置阶段并行化。官方实测：5000+ 模块 Android 仓 Studio sync 5m09s→2m44s（1.9×）。Configuration Cache 是前置条件。官方：**不要用来构建生产产物。** 第三方插件是主阻力。这是本周期对「团队变快」贡献最大的一项。

### AGP 9.4 + built-in Kotlin — Trial / Adopt 预备动作

在 9.x 上提前锁死：

```properties
android.newDsl=true
android.builtInKotlin=true
```

9.4+ 可用 `android.newDsl.optOut=:legacy-lib` 做模块级缓冲，10.0 会删掉。无 Kotlin 源码的模块应 `enableKotlin = false`。现在不做插件盘点，AGP 10 会变成发布阻断。

### Agent Skill 成为升级说明书 — Adopt

`android/skills` v1.0.11 + `Kotlin/kotlin-agent-skills` 把 AGP 9 / Navigation 3 / R8 / KMP 迁移做成可触发 Skill。Google 已写进 AGP Upgrade Assistant 文档。**不要让 Agent 自由发挥升 AGP。** 这不进 APK，直接装到 Cursor / Claude / Codex / Studio。

### Slack Foundry 0.36.0

构建基线已是 AGP 9.3.1 / Gradle 9.6.1 / Kotlin 2.4.10。不要抄整套，抄版本矩阵和 convention 分层。

## 7. Performance

### 16KB — Adopt（合规，不是优化课题）

官方截止 2027-02-01。工具基线：AGP ≥ 8.5.1（实际应在 9.3/9.4）、NDK r28+（有 native 用 r30）、未压缩 `.so` 16KB zip-align。带 SDK / 游戏引擎 / SQLCipher 的应用必须在 **16KB 系统镜像** 上跑启动 Macrobenchmark，4KB 设备数字会骗人。Logan / KOOM 已打过补丁，自研 so 按同样清单过一遍。

### Baseline + Startup Profile CI — Adopt

没有 7 天内的平台新 API。仍然是：Baseline 约 30% 代码执行；R8 改写后再加约 15%；Startup Profile 再给启动约 15%。2026 的差距在 **CI 是否每次发版重生、并用 `BaselineProfileMode.Require` 卡住缺失 profile**。

### AGP R8 Analyzer + keepRules — Trial

`:app:analyzeReleaseR8Config` 不走完整打包，缩短 keep 规则反馈环。`src/<variant>/keepRules/*.keep` 让规则成为 source set。成本低，反馈环短。

### Benchmark 1.5.0 — Trial

`requireAot` 默认 true。升级后要用它重新校准启动/滚动基线，而不是沿用旧 CI 数字。先在独立分支试。

### btrace / LeakCanary

btrace 3.1 加 Harmony tracing。LeakCanary 3.0-alpha-9 已在记 Agent 通信流量——内存工具也在接 Agent 工作流。Profiler LeakCanary `Fix with Agent` 可起草解除引用补丁，人复测 heap。

ANR、启动/帧时间/电量的「改代码 → 再采同一指标」闭环仍未形成，不当流程。

## 8. AI + Android

判断标准：能不能进 Android 团队流程，以及能不能省工程师时间。不写 AI 新闻。

### 已经能省时间

| 闭环 | 路径 | 人还要做什么 |
|---|---|---|
| Crash 分诊 | Play/Crashlytics → Studio AQI Fix with AI 或 Crashlytics MCP → 读仓库 → 改代码 | 批准 diff、确认 mapping、回归 |
| Leak | Profiler LeakCanary → Fix with Agent | 再跑 Profiler |
| 机械迁移 | `android/skills`（edge-to-edge、Nav3、AGP 9、XML→Compose、R8） | 视觉验收、导航回归 |
| UI 冒烟起草 | Maestro MCP 落 YAML；或 Journeys 自然语言 | 稳定 selector；不要两套都养 |

### 未闭环（Hold / Assess）

- ANR 一键修复并复现：AQI 能列出，Verify 需要 systrace / Perfetto，没有产品接上。
- 通用性能（卡顿/启动）除 Leak 外：无「改代码 → 再采同一指标」。
- Cloud Agent 跑 Android 模拟器：官方未交付。
- Jenkins + AI：无 Android 一等协议。
- 架构评审当门禁：无 Verify。

### ADK Kotlin 1.0 — Trial

第一份面向 Android / JVM / KMP 的官方 Agent SDK。同一套 `LlmAgent` 可接 LiteRT-LM 端侧、ML Kit Gemini Nano（beta，尚不支持 tool calling）、Firebase AI，KSP `@Tool` 生成类型安全工具，也支持 MCP Toolset。星标只有 199，但对商业 App 的迁移价值远高于星标。1.0.1 把「模型调用了未注册 tool」从直接结束 invocation 改成返回可用 tool 列表——这是上线后立刻会踩的坑。

**执行建议：** 先把 Crash 和官方 skills 接进现有 Studio/On-call，再谈 Cloud Agent 和自动发版。前者已经能减重复劳动；后者还在断环。未接 MCP/CLI 的通用 Agent 只会增加 review 负担。

## 9. Watchlist Diff

这是仓库首次周报。Diff 不表示「上周刚变」，而表示「相对空雷达，本周哪些条目进入工程决策面」。后续周报只报告相对 `snapshots/weekly/2026-09-10.md` 的增量。

### Added

四路监控全部为首次入库，合并去重后进入周雷达的决策项：

- **Official：** Android 16/17、Studio Quail 4 / Rabbit 1、AGP 9.4、Gradle 9.7.1、Kotlin 2.4.20、KSP 2.3.12、Compose 1.12.1、Navigation3、R8、Baseline Profile、Benchmark 1.5、NDK r30、16KB、Play Target 36。
- **Engineering：** Isolated Projects、AGP 10 lock-in、Metro 1.0、KMP 默认结构、R8 analyzer / keepRules、Startup Profile CI。
- **Domestic OSS：** KuiklyUI / KuiklyUI-AI、Lynx 家族、MMKV、libpag、Hippy、MNN、ARouter、btrace、SoloPi、KOOM、Logan。
- **International OSS：** ADK Kotlin、android/skills、kotlin-agent-skills、CMP 1.12、Circuit、Foundry、Paparazzi、Store、Now in Android。
- **AI Agent：** Studio AQI / Leak Agent、Crashlytics MCP、Android CLI + skills、Journeys、Maestro MCP、Bugbot、Cloud Agent、GitHub Agentic Workflows。

完整清单见 `watchlist/weekly.md`。

### Updated

无。无上一份周快照。

### Downgraded

项目活跃度、技术价值或成熟度在首次分类中已下降，下轮不再当「新闻」展开：

- 热修复 / 插件化：Tinker、Shadow、Atlas、AndFix、Robust、Walle、Shield。
- UI / APM 遗产：Matrix、QMUI、vlayout、Tangram、MACE、ijkplayer、CRN。
- 工具链遗产：ByteX、AlphaPlayer、Flipper、AffectedModuleDetector。
- 架构时尚：Circuit 全量替换锁定 MVVM；通用 SDUI。

### Removed

周雷达本身无历史条目可删。以下仓库已 archived 或明确停止作为新项目候选，从推荐面移除：

- alibaba/vlayout、alibaba/Tangram-Android、alibaba/AndFix、alibaba/atlas
- bytedance/ByteX、bytedance/AlphaPlayer
- facebook/flipper、dropbox/AffectedModuleDetector

## 10. PoC Candidates

最多 5 个。按「一周内能在真实 app module 看到工时或风险变化」排序。

### 1. Gradle Isolated Projects（本地）

```text
Technology
Gradle Isolated Projects（9.7 incubating）

Problem
Configuration Cache 只能跳过「配置未变」的重复构建。IDE sync、改 build logic、第一次 CI 配置仍要配完所有 project。

Expected Benefit
大仓 Android Studio sync 下降 ≥20%（官方万级模块约 1.9×）。每天多次 sync 是 DevXP 级收益。

PoC Scope
前置：Configuration Cache 从 warn→fail。打开 org.gradle.isolated-projects=true（或 diagnostics），量 Studio sync 与 --dry-run 配置时间，记录不兼容插件。不用于 release 流水线。

Estimated Difficulty
中。第三方插件是主阻力。

Success Criteria
sync 下降 ≥20%，且无静默错误；产出不兼容插件清单。
```

### 2. AGP 9.4 / AGP 10 就绪审计

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

### 3. Google ADK for Kotlin 1.0

```text
Technology
google/adk-kotlin 1.0.1

Problem
商业 Android 应用要把 Agent 做进进程：工具调用、session、端侧隐私、云端复杂推理，而不是嵌一个 WebView Chat。内部自研编排会和官方 API 重复。

Expected Benefit
同一套 LlmAgent 接 LiteRT-LM 或 Firebase AI；KSP @Tool 类型安全；Room session 可测试。

PoC Scope
两周：一个带 @Tool 的端侧/混合 Agent + Room session + 一个业务只读工具（搜订单/查库存）。不要一上来做多 Agent。不要上 ML Kit beta 的 tool calling。

Estimated Difficulty
中。KSP 进现有模块即可。

Success Criteria
工具调用可单测；未知 tool 走 1.0.1 容错；不引入第二套推理运行时。
```

### 4. Crash Agent 闭环

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
2/3 给出可编译 diff；至少 1 个能被现有单测或手工复现验证；Agent 在 issue 留下 note。失败则只留给明显 NPE/生命周期错误。
```

### 5. Metro 1.0 单模块

```text
Technology
Metro 1.0（ZacSweers/metro）

Problem
Dagger/Hilt + Anvil + KSP/KAPT 的多工具链兼容成本和源码生成编译税。

Expected Benefit
该模块 compileKotlin 明显下降；单一 compiler plugin 替代版本矩阵。

PoC Scope
选一个无 ContentProvider 启动依赖、无 Hilt WorkManager 的 feature。对比该模块编译与全量 assemble。用 Dagger interop 接到现有 AppComponent。

Estimated Difficulty
中高。Compiler plugin 跟 Kotlin 版本绑定。

Success Criteria
该模块编译时间明显下降，且 interop 能接到现有图。达不到就 Hold，不要扩面。
```

明确不做的 PoC：Cloud Agent 里启动模拟器、ANR 自动修复、Jenkins AI 构建分析、无测试的架构重构、同时上 ADK + MNN、lynxtron 桌面桥。

## 11. Technology Radar

### Adopt

- Play Target API 36（含 edge-to-edge / Predictive Back / 大屏回归）
- 16KB Page Size 合规（native / 第三方 so 盘点 + 16KB 镜像回归）
- Android Studio Quail 4
- Configuration Cache（Isolated Projects 前置，40+ 模块仓非可选）
- Baseline Profile + Startup Profile CI（`BaselineProfileMode.Require`）
- Android CLI + `android/skills` / `kotlin-agent-skills`（给所有 Agent 同一套官方规程）
- Studio AQI Fix with AI + LeakCanary Fix with Agent（人在回路的 Crash/Leak）
- NDK r30 LTS（有 native 时显式钉版本，不要吃 AGP 默认 28.2）

### Trial

- AGP 9.4.0 + `android.newDsl=true` + `android.builtInKotlin=true`（AGP 10 最后窗口）
- Gradle Isolated Projects（仅本地 / IDE sync / 非生产 CI）
- Kotlin 2.4.20（必须与 KSP / Hilt / Room / Compose Compiler 配对）
- Jetpack Compose 1.12.1
- Benchmark 1.5.0（独立分支，预期 `requireAot` 让旧用例失败）
- AGP R8 analyzer + keepRules source set
- Metro 1.0（单 feature，验证编译时间与 Hilt interop）
- Google ADK for Kotlin 1.0（端侧或混合 Agent，不要自研编排层）
- Maestro MCP（主路径冒烟，留下可进 CI 的 YAML；与 Journeys 二选一）
- KuiklyUI 2.27（仅已有鸿蒙/跨端 KPI 的团队做嵌入式 View PoC）

### Assess

- Android 17 Beta（内存限额、后台音频、本地网络——设备升级即生效）
- Navigation3 1.2.0-rc01（稳定线 1.1.7 已可 Adopt 新屏幕；1.2 跟 RC）
- KSP 2.3.12（自定义 processor / backing fields）
- AGP 10.0 第三方插件盘点
- KMP 默认模块拆分（仅已有或计划 KMP 的仓）
- Slack Circuit 0.38（已用必须升级；新模块可 PoC）
- Firebase Crashlytics MCP（Experimental，先值班机）
- GitHub Agentic Workflows（编译/依赖红灯自愈，先单个仓库）
- Paparazzi 2.0.0-alpha05（组件库模块，等稳定再全量）
- Alibaba MNN 3.6.1（与 LiteRT-LM / ADK 对比，选一条主线）

### Hold

- Isolated Projects 打生产包（官方未背书）
- Circuit / Metro 全量替换已锁定的 MVVM + Hilt
- Cursor Cloud Agent 做 Instrumented / ANR（模拟器未交付）
- Jenkins + AI 插件当 Android 闭环
- 新项目选用 Tinker / Shadow / Atlas / AndFix / Robust / Walle
- 新项目选用 Flipper / AffectedModuleDetector / ByteX
- 同时上 ADK + MNN 双推理运行时

## 12. Next Week

下周最值得继续跟踪的方向：

1. **Play target 36 与 16KB 执行进度** — 延期窗口只到 2026-11-01；native 依赖对齐清单是否闭环。
2. **AGP 9.4 升级与 AGP 10 插件债** — 非主干是否编过；`applicationVariants` / 第三方插件兼容表。
3. **Isolated Projects 本地数字** — Configuration Cache fail 之后，Studio sync 与不兼容插件是否有第一手数据。
4. **ADK Kotlin 1.0.x 与 android/skills** — 1.0 后的补丁节奏；官方 Skill 是否覆盖更多机械迁移。
5. **Android 17 内存限额 / 后台音频** — Beta 行为变化页是否继续更新；现网音频与保活模块在 Beta 镜像上的表现。

无新官方数字、推荐不变的 Watchlist：**不要重写本章**。

## 13. Sources

一手资料与当日监控报告：

- `reports/daily/android-official-2026-09-10.md`
- `reports/daily/engineering-2026-09-10.md`
- `reports/daily/open-source-2026-09-10.md`
- `reports/daily/ai-android-2026-09-10.md`
- https://developer.android.com/google/play/requirements/target-sdk （Last updated 2026-09-01）
- https://developer.android.com/guide/practices/page-sizes
- https://developer.android.com/about/versions/16/behavior-changes-16
- https://developer.android.com/about/versions/17/behavior-changes-all （Last updated 2026-09-02）
- https://developer.android.com/studio/releases （Quail 4 \| 2026.1.4）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes （Last updated 2026-09-03）
- https://developer.android.com/build/releases/gradle-plugin-roadmap
- https://blog.gradle.org/introducing-isolated-projects （2026-08-06）
- https://kotlinlang.org/docs/whatsnew2420.html （2026-09-07）
- https://github.com/google/ksp/releases/tag/2.3.12
- https://github.com/android/ndk/releases/tag/r30
- https://developers.googleblog.com/en/announcing-adk-for-kotlin-10-building-production-ready-ai-agents-in-kotlin-android-and-beyond/
- https://github.com/google/adk-kotlin
- https://github.com/android/skills
- https://developer.android.com/studio/gemini/analyze-crashes-with-aqi
- https://www.zacsweers.dev/metro-is-stable/ （2026-04-27）
- https://lynxjs.org/next/blog/lynx-open-source-roadmap-2026
- https://kuikly.tds.qq.com/Blog/roadmap2026.html
- https://github.com/Tencent-TDS/KuiklyUI/releases/tag/2.27.0
- https://slackhq.github.io/circuit/changelog/
- https://firebase.google.com/docs/crashlytics/ai-assistance-mcp
