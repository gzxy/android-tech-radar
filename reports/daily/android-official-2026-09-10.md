# Android Official Daily Report

Date: 2026-09-10  
Check type: Initial baseline + current-enforcement scan  
Previous snapshot: none

## 1. Executive Summary

1. **Play target API 36 已在强制窗口内。** 2026-08-31 起新应用与更新必须 target Android 16；未完成的应用只能走延期到 2026-11-01。这不是预告，是上架阻断。
2. **16KB 页大小还有约 5 个月。** target API 35+ 的 64-bit 更新若 ELF 未 16KB 对齐，2027-02-01 起无法上架。含 so 的应用必须现在排期，而不是等截止日期。
3. **工具链刚完成一轮稳定发布：Studio Quail 4 + AGP 9.4.0 + Kotlin 2.4.20 + NDK r30。** AGP 9.4 是升级到 AGP 10 前的最后准备窗口——10.0 将删除 legacy Variant API。
4. **Android 17（API 37）Beta 行为变化页仍在更新。** 内存限额与后台音频硬化会在用户设备升级后影响所有应用，不依赖你是否已经 target 37。
5. **KSP 2.3.12 / Compose 1.12.1 / Benchmark 1.5.0 于 2026-09-09 发布。** 不要把 Kotlin 2.4.20 和 KSP 拆开升；自定义 annotation processor 需要评估 backing fields opt-in。

## 2. Important Changes

| Technology | Change | Impact | Recommendation |
|---|---|---|---|
| Google Play Target SDK | 2026-08-31 起必须 target API 36；可延期至 2026-11-01 | 上架阻断；target 36 触发 edge-to-edge、Predictive Back、大屏自适应 | **Adopt** |
| 16KB Page Size | 2027-02-01 起 target 35+ 的 64-bit 更新必须 16KB 对齐 | Native / 第三方 SDK so 未对齐则无法更新 | **Adopt** |
| Android Gradle Plugin 9.4.0 | 支持 API 37；要求 Gradle 9.6+；为 AGP 10 提供 `newDsl.optOut` 与 DFM 1:1 预警 | 自定义 Gradle 插件 / DFM 工程在 AGP 10 会直接编译失败 | **Trial**（先消警告） |
| Android Studio Quail 4 | 2026.1.4 稳定，Quail 最终版；内置 23 个 Android skills | 旧 Studio 将失去 Cloud services；Otter 2 已 deprecated | **Adopt** |
| Kotlin 2.4.20 | 2026-09-07 tooling release；Gradle 到 9.7；`when` invokedynamic 默认开 | 编译器/工具链变更，语言不是大版本 | **Trial** |
| KSP 2.3.12 | 2026-09-09；最低 AGP 8.12；backing fields 需双重 opt-in | 自定义 processor 与 Room/Hilt 等生成链路 | **Assess** |
| NDK r30 LTS | 2026-09-08；`30.0.16248370`；AGP 9.4 默认仍是 28.2 | 16KB 与 LTO 稳定性；默认不会自动跟上 | **Adopt**（有 native 时） |
| Android 17 | Beta 4.1；内存限额、后台音频硬化、本地网络权限、CT/ECH 默认 | 设备升级后全量生效部分行为；target 37 更严 | **Assess** |
| Jetpack Compose 1.12.1 | 2026-09-09 补丁；1.12.0 含可变字体 / WCG | UI 稳定线前进，非 breaking | **Trial** |
| Benchmark 1.5.0 | 2026-09-09；UiAutomator 2.4；`requireAot` 默认 true | 性能 CI 可能因默认值变严而失败 | **Trial** |
| Navigation3 1.2.0-rc01 | 2026-09-09 进入 RC | Compose 导航迁移窗口打开 | **Assess** |
| Gradle 9.7.1 | Isolated Projects incubating；官方要求避开 9.7.0 | AGP 9.4 最低 9.6.0，可跟到 9.7.1 | **Trial** |

## 3. Breaking Changes

### 已生效 / 正在咬人

- **Play target 36：** 未达标更新无法提交。target 36 后 `windowOptOutEdgeToEdgeEnforcement` 在 Android 16 设备上失效；未迁移 Predictive Back 时 `onBackPressed` 不再被调用。
- **大屏（sw>=600dp）：** target 36 忽略方向/比例/可调整大小限制（仍可 opt-out）。**target 37 将取消 opt-out。** 现在不改，明年会变成硬失败。

### 2027-02-01 硬截止

- **16KB：** 未 16KB 对齐的 `arm64-v8a` / `x86_64` `.so` 将阻止 Play 更新。Java/Kotlin-only 应用通常已兼容，但仍需 16KB 模拟器回归。

### 构建系统（AGP 10 预告，9.4 已给迁移开关）

- `applicationVariants.all` / legacy Variant API / Transform API 将在 AGP 10 删除。
- Dynamic Feature 与 base app 的 flavor dimension 必须 1:1；9.4 默认 warning，10.0 默认 error。
- `android.newDsl=false`、`android.builtInKotlin=false` 将在 10.0 失效。9.4 可用 `android.newDsl.optOut=:module` 做过渡。

### Android 17（现在就要测，即使尚未 target 37）

- 后台音频：非法生命周期调用会静默失败。
- App memory limits：泄漏/异常内存会话会被系统杀掉（`ApplicationExitInfo` 描述含 `MemoryLimiter:AnonSwap`）。
- target 37 额外：`ACCESS_LOCAL_NETWORK`、CT 默认、Native `System.load()` 必须只读、`static final` 不可反射改写、RemoteViews 内存硬限制。

### KSP 2.3.12

- 最低 AGP 8.12.0。
- 新语言特性默认关闭；processor 若只调用 `registerProcessorForNewFeatures` 或只切 `KSVisitorNext` 之一，行为未定义。

## 4. Android Engineering Impact

### 上架与合规（立刻）

Play 政策已经改变发布门槛。工程优先级应是：确认所有正式包 `targetSdk=36`，跑完 Android 16 行为变化清单（edge-to-edge、返回、大屏），再处理 16KB。延期到 11-01 只是缓冲，不是策略。

### 构建系统（本季度）

AGP 9.4 不是“可有可无的小版本”。它是官方给出的 AGP 10 预演开关：先把项目升到 9.4 + Gradle 9.6/9.7.1，打开 `android.newDsl=true` 和 `android.builtInKotlin=true`，用 `optOut` 隔离落后模块，审计第三方 Gradle 插件。等到 10.0 再迁会集中爆 `ClassCastException: cannot be cast to BaseExtension`。

### Native / 性能

有 so 的应用：不要停留在 AGP 默认 NDK 28.2。r30 是新 LTS，且 16KB 对齐必须在依赖链（含第三方 SDK）上验证。Benchmark 1.5 默认 AOT，升级后要用它重新校准启动/滚动基线，而不是沿用旧 CI 数字。

### 平台前瞻

Android 17 的内存限额和后台音频硬化，会在用户升级设备后影响现网，与 targetSdk 无关。音频、保活、本地网络扫描、动态加载 so 的模块应在 Beta 镜像上先跑一遍。

## 5. Watchlist Diff

### Added

首次建立完整官方 Watchlist（Platform 16/17、Studio、AGP、Gradle、Kotlin、Coroutines、KSP、Compose、Navigation3、R8、Baseline Profile、Benchmark、NDK、16KB、Play Target SDK、App Startup、以及 Navigation/Room3/Lifecycle/CameraX 版本锚点）。详见 `watchlist/android-official.md`。

### Updated

无（无上一份 Watchlist）。

### Removed / Deprecated

无条目删除。官方废弃信号：

- Studio Otter 2 Cloud services
- AGP legacy Variant API / `newDsl` / `builtInKotlin` opt-out（AGP 10）
- `usesCleartextTraffic`（未来版本）
- `setContentCaptureEnabled`（target 37）
- `elegantTextHeight` / edge-to-edge opt-out（target 36）

### No Significant Change

- App Startup 1.2.0
- Kotlin Coroutines 1.11.0（本周无新 release）
- profileinstaller 1.4.1

以上三项只建基线，不产出额外技术分析。

## 6. Recommended Actions

1. **本周：核对 Play Console。** 所有还在提交的应用是否已 target 36；未完成的立刻提交 2026-11-01 延期，同时排期 edge-to-edge + Predictive Back + 大屏回归。
2. **本周：盘点 native 依赖。** 用 APK Analyzer / `check_elf_alignment.sh` 扫正式包 `arm64-v8a`/`x86_64`；第三方 SDK 未对齐的开 ticket。截止日期 2027-02-01。
3. **本迭代：升 Android Studio Quail 4，并在非主干试 AGP 9.4.0 + Gradle 9.7.1。** 打开 New DSL 严格模式，列出仍依赖 `applicationVariants` 的模块和插件。
4. **有 NDK 的模块：显式 `ndkVersion = "30.0.16248370"`**，不要吃 AGP 默认 28.2。
5. **Kotlin 2.4.20 不要单独升。** 先确认 KSP / Hilt / Room / Compose Compiler plugin 的配对版本；自定义 KSP processor 评估 2.3.12 的 backing fields 迁移。
6. **性能组：在独立分支试 Benchmark 1.5.0。** 预期 `requireAot` 默认值会让旧 microbenchmark 失败，修好后再升主干。
7. **平台组：用 Android 17 Beta 镜像跑音频、内存泄漏、本地网络、动态 so 加载。** 现在测的是全量行为，不是 target 37 迁移。

评分摘要（仅对需决策项）：

| 变化 | 工程 | 性能 | 稳定 | 效率 | 范围 | 成本 | 成熟度 | 结论 |
|---|---|---|---|---|---|---|---|---|
| Play target 36 | 高 | 中 | 高 | 低 | 全应用 | 中 | 高 | Adopt |
| 16KB | 高 | 高 | 高 | 低 | Native 应用 | 中高 | 高 | Adopt |
| AGP 9.4 / 预备 10 | 高 | 中 | 中 | 中 | 构建 + 插件 | 中高 | 高（9.4）/ 中（10） | Trial |
| Studio Quail 4 | 中 | 低 | 中 | 高 | 全体开发 | 低 | 高 | Adopt |
| Kotlin 2.4.20 | 中 | 中 | 中 | 中 | 工具链 | 低中 | 高 | Trial |
| NDK r30 | 高 | 中 | 高 | 低 | Native | 中 | 高 | Adopt |
| Android 17 兼容测试 | 高 | 高 | 高 | 低 | 全应用 | 中 | Beta | Assess |
| Compose 1.12.1 | 中 | 中 | 中 | 中 | UI | 低 | 高 | Trial |
| Benchmark 1.5 | 中 | 高 | 中 | 中 | 性能 CI | 低中 | 高 | Trial |
| Navigation3 1.2 RC | 中 | 低 | 中 | 高 | 导航 | 高 | RC | Assess |
| KSP 2.3.12 | 中 | 低 | 中 | 中 | 代码生成 | 中 | 高 | Assess |

## 7. Sources

一手资料（本次结论均回源到以下页面，不以搜索摘要为准）：

- https://developer.android.com/google/play/requirements/target-sdk （Last updated 2026-09-01）
- https://developer.android.com/guide/practices/page-sizes
- https://developer.android.com/about/versions/16/behavior-changes-16
- https://developer.android.com/about/versions/17
- https://developer.android.com/about/versions/17/behavior-changes-all （Last updated 2026-09-02）
- https://developer.android.com/about/versions/17/behavior-changes-17 （Last updated 2026-09-02）
- https://developer.android.com/studio/releases （Quail 4 \| 2026.1.4）
- https://developer.android.com/studio/preview/features （Last updated 2026-09-09）
- https://developer.android.com/blog/posts/leverage-android-skills-and-gemma-4-in-android-studio-quail-4 （2026-09-01）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes （Last updated 2026-09-03）
- https://developer.android.com/build/releases/gradle-plugin-roadmap （Last updated 2026-07-22）
- https://docs.gradle.org/current/release-notes.html （Gradle 9.7.1）
- https://kotlinlang.org/docs/releases.html （Last updated 2026-09-09）
- https://kotlinlang.org/docs/whatsnew2420.html （Released 2026-09-07）
- https://github.com/JetBrains/kotlin/releases/tag/v2.4.20
- https://github.com/google/ksp/releases/tag/2.3.12 （2026-09-09）
- https://github.com/Kotlin/kotlinx.coroutines/releases/tag/1.11.0
- https://developer.android.com/jetpack/androidx/releases/compose-ui （1.12.1，2026-09-09）
- https://developer.android.com/jetpack/androidx/releases/benchmark （1.5.0，2026-09-09）
- https://developer.android.com/jetpack/androidx/releases/navigation3 （1.2.0-rc01，2026-09-09）
- https://developer.android.com/ndk/downloads （r30 LTS，Last updated 2026-09-08）
- https://github.com/android/ndk/releases/tag/r30
- https://developer.android.com/topic/performance/baselineprofiles/overview （Last updated 2026-09-01）
- https://developer.android.com/latest-updates
