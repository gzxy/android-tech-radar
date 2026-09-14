# Android Engineering Daily Report

Date: 2026-09-11  
Window: 7 / 30 / 90 days  
Previous snapshot: 2026-09-10

## Executive Summary

本周期只保留 **3 个会改团队动作** 的信号。Isolated Projects、Metro 全量分析、Baseline 教程不重写——成熟度与推荐未变。

1. **Remote Compose 是官方 Server Driven UI。** `androidx.compose.remote` 于 **2026-09-09** 发到 **1.0.0-alpha19**。90 天内从 alpha12 连发到 alpha19，公开 API / Preview / 自定义组件在加速放开。上一周期「SDUI 无高信号」判断作废。它解决的是发版周期，不是再发明一套 MVI。
2. **AGP 当前稳定线是 9.4.0，不是 9.3。** 9.4（notes 2026-09-03）给出大型仓真正用得上的阀门：`android.newDsl.optOut=:module`，以及 DFM 1:1 flavor 的 warning。AGP 10 就绪审计应落在 **9.4 + Gradle ≥ 9.6**，不要停在 9.3。
3. **Android 17 Memory Limiter 已从 Beta 行为变成现网课题。** 2026-08-19 官方博文：Pixel 已开，OEM 将在一年内铺到 4–16GB。超限先被打进 zRAM（卡顿），再被 **无堆栈杀掉**。这是稳定性与帧时间问题，不是再挖一层 Compose 微优化。

核心判断：让团队更快的仍是 **Configuration Cache → 本地 Isolated Projects → 用 AGP 9.4 清插件债**。让团队更稳的新变量是 **Memory Limiter 遥测**。架构上唯一值得进雷达的新技术是 **Remote Compose**，且只配非核心表面。

## Architecture

### Remote Compose（Assess / 非核心 Trial）

官方坐标：`androidx.compose.remote:*`。创建端可在 **纯 JVM** 跑（无需 Android SDK）；播放端用 native player，不是 WebView。

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | 运营/活动/远程表面要改 UI 却必须走完整发版。自研 JSON 组件目录既贵又把布局锁死在客户端白名单里。 |
| 2. 为什么现在出现 | Compose 绘制/布局指令终于能序列化成紧凑二进制文档。90 天内公开 API 从库内可见推到外部可用；alpha19（2026-09-09）仍在修 density / 文本对齐，说明有人在真用。Glance Wear 基建已开始依赖同一套 capture API。 |
| 3. 技术原理 | 服务端用接近 Compose 的 DSL 写出 document；客户端 `RemoteComposePlayer` / View 回放绘制、布局、触摸与表达式。不是「JSON → when(component)」映射，而是 **操作日志回放**。 |
| 4. 对比现有方案 | 对比 JSON SDUI：布局自由度高，客户端不用维护巨型组件注册表，但服务端必须会写 Remote DSL。对比 WebView：原生绘制与无障碍路径，包体与进程模型更轻。对比全量进 APK：省发版，失掉编译期 UI 检查。 |
| 5. 性能收益 | 二进制文档解析通常低于等价 JSON 树。收益在首屏文档成本和滚动时的 player 开销，**没有官方 Macrobenchmark 数字**，不能写进启动 KPI。 |
| 6. 工程效率收益 | 活动页、配置卡片、远程表盘可以不发版。Studio preview API（`RemoteContentPreview` 等）从 alpha12 起存在。每两周一次 alpha 意味着对接成本高。 |
| 7. 稳定性收益 | 无。Alpha 每两周改签名。远程文档等价于受控的「远程 UI 程序」，需要校验、版本、降级。稳定性取决于你们的文档管道，不取决于库。 |
| 8. 成熟度 | **Alpha，无 RC/稳定线。** 2026-09-09 仍在修 density 与复杂文本对齐。不能当生产架构默认。 |
| 9. 落地成本 | 高。要新建 JVM 文档生产服务、文档版本协议、缓存、签名、失败回退、安全评审。客户端接入本身不重。 |
| 10. 风险 | API 不稳；Compose 原语覆盖不全；远程文档攻击面；无官方 SLA；依赖版本必须和 Compose BOM 对齐。 |
| 11. 大型商业 App | **核心交易 / 主导航 Hold。** 营销卡片、活动落地、远程表盘/Glance 类表面可以做 **2 周 spike**。不要用它替换 Design System。 |

Navigation 3：稳定线 **1.1.7**，**1.2.0-rc01（2026-09-09）**。Deep link serializer 与 `BackStackMatcher` 是增量能力。推荐仍是 **新 Compose 流程 Adopt**，不重写迁移指南。

Metro：**1.4.2（2026-08-13）**。实验性 `metro.enableSuspendProviders`、Circuit `@SubCircuitInject`。编译税故事没变，推荐仍 **单 feature Trial**。不重写 1.0 分析。

KMP 默认结构无新文档。AGP 9.4 增加 incubating `KotlinHierarchyBuilder.withAndroid()`，给已有 KMP 仓作 Assess 附件，不单独升级推荐。

## Engineering Productivity

### AGP 9.4.0：AGP 10 的真实预演版本（Adopt）

上一周期把「升 9.3」写成 Adopt。那条过时了。**9.4.0 才是当前 9.x 稳定线**（2026-09，notes 2026-09-03），最高 API 37，**Gradle 最低 9.6.0**（可跟到 9.7.1）。

相对 9.3，9.4 多了大型仓真正缺的东西：

```properties
android.newDsl=true
android.builtInKotlin=true
# 只给还没迁完的遗留模块。10.0 会删掉。
android.newDsl.optOut=:legacy-lib
```

没有模块级 opt-out 时，100+ 模块仓只能全局关 new DSL，AGP 10 审计会失真。有了 opt-out，可以 **默认锁死新 DSL，按模块还债**。

DFM：9.4 检查 base app 与 dynamic feature 的 flavor dimension 是否 1:1，默认 warning。`android.enforceDynamicFeatureVariantMatching=true` 升为 error。**10.0 默认失败。** 有 DFM 的仓现在就要列 mismatch，不要等发布窗口。

Incubating、本周期不 Trial：

- `AgpTestSuite`：按 variant 声明 host/device 测试套件，可挂 JUnit Engine。测试架构信号，文档不够。
- `R8Plugin`：R8 从 AGP 内拆成独立插件。构建系统拆分信号，不要现网切。

Isolated Projects：跟 **Gradle 9.7.1**（官方要求避开 9.7.0）。仍 incubating，**不要打生产包**。推荐不变，不重写 1.9× sync 数字。

## Performance

### Android 17 Memory Limiter（Adopt 遥测 / Assess 优化）

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | 一个泄漏或吃内存的前台/FGS 进程会逼 LMK 杀掉一堆无辜缓存进程，设备变慢、电耗升高、用户丢状态。 |
| 2. 为什么现在出现 | 内存涨价，新机 RAM 不再单向变大。Android 17 用 cgroup v2 给每个应用进程设预算。2026-08-19 博文把范围从 Pixel 扩到「未来一年 OEM 4–16GB」。行为页 2026-09-02 仍在更新。 |
| 3. 技术原理 | 按设备 RAM 档选择 `memory.high` + swap（前台更宽、不可见更紧）。超限后内核先回收 file-backed、把匿名页打进 zRAM；继续涨则杀进程。应用 **没有 API 查询自己的限额**。 |
| 4. 对比现有方案 | 对比 LMK：LMK 看全局压力；Limiter 在系统还不饿的时候就能卡/杀你。对比 `onTrimMemory`：那是自愿释放；Limiter 是硬预算。对比 Java heap OOM：这是进程级 anon+swap，bitmap / native / 多进程都算。 |
| 5. 性能收益 | 做好了：少 zRAM 抖动，帧时间更稳。做不好：先卡顿再死，用户看成「卡 + 闪退」。这是防御性收益，不是加速彩票。 |
| 6. 工程效率收益 | 现场终于能归因。`ApplicationExitInfo.getDescription()` 含 `MemoryLimiter:AnonSwap`（reason 常是 `REASON_OTHER`）。Crashlytics 20.1.0 增加 OOM / limiter 调试数据。Play vitals 增加 Memory Usage（Anon RSS + swap）。`ProfilingManager` 的 `TRIGGER_TYPE_ANOMALY` 可在击中限额时抓 heap dump。 |
| 7. 稳定性收益 | 高。沉默杀死没有堆栈，不接 ExitInfo 会表现为「随机进程死亡」。接上之后泄漏和异常会话能进崩溃队列。 |
| 8. 成熟度 | Pixel Android 17 已执法。OEM 配置各异。`am memory-limiter` 可在已执法设备上 ignore / manual / status。 |
| 9. 落地成本 | 遥测：低（几天）。优化：中高（bitmap、泄漏、进程拆分、R8 full mode、`onTrimMemory`）。 |
| 10. 风险 | 限额不可读，实验室高 RAM / 4KB 页设备会漏报。`am memory-limiter` 在未执法设备上无效。误把所有后台死进程都怪到 Limiter。 |
| 11. 大型商业 App | **必须做遥测。** 图多、长会话、播放器、多 WebView、自管 bitmap 的应用还要做限额加压回归。 |

16 KB：**截止日期更正为 2027-02-01**。上一周期写成 May 2026 已过，与现行 Play 文档不符。合规动作不变，不重写对齐教程。

R8：9.3 的 `:app:analyzeReleaseR8Config` 仍是 keep 反馈环（Trial）。9.4 `R8Plugin` 只 Assess。官方 2026-06 记忆体文再次强调 full R8（Monzo：ANR -35%、冷启动 +30%），这是执行问题，不是新技术。

## New Technology

只进本周期雷达：

1. **Remote Compose（alpha19，2026-09-09）** — 近 7 天版本 + 近 90 天公开 API 加速。官方 SDUI，不是又一篇 Clean Architecture 博客。
2. **AGP 9.4 `newDsl.optOut` + DFM 1:1** — 近 30 天稳定线前进。改变 AGP 10 审计的落地版本。
3. **Memory Limiter 工程化** — 近 30 天官方博文把 OEM 铺开写成时间表。新的是遥测与加压方法，不是「少用内存」口号。

未收录：Declarative Gradle（仍 experimental）、又一篇垂直切片、无数字的新 MVI、Benchmark 1.5 `requireAot`（稳定线未定）。

## Watchlist Diff

详见 `diffs/engineering/2026-09-11.md`。

- **Added：** Remote Compose；Memory Limiter；AGP 9.4 DFM parity / AgpTestSuite / R8Plugin。
- **Updated：** AGP 9.3 → 9.4；Metro 1.0 → 1.4.2；Nav3 → 1.2.0-rc01；Isolated Projects → Gradle 9.7.1；16KB 截止 2027-02-01。
- **Removed：** 无。
- **No rewrite：** Isolated Projects、Metro 推荐、CC、Baseline/Startup Profile、Circuit Hold。

## Recommendation

| 技术 | 评级 | 说明 |
| --- | --- | --- |
| AGP 9.4 + `android.newDsl=true` + `android.builtInKotlin=true` | **Adopt** | 用 `newDsl.optOut` 隔离遗留模块。无 Kotlin 模块 `enableKotlin = false`。 |
| Configuration Cache | **Adopt** | Isolated Projects 前置。 |
| Navigation 3（新 Compose 流程） | **Adopt** | 1.2 RC，可与 Nav2 并存。 |
| Baseline + Startup Profile CI | **Adopt** | Require 模式门禁。 |
| 16 KB | **Adopt** | 截止 2027-02-01，不是 May 2026。 |
| Memory Limiter 遥测（ExitInfo / vitals / Crashlytics） | **Adopt** | 先看见，再优化。 |
| Isolated Projects | **Trial** | 仅本地 / IDE sync / 非生产 CI。用 9.7.1。 |
| Metro 1.4 单 feature | **Trial** | 验证编译时间与 Hilt interop。 |
| AGP 9.3/9.4 R8 analyzer + keepRules source set | **Trial** | 成本低。 |
| Remote Compose（活动/卡片/远程表面） | **Assess** | 2 周 spike，不进核心。 |
| AGP 10 第三方插件盘点 | **Assess** | 现在列清单。 |
| DFM 1:1 flavor | **Assess** | 有 DFM 就开 warning→error。 |
| KMP 新默认结构 | **Assess** | 仅已有或计划 KMP 的仓。 |
| Memory Limiter 全盘内存改造 | **Assess** | 等遥测证明击中再开专项。 |
| Circuit 全量替换 MVVM | **Hold** | 无新平台压力。 |
| Isolated Projects 打生产包 | **Hold** | 官方未背书。 |
| Remote Compose 进核心流程 | **Hold** | Alpha。 |
| AgpTestSuite / R8Plugin 现网 | **Hold** | Incubating。 |

## PoC Candidates

按投入产出只开这 3 个。不要并行开 10 个。

1. **AGP 9.4 + 模块级 new DSL 审计（3–5 天）**  
   升到 AGP 9.4.0 + Gradle 9.7.1。全仓 `android.newDsl=true`、`android.builtInKotlin=true`。对编不过的模块写 `android.newDsl.optOut`，同时扫 `applicationVariants` / `BaseExtension` / `kotlin-android`。有 DFM 则打开 `android.enforceDynamicFeatureVariantMatching=true` 看谁爆。成功标准：debug 能编过，opt-out 模块清单有主，第三方插件标「已兼容 / 可升级 / 必须替换」。这是上一周期「升 9.3」PoC 的修正版，不要并存两套。

2. **Memory Limiter 可见性 PoC（3–5 天）**  
   现网：解析 `ApplicationExitInfo`，把含 `MemoryLimiter:AnonSwap` 的退出打进稳定性看板；确认 Crashlytics ≥ 20.1.0。实验室：在 Android 17 / 已执法设备上 `am memory-limiter status`，再 `manual <pid> <MB>` 压主路径（启动、信息流、播放器）。成功标准：能区分 limiter kill 与普通 LMK/OOM，并至少复现一条可修的泄漏或超大 bitmap。

3. **Remote Compose 非核心表面 spike（1–2 周）**  
   选一张运营卡片或远程表面，不用主导航。JVM 模块出 document，App 用 `remote-player-view` 播放，必须有签名校验、缓存和本地 Compose 降级。成功标准：改服务端文案/布局能在不发版情况下出现；文档损坏时落到本地 UI。做不到或 API 周级破裂就 Hold，不要扩面。

Isolated Projects 与 Metro 单模块 PoC 仍有效，但本周期不重复立项——字段没变。

## Sources

- https://developer.android.com/jetpack/androidx/releases/compose-remote （1.0.0-alpha19，2026-09-09）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes （Last updated 2026-09-03）
- https://developer.android.com/build/releases/gradle-plugin-roadmap （Last updated 2026-07-22）
- https://developer.android.com/reference/tools/gradle-api/9.4/com/android/build/api/dsl/AgpTestSuite
- https://developer.android.com/reference/tools/gradle-api/9.4/com/android/build/gradle/R8Plugin
- https://docs.gradle.org/9.7.1/release-notes.html
- https://docs.gradle.org/current/userguide/isolated_projects.html
- https://android-developers.googleblog.com/2026/08/app-broader-memory-limits.html （2026-08-19）
- https://developer.android.com/blog/posts/prioritizing-memory-efficiency-essential-steps-for-android-17 （2026-06-02）
- https://developer.android.com/about/versions/17/behavior-changes-all （Last updated 2026-09-02）
- https://source.android.com/docs/core/perf/memory-limiter
- https://developer.android.com/jetpack/androidx/releases/navigation3 （1.2.0-rc01，2026-09-09）
- https://zacsweers.github.io/metro/latest/changelog/ （Metro 1.4.2，2026-08-13）
- https://developer.android.com/guide/practices/page-sizes （Play 16KB 截止 2027-02-01）
