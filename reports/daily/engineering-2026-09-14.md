# Android Engineering Daily Report

Date: 2026-09-14  
Window: 7 / 30 / 90 days  
Previous snapshot: 2026-09-11

## Executive Summary

本周期只保留 **2 个会改团队动作** 的信号，外加 1 条上一周期写错的成熟度校正。Remote Compose、AGP 9.4、Isolated Projects、Nav3、Metro 全量分析不重写——字段没变到值得再讲一遍。

1. **Play 把内存和 DEX 优化变成 2027-02 发布门槛。** 2026-08-26 官方博文《Elevating app quality》把 Memory（Anon RSS + swap）、Bitmap、DEX 优化写成即将执行的质量要求。Help Center 现在给出按 RAM 档、进程态的 **P90 数字**。上一周期只把 Memory Usage 写成 Memory Limiter 的遥测附件，判断偏窄：限额本身仍不可查询，但 **Play 已经用 vitals 做执法预演**。
2. **R8 Configuration Analyzer 是达标工具，不是可选卫生项。** 文档 **2026-09-08** 更新。Play 要求 DEX > 10 MB 的应用 shrink / optimize / obfuscate **各 ≥ 25%**。Tinder（2026-08-18）证明：开了 full R8 仍可能只有 28%——一条内部库 `-keep public class *` 就能锁死优化。收窄后分数到 50%，慢冷启动 **-47%**，包体 **-29%**，ANR 0.35%→0.28%。上一周期「analyzer Trial / full R8 是执行问题」作废。
3. **Benchmark 1.5.0 已稳定（2026-09-09）。** 上一周期 Hold 里写「1.5 仍 alpha」与官方稳定线矛盾。`requireAot` / `requireMainThread` 默认 true。有 Microbenchmark CI 的仓升级即可，不单独立项。

核心判断：让团队更快、更稳、更高性能的下一杠杆，不再是再挖一层 Compose 微优化，而是 **把 Play 质量门槛接进发布门禁，并用 R8 Analyzer 把 25% 做成可回归的分数**。架构侧本周期无新条目。

## Architecture

本周期无新架构技术进雷达。Remote Compose 仍 **alpha19**，Navigation 3 仍 **1.2.0-rc01**，Metro 只从 1.4.2 补到 **1.4.3**（Hilt interop 在 IR class generation 下修好，推荐仍单 feature Trial）。KMP 默认结构、Circuit、垂直切片无字段变化，不重写。

Play 的质量门槛会倒逼模块边界和图片生命周期，但那是工程与性能问题，不是新的 MVI / Clean Architecture。

## Engineering Productivity

### Play DEX 25% + R8 Configuration Analyzer（Adopt）

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | 大型仓开了 `isMinifyEnabled` 仍被宽 keep、第三方 consumer rules、`proguard-android.txt` 锁死。Play 从 2027-02 起对 DEX > 10 MB 的应用要求 shrink / optimize / obfuscate **各 25%**，不达标影响可见性与发布能力。 |
| 2. 为什么现在出现 | 内存涨价 + Android 17 Memory Limiter。Play 2026-08-26 把 DEX 优化从最佳实践写成质量要求。Analyzer 文档 2026-09-08 刷新；Tinder 案例把「分数」和「用户指标」连上。 |
| 3. 技术原理 | R8 在全程序图上做 shrinking / inlining / class merging / renaming。Analyzer（AGP 9.3+：`:app:analyzeReleaseR8Config`）对每条 keep 计算它挡住了多少类/方法/字段，输出 shrinking / optimization / obfuscation 三个分数。Play 读 `r8.json`（AGP 8.10+ 最新补丁）或回退到 `mapping.txt` + DEX 启发式。分数量的是 **可被优化的代码占比**，不是「已经删掉了多少字节」。 |
| 4. 对比现有方案 | 对比「开 minify 就完事」：Tinder 开了 full R8 仍只有 28%。对比手工扫 ProGuard：Analyzer 按规则归因，能指到内部库那条 `-keep public class * { public protected *; }`。对比 9.4 incubating `R8Plugin`：Analyzer 是现网可用的报告任务，R8Plugin 只是构建拆分信号。 |
| 5. 性能收益 | Tinder（官方）：慢冷启动用户 **-47%**；下载包 86.6 MB → 61.5 MB（**-28.98%**）；用户可感知 ANR 0.35%→0.28%（**-28%**）；DEX 文件 17→11。Monzo 旧数字（ANR -35%、冷启动 +30%）仍成立，但这是执行，不再当发现。 |
| 6. 工程效率收益 | 本地 `:app:analyzeReleaseR8Config` 不打 APK，反馈环短。Tinder 把分数接进 CI，贡献者能看见自己的 keep 是否把分数打下去。`android skills add r8-analyzer` 可把报告压成 Top-5 keep。 |
| 7. 稳定性收益 | 间接。更小的 resident DEX、更少的主线程解释执行，降低 ANR。收窄 keep 有反射漏 keep 风险，必须用 release 回归托底。 |
| 8. 成熟度 | Analyzer 随 AGP 9.3 稳定任务提供；9.4 仓直接用。Play 门槛 2027-02 才执法，但 **每个上传的 AAB 已经出优化洞察**。 |
| 9. 落地成本 | 出分：低（半天）。把分数做到 ≥ 25%：中（几天到两周），取决于内部库 keep。持续 CI：低。 |
| 10. 风险 | 误删反射 keep 导致 release 崩溃；第三方 consumer rules 改不了，只能过滤或换库；CI 产物和上传 Play 的 AAB 不完全一致；不要把 incubating `R8Plugin` 和 Analyzer 一起切。 |
| 11. 大型商业 App | **必须做。** DEX 通常远超 10 MB。先出三个分数和 Top keep，再决定要不要开内存专项。 |

Isolated Projects：稳定线仍 Gradle **9.7.1**。约 2026-09-13 出现 **9.8.0-RC1**（Java 27 等），**未改变 incubating / 禁止生产产物**。KSP 2.3.11（2026-08-03）已支持 `org.gradle.isolated-projects`，本地 Trial 少了一个常见阻断。不重写 1.9× sync 数字。

AGP 仍是 **9.4.0**。无 9.4.x、无 9.5、无 10.0 船期。

## Performance

### Play Memory Core Vitals（Adopt 看板 / Assess 专项改造）

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | 单应用泄漏或咬住 bitmap，会逼设备进 zRAM、杀缓存进程、最后被 Memory Limiter 无堆栈杀掉。Play 现在用 28 天 P90 衡量，而不是等用户投诉。 |
| 2. 为什么现在出现 | 2026-08-26 Play 质量要求。Memory 成为 core vital。限额 API 仍不可读（与上一周期相同），但 **执法面从 OEM 内核变成 Play 看板**——这是 memory 条目里「等 Play vitals 默认执法」的触发条件。 |
| 3. 技术原理 | 采样匿名 RSS + swap（Java/Kotlin 堆、native、匿名映射、zRAM），按进程态（前台 / 用户可感知服务 / 后台 / cached）和设备 RAM 档聚合 P90。Bitmap 单独计量：非前台长时间持有位图没有绘制理由。Android 13+ 有数据；Limiter 杀进程仍靠 `ApplicationExitInfo` 描述里的 `MemoryLimiter:AnonSwap`。 |
| 4. 对比现有方案 | 对比上一周期的 Limiter 遥测：ExitInfo 看见的是 **已经被杀**；P90 看板看见的是 **还没死但已经越线**。对比 `onTrimMemory`：那是自愿释放；Play 门槛是结果指标。对比 Java heap OOM：这是进程级 anon+swap，bitmap / native / 多进程都算。 |
| 5. 性能收益 | 做好了：少 zRAM 抖动，帧时间更稳，少被 Limiter 杀。做不好：先卡顿再死，用户看成「卡 + 闪退」，2027-02 起再叠加商店可见性。防御性收益，不是加速彩票。 |
| 6. 工程效率收益 | Play Console 已按 RAM 档、进程态、版本切分；Developer Reporting API 可进内部看板。Crashlytics ≥ 20.1.0 有 OOM / limiter 调试数据。`ProfilingManager` `TRIGGER_TYPE_ANOMALY` 可在击中限额时抓 heap dump。 |
| 7. 稳定性收益 | 高。P90 越线是系统性泄漏或图片策略问题，比单条无堆栈死亡更早。 |
| 8. 成熟度 | 指标已在 vitals 滚动。执法 **2027-02**。阈值会改，官方承诺给迁移窗口。 |
| 9. 落地成本 | 看板：低（几天）。优化：中高（bitmap、泄漏、进程拆分、R8、`onTrimMemory`）。 |
| 10. 风险 | 实验室高 RAM / 4 KB 页设备漏报；误把所有后台死进程都怪到 Limiter；改商店类目来套游戏阈值违反政策。 |
| 11. 大型商业 App | **必须做看板。** 应用侧关键数字（P90，2027-02）：4 GB 档前台 **2 GB**、用户可感知服务/后台 **1 GB**；8 GB 档前台 **2.25 GB**、后台 **1.5 GB**。Bitmap：服务/后台 **> 200 MB**、cached **> 400 MB** 为坏行为。图多、长会话、播放器、多 WebView 的应用还要按 RAM 档加压。 |

App 侧 Memory P90 门槛（节选，来自 Play HC）：

| RAM 档 | 前台 | 用户可感知服务 | 后台 |
| --- | --- | --- | --- |
| 4 GB | 2 GB | 1 GB | 1 GB |
| 6 GB | 2.25 GB | 1.25 GB | 1.25 GB |
| 8 GB | 2.25 GB | 1.5 GB | 1.5 GB |
| 12 GB | 3.25 GB | 1.75 GB | 1.75 GB |
| 16 GB | 4.25 GB | 2 GB | 2 GB |

16 KB：手机/平板截止仍 **2027-02-01**。**Wear 截止 2026-09-15（本周）**。有 Wear `.so` 的仓这是本周合规，不是发现。不重写对齐教程。

Benchmark **1.5.0（2026-09-09 稳定）**：默认要求 AOT 后再跑 Microbenchmark，禁止在主线程 `measureRepeated`（防 ANR）。上一周期「等稳定再改 CI」过时。升库、看 CI 是否被新默认打断即可。

## New Technology

只进本周期雷达：

1. **Play Memory / DEX quality gates（2026-08-26 公告，门槛页现行）** — 近 30 天政策。Memory 从「Limiter 遥测」变成带数字的 core vital。DEX 25% 是新的工程闸门。
2. **R8 Configuration Analyzer 作为发布工具（文档 2026-09-08；Tinder 2026-08-18）** — 近 7 天文档刷新 + 近 30 天官方 benchmark。它解决的是「为什么 full R8 仍然只有 28%」，不是再写一篇开启 minify 的教程。

未收录：Remote Compose（仍 alpha19）、AGP 10（无船期）、Gradle 9.8 RC（未改 Isolated Projects 成熟度）、Declarative Gradle、又一篇垂直切片、Zero-Tap Sign-In / Restore Credentials（2027-04 产品合规，不是架构/构建/性能发现）。

## Watchlist Diff

详见 `diffs/engineering/2026-09-14.md`。

- **Added：** Play Memory/Bitmap/DEX 质量门槛；R8 Analyzer 升格；Benchmark 1.5.0 stable；Wear 16KB 2026-09-15。
- **Updated：** R8 analyzer Trial → Adopt；Memory 遥测 → P90 执法预演；Metro 1.4.2 → 1.4.3；Gradle 旁路 9.8.0-RC1。
- **Removed：** 无。
- **No rewrite：** Remote Compose、AGP 9.4、Isolated Projects 推荐、Nav3、Circuit Hold、KMP 结构、Baseline/Startup Profile。

## Recommendation

| 技术 | 评级 | 说明 |
| --- | --- | --- |
| Play Memory / Bitmap P90 看板（按 RAM 档 + 进程态） | **Adopt** | 2027-02 执法。先看见，再开专项。 |
| R8 Analyzer + DEX 25% CI 门禁 | **Adopt** | `:app:analyzeReleaseR8Config`；分数进 CI。不要和 `R8Plugin` 现网切混为一谈。 |
| Benchmark 1.5.0（`requireAot` / `requireMainThread`） | **Adopt** | 已稳定。有 Microbenchmark 的仓升级。 |
| AGP 9.4 + `android.newDsl=true` + `android.builtInKotlin=true` | **Adopt** | 用 `newDsl.optOut` 隔离遗留模块。 |
| Configuration Cache | **Adopt** | Isolated Projects 前置。 |
| Navigation 3（新 Compose 流程） | **Adopt** | 仍 1.2 RC，可与 Nav2 并存。 |
| Baseline + Startup Profile CI | **Adopt** | Require 模式门禁。 |
| 16 KB | **Adopt** | 手机/平板 2027-02-01；**Wear 2026-09-15**。 |
| Memory Limiter 遥测（ExitInfo / Crashlytics） | **Adopt** | 和 P90 看板一起看，不要互相替代。 |
| Isolated Projects | **Trial** | 仅本地 / IDE sync / 非生产 CI。用 9.7.1，不要跟 9.8 RC 打生产包。 |
| Metro 1.4.3 单 feature | **Trial** | 验证编译时间与 Hilt interop。 |
| Remote Compose（活动/卡片/远程表面） | **Assess** | 仍 alpha19。 |
| AGP 10 第三方插件盘点 | **Assess** | 现在列清单。 |
| DFM 1:1 flavor | **Assess** | 有 DFM 就开 warning→error。 |
| KMP 新默认结构 | **Assess** | 仅已有或计划 KMP 的仓。 |
| Memory / Bitmap 全盘改造 | **Assess** | 等 P90 证明击中再开专项。 |
| Circuit 全量替换 MVVM | **Hold** | 无新平台压力。 |
| Isolated Projects / Gradle 9.8 RC 打生产包 | **Hold** | 官方未背书。 |
| Remote Compose 进核心流程 | **Hold** | Alpha。 |
| AgpTestSuite / R8Plugin 现网 | **Hold** | Incubating。 |

## PoC Candidates

按投入产出只开这 2 个。不要并行开 10 个。Isolated Projects、Metro、Remote Compose、AGP 9.4 审计上一周期已立项，字段没变，不重复开。

1. **Play DEX 25% + R8 Analyzer CI（3–5 天）**  
   在 AGP 9.4 仓跑 `:app:analyzeReleaseR8Config`，记下 shrinking / optimization / obfuscation 三个分数和 Top keep（先看内部库）。把同一套分数接到上传 Play 的 AAB（看 Bundle Explorer / `r8.json`）。成功标准：三个分数都能量出来；若任一 < 25%，列出要收窄的 keep 和负责模块；CI 在分数下降时失败。Tinder 的教训是：内部「稳定库」往往比第三方更脏。

2. **Play Memory P90 看板 + Limiter 对照（3–5 天）**  
   Console：按 RAM 档、进程态、版本拉 Anon RSS+swap 与 Bitmap 的 28 天 P90，对照上表。现网：继续解析 `MemoryLimiter:AnonSwap`。实验室：在已执法设备上按 **4 GB / 8 GB 档的后台阈值** 加压主路径（启动、信息流、播放器、进后台）。成功标准：能指出是否已经越过 2027-02 门槛，并能把越线会话对上一条可修的泄漏或未释放 bitmap。没越线就不要开全盘改造。

Benchmark 1.5 升级是半日卫生项，不单独立项。

## Sources

- https://android-developers.googleblog.com/2026/08/app-quality-memory-optimization-secure-onboarding.html （2026-08-26）
- https://support.google.com/googleplay/android-developer/answer/17492799 （Play technical quality requirements；Memory P90 / DEX 25% / Wear 16KB 2026-09-15）
- https://android-developers.googleblog.com/2026/08/tinder-app-cold-start-r8-configuration-analyzer.html （2026-08-18；慢冷启动 -47%）
- https://developer.android.com/topic/performance/app-optimization/r8-configuration-analyzer （Last updated 2026-09-08）
- https://developer.android.com/topic/performance/vitals/memory-usage
- https://developer.android.com/jetpack/androidx/releases/benchmark （1.5.0，2026-09-09）
- https://developer.android.com/jetpack/androidx/releases/compose-remote （仍 1.0.0-alpha19，2026-09-09）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes （仍 9.4.0；Last updated 2026-09-03）
- https://developer.android.com/build/releases/gradle-plugin-roadmap （Last updated 2026-07-22）
- https://docs.gradle.org/9.7.1/release-notes.html
- https://github.com/gradle/gradle/releases （9.8.0-RC1）
- https://github.com/ZacSweers/metro/releases/tag/1.4.3 （2026-09-08）
- https://developer.android.com/jetpack/androidx/releases/navigation3 （仍 1.2.0-rc01，2026-09-09）
- https://developer.android.com/guide/practices/page-sizes （手机/平板 16KB 截止 2027-02-01）
- https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html （2026-08-19；Limiter，无新 API）
