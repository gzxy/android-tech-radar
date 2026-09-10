# Android Engineering Daily Report

Date: 2026-09-10  
Window: 7 / 30 / 90 days  
Mode: first snapshot (empty radar)

## Executive Summary

本周期只保留 3 个能改变大型 Android 团队速度或稳定性的信号，不凑数量。

1. **Gradle Isolated Projects**（9.7，2026-08-06，孵化）：配置阶段并行化。Android 5000+ 模块仓 Android Studio sync 约 1.9×；AndroidX 1000+ 模块 Gradle 部分 sync 约 1.4×。Configuration Cache 是前置条件。官方明确：**不要用来打生产包**。
2. **AGP 10.0 锁死窗口**（预计 2026 下半年）：`android.newDsl=false` / `android.builtInKotlin=false` 和 `applicationVariants` 将被删除。AGP 9.3（2026-07，文档 2026-09-03 更新）已提供 R8 `optimization` DSL、`keepRules` source set、以及不打包就能跑的 `:app:analyzeReleaseR8Config`。
3. **Metro 1.0**（2026-04-27）：Kotlin compiler plugin DI，去掉 KSP/KAPT 源码生成。迁移自 Dagger+Anvil+KSP 的团队报告编译耗时下降 **50–80%**。对大型商业 App 是「编译器成本」问题，不是架构时尚。

核心判断：能让团队更快的，不是再写一套 MVI，而是 **先把 Configuration Cache 做实 → 本地试 Isolated Projects → 用 AGP 9.3 把 new DSL / built-in Kotlin 跑干净，赶在 AGP 10 前清掉第三方插件债**。性能侧，Startup Profile + R8 analyzer 的投入产出比仍然高于再挖一层 Compose 微优化。

## Architecture

### Metro 1.0（Trial）

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | Dagger/Hilt + Anvil + KSP/KAPT 的多工具链兼容成本和源码生成编译税。 |
| 2. 为什么现在出现 | Kotlin 2.x FIR/IR 足够稳，才能把图验证和代码生成放进编译器插件；1.0 锁定 runtime ABI。 |
| 3. 技术原理 | FIR 做分析与类头生成，IR 做其余 codegen；无 KSP 额外 pass；增量编译走 kotlinc 原生设施。 |
| 4. 对比现有方案 | 对比 Hilt/Dagger：少一层 annotation processor，多 compile-time 环检测/作用域校验。对比 kotlin-inject：聚合（Anvil 风格 contributes）是一等能力，且有 Dagger interop。 |
| 5. 性能收益 | 运行时无反射/HashMap 查找。主要收益在构建，不在帧时间。 |
| 6. 工程效率收益 | 单一插件替代 Dagger+Anvil+KSP 版本矩阵；`createDynamicGraph()` 便于测试替换。 |
| 7. 稳定性收益 | 编译期环、作用域、multibinding 重复 key 校验。稳定性指「装错依赖编不过」，不是崩溃率。 |
| 8. 成熟度 | Runtime ABI 稳定。作者维护 compiler/IDE 兼容窗口（多版本 Kotlin + 5 个 AS + 2 个 IDEA）。不能混用不同 Metro 处理版本。 |
| 9. 落地成本 | 中高。Hilt 全家桶（WorkManager、Navigation、ViewModel 扩展）要逐项替换或走 interop。`metrox-android` 要求 minSdk 28。 |
| 10. 风险 | Compiler plugin 跟 Kotlin 版本绑定；IDE 诊断仍有 registry flag；Hilt 生态插件可能暂时不兼容 Isolated Projects/AGP 10。 |
| 11. 大型商业 App | **适合做 PoC，不适合本周全量切。** 先选一个无 Hilt 特殊入口的 feature 模块。 |

### Navigation 3 与 KMP 默认结构（Adopt / Assess）

Nav3（2025-11-19 稳定）把 back stack 变成应用拥有的 Compose state，适合 list-detail / 多窗格，不再是「新发现」，但是 **新 Compose 流程的默认选择**。KMP 默认结构（2026-05）把 `shared` 与 `androidApp` 拆开，直接对应 AGP 9.0「KMP 模块不能再挂 Android application plugin」。已有 KMP 仓必须评估；纯 Android 仓不必为了对齐结构而拆。

Circuit 仍放在 Evaluate：和 Metro 的 opt-in codegen 组合漂亮，但会改 Presenter 边界，和现有 MVVM 冲突。没有 30 天内的平台级解锁，不升级推荐。

## Engineering Productivity

### Gradle Isolated Projects（Trial）

| # | 分析 |
| --- | --- |
| 1. 解决什么问题 | Configuration Cache 只能跳过「配置未变」的重复构建。IDE sync、改 build logic、第一次 CI 配置，仍然要配完所有 project。 |
| 2. 为什么现在出现 | Gradle 9.7（2026-08-06）从 experimental 升到 incubating。Google / JetBrains 插件已兼容；Now in Android 已能开。 |
| 3. 技术原理 | 禁止跨 project 读可变状态，于是配置可并行。当前收益主要是并行配置；后续才是按需跳过未涉及的 project、更细粒度 configuration cache。 |
| 4. 对比现有方案 | 对比只开 CC：CC 加速「同输入再跑」；Isolated Projects 加速「必须配置」的那一次，尤其是 Studio sync。 |
| 5. 性能收益 | 官方实测：Gradle 自身 300 模块 IDE sync 中位 84s→47s（1.8×）；2500 模块 Java 仓 warm IDEA sync 3m25s→2m13s；**5000+ 模块 Android 仓 Studio sync 5m09s→2m44s（1.9×，并行度 32）**；AndroidX 1000+ 模块 Gradle 部分 4m00s→2m47s。CLI 收益小于 IDE，因为 task graph 发现仍是串行。 |
| 6. 工程效率收益 | 每天多次 sync 的大型仓，单次省 1–3 分钟，是 DevXP 级收益。 |
| 7. 稳定性收益 | 约束本身减少隐式跨模块配置耦合。当前孵化期约束还可能加严。 |
| 8. 成熟度 | Incubating。官方：**不要用来构建生产产物**。适合本地和部分 CI dry-run。 |
| 9. 落地成本 | 中。必须先 CC 兼容。第三方插件是主阻力。可用 diagnostics 模式一次收集违规。属性：`org.gradle.isolated-projects=true`。 |
| 10. 风险 | 插件不兼容直接失败；生产产物正确性未背书；IDE 还需后续版本才能吃满并行。 |
| 11. 大型商业 App | **非常适合。** 这是本周期对「团队变快」贡献最大的一项。 |

### AGP 9.3 / AGP 10.0（Adopt + Assess）

AGP 9.0（2026-01）默认 built-in Kotlin，并引入 `com.android.kotlin.multiplatform.library`。AGP 9.3 需要 Gradle 9.5.0，支持 API 37。AGP 10.0 完成惰性、CC / Project Isolation 兼容的构建模型，删除：

- `applicationVariants` / `libraryVariants` / 直接拿 Task
- `android.newDsl`、`android.builtInKotlin` 退出开关

可在 9.x 上提前锁死行为：

```properties
android.newDsl=true
android.builtInKotlin=true
```

9.4+ 可用 `android.newDsl.optOut=:legacy-lib` 做模块级缓冲，10.0 会删掉。无 Kotlin 源码的模块应 `android { enableKotlin = false }`，去掉无用的 Kotlin compile 和 stdlib。

**对大型商业 App：** 现在不做插件盘点，AGP 10 会变成发布阻断。这是工程风险，不是性能彩票。

## Performance

### AGP 9.3 R8 Analyzer + keepRules source set（Trial）

`:app:analyzeReleaseR8Config` 不走完整 APK/AAB 打包，专门缩短 keep 规则反馈环。`src/<variant>/keepRules/*.keep` 让规则成为 source set，库和 KMP consumer rules 终于有正式位置。`optimization {}` 打开后同时启用代码优化和优化资源压缩，不再手写默认 Android keep 文件。

这对包体、启动 DEX 布局、反射/序列化崩溃都有间接收益。成熟度：随 AGP 9.3 稳定发布，legacy DSL 仍可用，迁移成本低。

### Baseline / Startup Profile（Adopt，非新发明）

没有 7 天内的平台新 API。仍然是：Baseline 约 30% 代码执行；R8 改写规则后再加约 15%；Startup Profile 再给启动约 15%（大包更明显）。2026 的差距在 **CI 是否每次发版重生、并用 `BaselineProfileMode.Require` 卡住缺失 profile**，以及 Compose 路径是否调用 `ReportDrawn` / `ReportDrawnWhen`。不把「再写一遍 Baseline 教程」当成新技术。

### 16 KB（Adopt / 合规基线）

May 2026 截止日后不应再当「发现」。工具基线：AGP ≥ 8.5.1（实际应在 9.3）、NDK r28+、未压缩 `.so` 16 KB zip-align。纯 Kotlin 应用风险低；带 SDK / 游戏引擎 / SQLCipher 的应用仍要在 **16 KB 系统镜像** 上跑启动 Macrobenchmark，4 KB 设备数字会骗人。

## New Technology

只记录本周期值得进雷达的新技术，而不是清单扩写。

1. **Isolated Projects（Gradle 9.7）** — 唯一进入「近 30 天 + 官方晋升 + 有 Android 万级模块实测」的工程能力。
2. **AGP 9.3 R8 Configuration Analyzer / keepRules source set** — 近 7–90 天文档仍在更新（2026-09-03），是可立刻试的性能工程工具。
3. **Metro 1.0** — 90 天窗口外一点，但 1.0 是质变点，且直接回答「怎样让编译更快」。

未收录：又一篇 Clean Architecture / 垂直切片博客、通用 SDUI 教程、无官方数据的「新 MVI 框架」。

## Watchlist Diff

无历史 snapshot。本次全部为 **Added**。详见 `diffs/engineering/2026-09-10.md`。

若下一周期 Isolated Projects 仍是 incubating、无新官方数字、推荐不变：**不要重写本报告**。

## Recommendation

| 技术 | 评级 | 说明 |
| --- | --- | --- |
| AGP 9.3 + `android.newDsl=true` + `android.builtInKotlin=true` | **Adopt** | AGP 10 的预演。无 Kotlin 模块关 `enableKotlin`。 |
| Configuration Cache | **Adopt** | Isolated Projects 前置，不是可选项。 |
| Navigation 3（新 Compose 流程） | **Adopt** | 稳定，可与 Nav2 并存迁移。 |
| Baseline + Startup Profile CI | **Adopt** | 用 Require 模式做门禁，不要手养 profile。 |
| 16 KB | **Adopt** | 合规，不是优化课题。 |
| Isolated Projects | **Trial** | 仅本地 / IDE sync / 非生产 CI。 |
| AGP 9.3 R8 analyzer + keepRules source set | **Trial** | 成本低，反馈环短。 |
| Metro 1.0（单 feature） | **Trial** | 验证编译时间和 Hilt interop，不全量。 |
| AGP 10.0 第三方插件盘点 | **Assess** | 现在列清单，避免发布窗口被插件卡住。 |
| KMP 新默认结构 / Android KMP library plugin | **Assess** | 仅已有或计划 KMP 的仓。 |
| Circuit 全量替换 MVVM | **Hold** | 无新平台压力。 |
| Isolated Projects 打生产包 | **Hold** | 官方未背书。 |

## PoC Candidates

按投入产出排序，建议实际验证这 3 个，不要并行开 10 个。

1. **Isolated Projects 本地 PoC（1 周）**  
   前置：Configuration Cache 在 warn→fail。打开 `org.gradle.isolated-projects=true`（或 diagnostics），量 Android Studio sync 与 `--dry-run` 配置时间，记录不兼容插件。成功标准：sync 下降 ≥20%，且无静默错误。不用于 release 流水线。

2. **AGP 10 就绪审计（3–5 天）**  
   升到 AGP 9.3.x + Gradle 9.5+。全仓 `android.newDsl=true`、`android.builtInKotlin=true`。CI 扫 `applicationVariants` / `BaseExtension` / `kotlin-android`。对每个第三方 Gradle 插件标「已兼容 / 可升级 / 必须替换」。成功标准：零 opt-out 能编过 debug。

3. **Metro 单模块 PoC（1–2 周）**  
   选一个无 ContentProvider 启动依赖、无 Hilt WorkManager 的 feature。对比该模块 compileKotlin 与全量 assemble。成功标准：该模块编译时间明显下降，且 Dagger interop 能接到现有 AppComponent。达不到就 Hold，不要扩面。

可选第 4（若还有带宽）：把一条 release 构建改到 `optimization {}` + `analyzeReleaseR8Config`，看 keep 规则噪音和包体，不作为架构变更。

## Sources

- https://blog.gradle.org/introducing-isolated-projects (2026-08-06)
- https://docs.gradle.org/current/release-notes.html (Gradle 9.7.0)
- https://docs.gradle.org/current/userguide/isolated_projects.html
- https://blog.gradle.org/isolated-projects-in-gradle-team
- https://developer.android.com/build/releases/gradle-plugin-roadmap (updated 2026-07-22)
- https://developer.android.com/build/releases/agp-9-3-0-release-notes (updated 2026-09-03)
- https://developer.android.com/build/releases/agp-9-0-0-release-notes
- https://developer.android.com/build/migrate-to-built-in-kotlin
- https://blog.jetbrains.com/kotlin/2026/01/update-your-projects-for-agp9/
- https://blog.jetbrains.com/kotlin/2026/05/new-kmp-default-structure/
- https://kotlinlang.org/docs/multiplatform/multiplatform-project-agp-9-migration.html
- https://www.zacsweers.dev/metro-is-stable/ (2026-04-27)
- https://github.com/ZacSweers/metro/releases/tag/1.0.0
- https://developer.android.com/blog/posts/jetpack-navigation-3-is-stable (2025-11-19)
- https://developer.android.com/topic/performance/baselineprofiles/overview
- https://developer.android.com/guide/practices/page-sizes
