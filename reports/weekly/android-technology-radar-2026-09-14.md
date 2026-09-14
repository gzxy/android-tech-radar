# Android Technology Radar

日期：2026-09-14

周期：相对 `snapshots/weekly/2026-09-11.md` / `watchlist/weekly.md` 的增量周报。  
本周新日报：`engineering`（09-11、09-14）、`open-source`（09-14）、`ai-android`（09-11、09-14）。`android-official` 仍停在 2026-09-10，与周副本字节一致，不重写未变官方版本号。

## 1. Executive Summary

本周 Android 工程最值得关注的不是又一批仓库，而是发布门槛和 Agent 契约同时变硬：

1. **Play 把内存和 DEX 优化写成 2027-02 质量门槛。** Memory 成为 core vital，按 RAM 档 + 进程态卡 P90；DEX > 10 MB 要求 shrink / optimize / obfuscate 各 ≥ 25%。Tinder 官方数字：开了 full R8 仍可能只有 28%，收窄一条内部库 keep 后分数到 50%，慢冷启动 **-47%**。R8 Analyzer 从「可选卫生」升到 Adopt。
2. **Google 把上周拆开的两条 Agent 线接到同一套函数上。** ADK main 新增 `AppFunctionsToolset`：进程内 `LlmAgent` 发现并调用本 App 的 `@AppFunction`。样品仓同一天对齐 Jetpack **alpha11**。系统 Gemini 仍是 EAP——函数写一次、先用 Toolset 自测；不要把 1.0.2 未发版坐标写进 version catalog。
3. **三件「还在 PoC」的工具链变成执行项。** Benchmark 1.5.0 已稳定（上一周期误标 alpha）；AGP 9.4.0 才是当前 9.x 稳定线（`newDsl.optOut` 按模块还债）；R8 Analyzer 文档 2026-09-08 刷新。Isolated Projects 推荐不变，仍禁止生产包。
4. **官方 SDUI 终于有坐标：Remote Compose `1.0.0-alpha19`。** 解决的是发版周期，不是再发明 MVI。核心交易 / 主导航 Hold；活动页 / 卡片可以 spike。
5. **国内大厂没有新功能发版。** Kuikly 仍 2.27.0，Lynx 仍钉 4.1.0（4.0.3 是空 notes 的维护 tag）。唯一该改动作的遗产信号：ARouter develop 合并了未发布的 KSP2 编译器——等正式坐标，禁止 snapshot 进主干。

## 2. Top 10 Changes

| Technology | Category | Source | What Changed | Impact | Recommendation |
|---|---|---|---|---|---|
| Play Memory P90 门槛 | Official / Perf | engineering | 2026-08-26 质量要求；HC 给出按 RAM 档 + 进程态的 P90 数字；2027-02 执法 | 先看见越线再开专项；Limiter 杀进程是结果，看板是预警 | Adopt（看板） |
| R8 Analyzer + DEX 25% | Official / Build | engineering | 文档 2026-09-08；Play 要求三项各 ≥ 25%；Tinder 28%→50%，冷启动 -47% | 开了 minify 不等于达标；分数进 CI | Trial → **Adopt** |
| ADK `AppFunctionsToolset` | AI / OSS | open-source | main 让进程内 Agent 调本 App `@AppFunction`；`compileOnly` alpha11 | 函数契约写一次，消费方有两个；生产仍钉 1.0.1 | Trial（改 PoC 结构） |
| AppFunctions 样品 alpha11 | Official / AI | open-source | Testing Agent 切到 `AppFunctionState` / observe / search | 不要再按 alpha10 文档实现 | Trial（跟 alpha11） |
| Benchmark 1.5.0 | Official / Perf | engineering | 2026-09-09 **稳定**；`requireAot` / `requireMainThread` 默认 true | 有 Microbenchmark 的仓升级即可，不单独立项 | Trial → **Adopt** |
| AGP 9.4.0 + New DSL | Official / Build | engineering | 当前 9.x 稳定线；`newDsl.optOut=:module`；DFM 1:1 默认 warning | AGP 10 审计应落在 9.4，不要停在 9.3 | Trial → **Adopt** |
| Remote Compose | Architecture | engineering | `androidx.compose.remote` alpha19（2026-09-09）；90 天 alpha12→19 | 官方 SDUI；无 RC，核心流程不要上 | Assess（非核心 Trial） |
| android-profiler / Perfetto | AI / Perf | ai-android | 官方路径：录 trace → SQL → 根因；自动改代码+复测仍断 | 省读 trace 的 30–90 分钟，不省调参 | **Trial**（只试分析） |
| ARouter KSP2 | Domestic OSS | open-source | develop 合并独立 `arouter-compiler-ksp`（0.1.0-SNAPSHOT，矩阵含 AGP 9.3.2） | 遗产路由被 AGP 9 逼着续命，不是路由复活 | 观察，禁止 snapshot |
| Wear 16KB / Paparazzi / Lynx | Official / OSS | engineering + oss | Wear 截止 **2026-09-15**；Paparazzi 修 `--parallel cleanRecord` 竞态；Lynx 4.0.3 空 tag | 有 Wear so 是本周合规；大仓空 golden 先怀疑任务顺序 | 16KB Adopt；其余 Rec 不变 |

## 3. Domestic Big Tech Open Source

本周无 P0/P1 新功能版本号。热修复 / 插件化继续沉寂。华为 / 百度 / 小米 / 快手 / 网易 / 京东再扫一轮，仍没有可迁入大型 Android 工程的新开源。

### Tencent

- **KuiklyUI 仍是 2.27.0。** HEAD 是 H5 父拖拽/子点击冲突；`chore: update 2.1 publish version` 只是发布脚本，不是 2.28，也不是 Compose DSL 正式发版。
- **KuiklyUI-AI** 继续停在 08-10。`dsh-kuikly-expert` 无新提交；同组织 `dsh-create-app`（1★）是重复包装，不入库。
- MMKV / libpag / Hippy：无版本变化。

### Alibaba / Ant Group

- **ARouter：release 仍是 2020 的 1.5.1，develop 不再只是 interceptor 补丁。** PR #1088 新增独立 KSP2 工程，覆盖路由 / Provider / Autowired / Interceptor；增量删除有测试；和旧 APT 可按模块混用（同一模块只能选一种后端）。Kotlin 字段只保证 `@JvmField` 和可写 `lateinit`。官方写明 unpublished。已用且在迁 AGP 9 / 去 kapt 的大仓：现在盘字段形态，**等 Maven 坐标，不要 `mavenLocal` 进主干**。
- **MNN 3.6.1 未发版。** main 是 RVV KV-cache / OpenCL FlashAttention，对 Android 宿主 API 无新约束。已用团队当性能提交跟，不要当新推理栈。
- SoloPi：无变化。

### ByteDance

- **Lynx 功能线仍是 4.1.0。** 09-11 的 **4.0.3** release body 为空——4.0 维护线，不是路线图 4.2（仍指向 2026-10）。develop 继续回滚 Android Markdown、iOS 异步 UI。**继续钉 4.1.0。**
- **lynxtron v0.0.22：** 桌面 CEF / AutoLink / Linux TestBench。只有桌面 KPI 才看。
- **lynx-stack** 切到 `create-rspeedy@0.17.2`，并在 GenUI bench 复用 UI Judge——工具链侧「AI-ready」声响，不是 Android 宿主 SDK。
- btrace / CodeLocator / BlockFramework：无新版本。

### Meituan / Kuaishou / Others

- Logan / KOOM / 一代热修复：无复活。
- 小米 MACE 继续被 MNN / LiteRT 甩开。

## 4. Android Official

`android-official` **无新日报**，与 `reports/daily/android-official-2026-09-10.md` 字节一致。版本号结论不变：

- Play target 36：2026-08-31 起强制，延期窗口到 **2026-11-01**。
- 16KB：手机/平板 **2027-02-01**；**Wear 截止 2026-09-15（本周）**——有 Wear `.so` 的仓是合规事件，不是发现。
- 工具链地板：Studio Quail 4 + AGP 9.4.0 + Kotlin 2.4.20 + NDK r30 + KSP 2.3.12。
- Android 17 Beta 4.1：内存限额 / 后台音频硬化，设备升级即生效。

工程监控叠加到官方面、且**会改团队动作**的新证据：

- Play HC 给出 Memory P90 / Bitmap / DEX 25% 的现行数字门槛（2027-02 执法，上传已出洞察）。
- R8 Configuration Analyzer 文档 2026-09-08。
- Benchmark 1.5.0 稳定日 2026-09-09。
- Wear 16KB 本周到期。

这些改变「怎么过商店质量门」，不改变 Studio / AGP / Kotlin 版本号。

## 5. Architecture

无新架构框架稳定发版。Navigation 3 仍 1.1.7 / **1.2.0-rc01**；Circuit 仍 0.38；KMP 默认模块拆分 Rec 不变。

本周进决策面的只有一条：

- **Remote Compose（`androidx.compose.remote` 1.0.0-alpha19）。** 服务端用接近 Compose 的 DSL 写出二进制 document，客户端 native player 回放——不是 JSON 组件白名单。上一周期「SDUI 无高信号」作废。**核心交易 / 主导航 Hold。** 营销卡片、活动落地、Glance 类表面可以 2 周 spike。不要用它替换 Design System。

Metro **1.4.3**（2026-09-08）补了 IR class generation 下的 Hilt interop。推荐仍 **单 feature Trial**，不是 2.0，不升级为 Adopt。**Circuit / Metro 全量替换锁定 MVVM：仍 Hold。**

ARouter KSP2 改变的是遗产路由的编译后端，不是换路由框架。新项目不要新选 ARouter。

## 6. Engineering Productivity

本周真正改动作的是发布门禁，不是再挖一层 sync：

- **R8 Analyzer + DEX 25%：Adopt。** `:app:analyzeReleaseR8Config` 不打 APK，输出 shrinking / optimization / obfuscation 三个分数和 Top keep。把分数接到上传 Play 的 AAB（`r8.json` / Bundle Explorer）。不要和 incubating `R8Plugin` 现网切混为一谈。`android skills add r8-analyzer` 可把报告压成 Top-5 keep。
- **AGP 9.4.0：Adopt。** 用 `android.newDsl=true` + `android.builtInKotlin=true`，遗留模块用 `android.newDsl.optOut=:legacy-lib`。有 DFM 的仓把 flavor 1:1 从 warning 升 error——10.0 默认失败。无 9.4.x / 9.5 / 10.0 船期。
- **Isolated Projects：仍 Trial，仅本地 / IDE。** 稳定线 Gradle **9.7.1**。约 2026-09-13 出现 **9.8.0-RC1**，未改 incubating，**禁止生产包**。KSP 2.3.11 已支持 `org.gradle.isolated-projects`，本地少一个常见阻断。不重写 1.9× sync 数字。
- **Configuration Cache / compose-lints / Dagger KSP：** Rec 不变。Foundry main 已把构建基线推到 Kotlin 2.4.20——已对齐 Foundry 的仓跟上。

Benchmark 1.5 升级是半日卫生项，见 Performance。

## 7. Performance

官方 Baseline / Startup Profile 默认值无新日报，Require 门禁结论不变。

本周新杠杆是 **Play 质量门槛 + 已稳定的 Benchmark**：

- **Memory P90 看板：Adopt。** 采样匿名 RSS + swap，按进程态和 RAM 档聚合 28 天 P90。应用侧关键数字（2027-02）：4 GB 档前台 **2 GB**、后台 **1 GB**；8 GB 档前台 **2.25 GB**、后台 **1.5 GB**。Bitmap：服务/后台 **> 200 MB**、cached **> 400 MB** 为坏行为。Limiter 的 `MemoryLimiter:AnonSwap` 看见的是已经被杀；看板看见的是还没死但已经越线。没越线不要开全盘改造。
- **R8 / DEX：** 见上一节。Tinder：慢冷启动用户 -47%；包体 86.6→61.5 MB；ANR 0.35%→0.28%。
- **Benchmark 1.5.0：Adopt（有 Microbenchmark 的仓）。** 默认要求 AOT 后再跑，禁止主线程 `measureRepeated`。上一周期「等稳定再改 CI」过时。
- **Wear 16KB：2026-09-15。** 手机/平板截止仍 2027-02-01。
- **Paparazzi：** `#2377` 修了多模块 `--parallel cleanRecord` 删掉刚录 golden 的竞态；`#2383` 剪掉 `NO_HIDE_DESCENDANTS` 整棵子树。已上 2.0-alpha 且开 `--parallel` 的模块：先吃这两笔 main，再查 flaky。
- **Perfetto 分诊：** 见 AI 章。分析闭环可 Trial；自动加速 x% 仍 Hold。

## 8. AI + Android

`ai-android` 09-11 补了三条流程，09-14 **没有新产品把生产 ANR、Perfetto 复测、Cloud 模拟器或 Jenkins 接成闭环**。官方技能库仍 24 个 SKILL.md，Crashlytics MCP 仍 Experimental，Maestro CLI 仍 2.10.0。

| 轨道 | 仓库 / 产品 | 做什么 | 本周动作 |
|---|---|---|---|
| 进程内 Agent | `google/adk-kotlin` 1.0.1 + main Toolset | App 自己跑模型，现可消费本 App AppFunctions | 改 PoC：函数写一次 + Toolset 自测；**等 1.0.2 再升生产依赖** |
| 系统级 Tool | AppFunctions alpha11 + `android/appfunctions` | App 被 Gemini / 系统 Agent 调用 | 样品按 `AppFunctionState` 写；Gemini 仍 EAP |
| 怎么写这两套 | `android/skills` + Quail 4 预装 | 发现 → 实现 → KDoc → ADB | 09-11 起 Adopt 宿主就是 Quail 4，不必先装 CLI |
| 性能分诊 | `android-profiler` → Perfetto SQL | 读 `.perfetto-trace`，给出可复现查询 | **Trial 分析**；自动改代码+复测 Hold |
| Crash | Quail 4 AQI / Crashlytics MCP | 人在回路修 NPE/生命周期 | 无增量；没做完的 PoC 继续做 |
| 跨平台迁原生 | Studio Rabbit 1 Canary | iOS / Flutter / RN → Kotlin+Compose | 有源工程才 Assess；编译过 ≠ 能上架 |

09-11 的「不要把 AppFunctions 和 ADK 揉成一个里程碑」对**系统 Gemini EAP** 仍然成立；对**自己 App 里的 Agent** 已经过时——契约共用，里程碑仍拆开。

Cloud Agent 启模拟器、生产 ANR 自动修、Jenkins AI：仍 Hold。Rabbit 1 没有源工程的团队忽略。

## 9. Watchlist Diff

相对 `watchlist/weekly.md`（2026-09-11）与 `snapshots/weekly/2026-09-11.md`。

### Added

进入周雷达决策面：

- **Play Memory / Bitmap P90 看板**（Adopt）— 2027-02 执法预演；先看见再专项。
- **Remote Compose alpha19**（Assess）— 官方 SDUI；核心流程另加 Hold。
- **android-profiler / Perfetto 分诊**（Trial）— 读 trace 有验证，修代码无复测。
- **Rabbit 1 跨平台迁移**（Assess）— Canary；无源工程则忽略。
- **Remote Compose 进核心流程**（Hold）。
- **Kotlin Toolchain 替换 Gradle**（Hold）— 只有 Agent Skill，没有第二家 Android 大仓落地。

领域 Watchlist 有信号、**不进雷达主环**：

- ARouter KSP2 unpublished snapshot
- CMP 1.13.0-alpha01（Android minSDK 24；稳定版留 1.12.0）
- lynxtron v0.0.22 / lynx-stack rspeedy 0.17.2
- Gradle 9.8.0-RC1（旁路版本）
- OkHttp / Retrofit GitHub 名重定向到 Commonhaus（Maven 坐标未变）

### Updated

Rec 变了：

- **R8 Analyzer：** Trial → **Adopt**（Play DEX 25% 闸门，不再只是 keep 反馈环）。
- **Benchmark 1.5.0：** Trial → **Adopt**（已稳定，有 Microbenchmark 的仓升级）。
- **AGP 9.4.0：** Trial → **Adopt**（当前 9.x 稳定线 + 模块级 opt-out）。

Version / Signal 变、Rec 不变：

- **ADK Kotlin：** 1.0.1；main 增加 `AppFunctionsToolset`（alpha11 `compileOnly`）。仍 Trial。
- **AppFunctions：** alpha10 → **alpha11** + 样品 Testing Agent。仍 Trial。
- **16KB：** 补 Wear **2026-09-15**。仍 Adopt。
- **Paparazzi：** + `--parallel cleanRecord` 竞态 / 隐藏子树剪枝。仍 Assess。
- **Metro：** 1.4.2 → **1.4.3**。仍 Trial。
- **Lynx：** 记下 4.0.3 维护 tag。仍条件 Trial，钉 4.1.0。
- **MNN：** + RVV / FlashAttention。仍 Assess。
- **android/skills：** Quail 4 预装；技能数仍 24。仍 Adopt。

官方版本号（Play 36、Quail 4、Kotlin 2.4.20、Compose 1.12.1、Android 17、Nav3、KSP 2.3.12）无新日报，不重写。

### Downgraded

无新增降级。热修复 / 插件化 / Flipper / ByteX 维持 Hold。

### Removed

无。无新增 archived。不从周雷达推荐面再删条目。

## 10. PoC Candidates

最多 5 个。用本周新闸门换掉「AGP 9.4 审计」（9.4 已升 Adopt，直接执行）和「AppFunctions 与 ADK 各写一套」。

### 1. Play DEX 25% + R8 Analyzer CI

```text
Technology
AGP 9.3+ :app:analyzeReleaseR8Config + Play DEX 25%（shrink / optimize / obfuscate）

Problem
大型仓开了 isMinifyEnabled 仍被宽 keep、第三方 consumer rules 锁死。Play 从 2027-02 起对 DEX > 10 MB 的应用按三项分数卡可见性。

Expected Benefit
把「开了 R8」变成可回归的分数；Tinder 证明一条内部库 keep 就能把 28% 锁死，收窄后冷启动 -47%。

PoC Scope
AGP 9.4 仓跑 Analyzer，记下三个分数和 Top keep（先看内部库）。同一套分数对上上传 Play 的 AAB（r8.json / Bundle Explorer）。分数下降则 CI 失败。不要和 incubating R8Plugin 一起切。

Estimated Difficulty
出分：低（半天）。做到 ≥ 25%：中（几天到两周）。

Success Criteria
三个分数都能量出来；若任一 < 25%，列出要收窄的 keep 和负责模块；CI 能拦住回退。
```

### 2. Play Memory P90 看板 + Limiter 对照

```text
Technology
Play Memory / Bitmap core vitals + ApplicationExitInfo MemoryLimiter:AnonSwap

Problem
单应用泄漏或咬住 bitmap 会先卡顿再被无堆栈杀掉。限额 API 仍不可查；Play 已经用 28 天 P90 做执法预演。

Expected Benefit
在 2027-02 之前知道自己有没有越过 RAM 档门槛，并把越线会话对上可修的泄漏或未释放 bitmap。

PoC Scope
Console：按 RAM 档、进程态、版本拉 Anon RSS+swap 与 Bitmap 的 28 天 P90。现网：继续解析 MemoryLimiter:AnonSwap。实验室：按 4 GB / 8 GB 档后台阈值加压启动、信息流、播放器、进后台。没越线不要开全盘改造。

Estimated Difficulty
看板：低（几天）。归因：中。

Success Criteria
能指出是否已经越过 2027-02 门槛，并能把越线会话对上一条可修根因。
```

### 3. AppFunctions + ADK Toolset（改结构，不要等 1.0.2 上生产）

```text
Technology
Jetpack AppFunctions 1.0.0-alpha11 + AppFunctionsToolset（adk-kotlin main）+ android/skills device-ai/appfunctions

Problem
「查订单 / 建草稿」应调用已经存在的业务 API。@Tool 和 @AppFunction 各写一遍会在系统助理开闸时炸掉契约。

Expected Benefit
函数写一次：进程内 Agent 用 Toolset 自测；系统 Gemini EAP 将来走同一套。默认只看自己的包，设备没有 AppFunctions 时 Toolset 为空、不崩。

PoC Scope
独立 :appfunctions 模块，compileSdk 36，KSP。2 个只读 @AppFunction + AppFunctionsToolset(context) 挂到 LlmAgent + adb shell cmd app_function 对照。必须自己声明 androidx.appfunctions:1.0.0-alpha11。不要把 adk-kotlin main 写进生产 catalog。不要承诺「下个版本就能被 Gemini 调到」。

Estimated Difficulty
中。权限模型在跨包时才变成系统级。

Success Criteria
两个函数能被 Testing Agent / ADB / 进程内 Agent 调通；Skill 生成的 manifest 可审；不引入第二套推理运行时。
```

### 4. Perfetto 分诊（android-profiler）

```text
Technology
APA / Studio System Trace + android-profiler skill + Perfetto trace_processor SQL

Problem
启动 / jank / 内存问题的前 30–90 分钟耗在「打开 UI 盲翻 track」。没有产品做自动改代码再采同一指标。

Expected Benefit
同一张 .perfetto-trace 上得到可复现 SQL 和说得通的根因方向。

PoC Scope
选一张已知卡顿或启动 trace。只验收分析。不要验收「自动加速 x%」。不要接到生产 ANR 自动修。

Estimated Difficulty
低。官方 skill 已在 Quail 4。

Success Criteria
查询可复现；工程师认可根因方向；留下可复用的 SQL 片段。
```

### 5. Gradle Isolated Projects（本地，继续）

```text
Technology
Gradle Isolated Projects（9.7.1 incubating）

Problem
Configuration Cache 只能跳过「配置未变」的重复构建。IDE sync、改 build logic、第一次 CI 配置仍要配完所有 project。

Expected Benefit
大仓 Android Studio sync 下降 ≥20%（官方万级模块约 1.9×）。

PoC Scope
前置：Configuration Cache 从 warn→fail。打开 org.gradle.isolated-projects=true（或 diagnostics），量 Studio sync 与 --dry-run 配置时间，记录不兼容插件。用 9.7.1，不要跟 9.8 RC。不用于 release 流水线。

Estimated Difficulty
中。第三方插件是主阻力。KSP 2.3.11+ 已不是阻断。

Success Criteria
sync 下降 ≥20%，且无静默错误；产出不兼容插件清单。
```

明确不做的 PoC：Cloud Agent 里启动模拟器、ANR 自动修复、Jenkins AI、同时上 ADK + MNN、把系统 Gemini 联调写进本迭代、追 Lynx develop / 4.0.3、ARouter snapshot、Kotlin Toolchain 弃 Gradle、Remote Compose 进核心流程、Memory 全盘改造（先看 P90）。compose-lints、Dagger KSP、AGP 9.4、Benchmark 1.5 **不必 PoC**，直接执行。Crash AQI 若上周没做完，继续做，不新开名目。

## 11. Technology Radar

未变条目不重写解释。本周环位变化见各条「Since / 变化」。

### Adopt

- Play Target API 36（含 edge-to-edge / Predictive Back / 大屏回归）
- 16KB Page Size 合规（手机/平板 2027-02-01；**Wear 2026-09-15**）
- Android Studio Quail 4
- Configuration Cache（Isolated Projects 前置，40+ 模块仓非可选）
- Baseline Profile + Startup Profile CI（`BaselineProfileMode.Require`）
- Android CLI + `android/skills` / `kotlin-agent-skills`（Quail 4 已预装；技能数仍 24）
- Studio AQI Fix with AI + LeakCanary Fix with Agent（人在回路的 Crash/Leak）
- NDK r30 LTS（有 native 时显式钉版本，不要吃 AGP 默认 28.2）
- Dagger / Hilt KSP（新模块禁止 kapt；旧模块分批）
- compose-lints 1.6.0（Slack 生产 Compose lint，直接接 CI）
- **R8 Analyzer + Play DEX 25%**（`:app:analyzeReleaseR8Config`；分数进 CI）
- **Play Memory / Bitmap P90 看板**（按 RAM 档 + 进程态；没越线不开专项）
- **Benchmark 1.5.0**（有 Microbenchmark 的仓升级；`requireAot` / `requireMainThread`）
- **AGP 9.4.0 + New DSL / built-in Kotlin**（模块级 `newDsl.optOut`；DFM 1:1 先变成 error）

### Trial

- Gradle Isolated Projects（仅本地 / IDE sync / 非生产 CI；钉 9.7.1）
- Kotlin 2.4.20（必须与 KSP / Hilt / Room / Compose Compiler 配对）
- Jetpack Compose 1.12.1
- Metro 1.4.3（单 feature，验证编译时间与 Hilt interop）
- Google ADK for Kotlin 1.0（钉 1.0.1；PoC 可按 main Toolset 写；等 1.0.2）
- Maestro MCP（主路径冒烟，留下可进 CI 的 YAML；与 Journeys 二选一）
- KuiklyUI 2.27（仅已有鸿蒙/跨端 KPI 的团队做嵌入式 View PoC）
- AppFunctions 1.0.0-alpha11（只读函数 + Toolset 自测 + ADB；系统 Gemini 仍 EAP）
- **android-profiler / Perfetto 分诊**（只验收可复现 SQL，不验收自动加速）

### Assess

- Android 17 Beta（内存限额、后台音频、本地网络——设备升级即生效）
- Navigation3 1.2.0-rc01（稳定线 1.1.7 已可 Adopt 新屏幕；1.2 跟 RC）
- KSP 2.3.12（自定义 processor / backing fields；Hilt/Dagger 路径已 Adopt）
- AGP 10.0 第三方插件盘点
- KMP 默认模块拆分（仅已有或计划 KMP 的仓）
- Slack Circuit 0.38（已用必须升级；Parcelable breaking 未撤回）
- Firebase Crashlytics MCP（Experimental，先值班机）
- GitHub Agentic Workflows（编译/依赖红灯自愈，先单个仓库）
- Paparazzi 2.0.0-alpha05（本周修并行录制竞态，不是 2.0 稳定信号）
- Alibaba MNN 3.6.1（RVV/FlashAttention 不是换栈理由；勿与 ADK 双栈）
- **Remote Compose 1.0.0-alpha19**（活动/卡片/远程表面；无 RC）
- **Studio Rabbit 1**（有 iOS / Flutter / RN 源工程才看；Canary）

### Hold

- Isolated Projects / Gradle 9.8 RC 打生产包（官方未背书）
- Circuit / Metro 全量替换已锁定的 MVVM + Hilt
- Cursor Cloud Agent 做 Instrumented / ANR（模拟器未交付）
- Jenkins + AI 插件当 Android 闭环
- 新项目选用 Tinker / Shadow / Atlas / AndFix / Robust / Walle
- 新项目选用 Flipper / AffectedModuleDetector / ByteX
- 同时上 ADK + MNN 双推理运行时
- 把 AppFunctions 和系统 Gemini 联调写成同一个生产里程碑（契约可共用，EAP 不能绑死）
- **Remote Compose 进核心交易 / 主导航**
- **用 Kotlin Toolchain 替换 Gradle / 把 ARouter 0.1.0-SNAPSHOT 打进主干**

## 12. Next Week

下周最值得继续跟踪的方向：

1. **Play DEX 25% 与 Memory P90 第一手分数** — Analyzer 三个分数是否能量出来；Console 是否已经越线。
2. **ADK Kotlin 1.0.2** — `AppFunctionsToolset` / MCP reject / `onRunError` 是否进稳定包；样品是否继续停在 alpha11。
3. **Play target 36 与 16KB** — 延期窗口只到 2026-11-01；Wear 16KB 本周到期后的残留 so。
4. **AGP 9.4 落地数字** — `newDsl.optOut` 清单、DFM 1:1、Isolated Projects 本地 sync（钉 9.7.1）。
5. **Kuikly Compose DSL 正式发版 / Lynx 4.2 / Remote Compose RC** — 都还没到。不到点不要把 develop HEAD 或 alpha 当发版。

无新官方数字、推荐不变的 Watchlist：**不要重写本章。**

## 13. Sources

一手资料与本周监控报告：

- `reports/daily/engineering-2026-09-11.md`
- `reports/daily/engineering-2026-09-14.md`
- `reports/daily/open-source-2026-09-14.md`
- `reports/daily/ai-android-2026-09-11.md`
- `reports/daily/ai-android-2026-09-14.md`
- `reports/daily/android-official-2026-09-10.md`（无增量）
- `reports/weekly/android-technology-radar-2026-09-11.md`
- https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html （2026-08-26）
- https://support.google.com/googleplay/android-developer/answer/17492799 （Memory P90 / DEX 25% / Wear 16KB）
- https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html （2026-08-18）
- https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer （2026-09-08）
- https://developer.android.com/jetpack/androidx/releases/benchmark （1.5.0，2026-09-09）
- https://developer.android.com/jetpack/androidx/releases/compose-remote （1.0.0-alpha19，2026-09-09）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes
- https://github.com/google/adk-kotlin （`AppFunctionsToolset`，`6f349ef5af`）
- https://github.com/android/appfunctions/pull/52
- https://developer.android.com/jetpack/androidx/releases/appfunctions （1.0.0-alpha11）
- https://github.com/alibaba/ARouter/pull/1088
- https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.13.0-alpha01
- https://github.com/cashapp/paparazzi/pull/2377
- https://github.com/cashapp/paparazzi/pull/2383
- https://github.com/ZacSweers/metro/releases/tag/1.4.3
- https://github.com/lynx-family/lynx/releases/tag/4.0.3
- https://developer.android.com/android-performance-analyzer/analyze/ai
- https://developer.android.com/google/play/requirements/target-sdk
- https://developer.android.com/guide/practices/page-sizes
