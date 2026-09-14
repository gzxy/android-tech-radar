# Android Official Daily Report

Date: 2026-09-14  
Check type: Incremental vs 2026-09-10 baseline  
Previous snapshot: `snapshots/android-official/2026-09-10/`

## 1. Executive Summary

1. **稳定工具链与 Play 政策本周没有新的强制变化。** Studio Quail 4、AGP 9.4.0、Gradle 9.7.1、Kotlin 2.4.20、KSP 2.3.12、NDK r30、Compose UI 1.12.1、Benchmark 1.5.0 均未前进。不要把 2026-09-10 的 Adopt 项再当新任务下发。
2. **预览通道：Android Studio Rabbit 1 Canary 5（2026-09-10）配对 AGP 9.5.0-alpha05。** 这是 Canary 修复包，不是 AGP 10，也不是稳定构建线。生产工程 **Hold**。
3. **Compose Material3 1.5.0-alpha28 有 alpha-only API 调整**（Slider/ToggleButton/SecureTextField）。1.4.0 稳定线未动。只有已经跟 1.5 alpha 的模块需要看。
4. **Kotlin 2.5.0 EAP 仍未开；KSP 仍无显式 2.4.20 配对号；Navigation3 仍停在 1.2.0-rc01。** 这些是上一轮已登记的观察项，本周没有解锁条件。
5. **Android 17 仍是 Beta 4.1。** 全量行为页与 target 37 页均未在 2026-09-02 之后更新。

## 2. Important Changes

| Technology | Change | Impact | Recommendation |
|---|---|---|---|
| Android Studio Rabbit 1 | Canary 4 → Canary 5（2026-09-10）；Compose Preview / 本地 Gemini Agent UI 修复 | 仅 Canary 用户；稳定线 Quail 4 不受影响 | **Hold** |
| AGP 9.5 Preview | Maven 最新预览 `9.5.0-alpha05`，与 Canary 5 配对 | 确认 9.4 之后还有 9.5 预览线，但无稳定发行说明，不能当 AGP 10 替代 | **Hold** |
| Compose Material3 | 1.5.0-alpha27 → 1.5.0-alpha28 | 仅 alpha：无状态 Slider 废弃、ToggleButton overload 删除、SecureTextField 默认 obfuscation 改为 `System` | **Hold**（稳定 1.4.0 不变） |

## 3. Breaking Changes

无新的稳定线 / Play / 平台 Breaking Change。

Material3 **1.5.0-alpha28（预览，不影响 1.4.0）**：

- 删除已废弃 `ToggleButton` overload。
- 废弃无状态 `Slider` / `RangeSlider`，改为 `SliderState` / `RangeSliderState`（`startValue` / `endValue`）。
- `SecureTextField` 默认 `TextObfuscationMode` 从 `RevealLastTyped` 改为 `System`。

AGP 10 删除 legacy Variant API 的路线图未改（roadmap 仍 Last updated 2026-07-22）。这不是本周新消息，不重复展开。

## 4. Android Engineering Impact

本周没有改变上架门槛、默认工具链或平台行为。工程影响是负向确认：

- 生产构建应继续停在 **Studio Quail 4 + AGP 9.4.0 + Gradle 9.7.1**。不要因为看到 9.5 alpha 就提前跳。
- AGP 10 迁移准备工作（消 `applicationVariants` 警告、打开 `android.newDsl=true`）仍以 9.4 为载体，9.5 alpha 不提供新的官方迁移开关。
- Compose / Navigation3 / Kotlin 升级窗口未打开：没有新的稳定配对版本。
- Play target 36 与 16KB 截止日期未改动。未完成的工作继续按 2026-09-10 报告执行，本周不追加新政策。

## 5. Watchlist Diff

### Added

- **Android Gradle Plugin 9.5 Preview**（`9.5.0-alpha05`）。首次单独建档。上一轮 Canary 4 已带 9.5.0-alpha04，但未从 AGP 9.4 稳定条目中拆出。

### Updated

- Android Studio Rabbit 1：Canary 4 → **Canary 5**
- Compose Material3：1.5.0-alpha27 → **1.5.0-alpha28**
- 其余条目：仅刷新 Last Checked；稳定版本号未变

### Removed / Deprecated

无条目删除。无新的官方稳定线废弃。

### No Significant Change

Android 16/17、Studio Quail 4、AGP 9.4.0、Gradle 9.7.1、Kotlin 2.4.20、KSP 2.3.12、Coroutines 1.11.0、Compose UI 1.12.1、Navigation3、Benchmark、NDK r30、R8、Baseline Profile、16KB、Play Target SDK、App Startup、Navigation 2.10.0、Room3 3.0.2、Lifecycle 2.12.0、CameraX 1.6.2。

## 6. Recommended Actions

**本周没有新的生产行动。** 不要把上一轮 Adopt 项再排一次期。

仅在以下窄场景才需要人看一眼：

1. **已经在用 Studio Rabbit Canary 的人：** 升到 Canary 5。稳定通道用户不要动。
2. **已经在跟 Material3 1.5 alpha 的模块：** 按 1.5.0-alpha28 改 Slider / ToggleButton / SecureTextField。1.4.0 工程忽略。
3. **构建平台组：** 把 AGP 9.5 预览线加入观察，等官方 9.5 发行说明或 10.0 时间表变化；不要用 alpha05 做主干。

上一轮仍有效、但**不是本周新发现**的进行中工作（不重复评分）：Play target 36 / 16KB 对齐 / AGP 9.4 New DSL 消警告 / 有 native 时显式 NDK r30。

评分（仅本周增量）：

| 变化 | 工程 | 性能 | 稳定 | 效率 | 范围 | 成本 | 成熟度 | 结论 |
|---|---|---|---|---|---|---|---|---|
| Studio Rabbit Canary 5 | 低 | 低 | 低 | 中 | Canary 用户 | 低 | Canary | Hold |
| AGP 9.5.0-alpha05 | 中 | 低 | 低 | 低 | 构建预览 | 高 | Alpha | Hold |
| Material3 1.5.0-alpha28 | 低 | 低 | 低 | 低 | 1.5 alpha 模块 | 低 | Alpha | Hold |

## 7. Sources

一手资料（本次结论回源到以下页面 / Maven metadata，不以搜索摘要为准）：

- https://developer.android.com/studio/releases （Quail 4 \| 2026.1.4）
- https://developer.android.com/studio/preview （Rabbit 1 \| 2026.2.1 Canary 5；Last updated 2026-09-10）
- https://developer.android.com/studio/preview/features （Last updated 2026-09-09）
- https://developer.android.com/latest-updates （Rabbit 1 Canary 5，September 10, 2026）
- https://androidstudio.googleblog.com/ （Rabbit 1 Canary 5 + AGP 9.5.0-alpha05，2026-09-10）
- https://developer.android.com/build/releases/about-agp （AGP 9.4.0；Last updated 2026-09-03）
- https://developer.android.com/build/releases/agp-9-4-0-release-notes （Last updated 2026-09-03）
- https://developer.android.com/build/releases/gradle-plugin-roadmap （Last updated 2026-07-22）
- https://dl.google.com/android/maven2/com/android/tools/build/gradle/maven-metadata.xml （latest `9.5.0-alpha05`，lastUpdated 20260910182340）
- https://docs.gradle.org/current/release-notes.html （Gradle 9.7.1）
- https://services.gradle.org/versions/current （9.7.1）
- https://kotlinlang.org/docs/releases.html （2.4.20；Last updated 2026-09-09）
- https://kotlinlang.org/docs/eap.html （No preview versions；2026-09-04）
- https://github.com/JetBrains/kotlin/releases/tag/v2.4.20
- https://github.com/google/ksp/releases/tag/2.3.12
- https://github.com/Kotlin/kotlinx.coroutines/releases/tag/1.11.0
- https://developer.android.com/jetpack/androidx/releases/compose （Last updated 2026-09-10）
- https://developer.android.com/jetpack/androidx/releases/compose-ui （1.12.1 / 1.13.0-alpha03）
- https://developer.android.com/jetpack/androidx/releases/compose-material3 （1.5.0-alpha28，2026-09-09）
- https://developer.android.com/jetpack/androidx/releases/navigation3 （1.2.0-rc01）
- https://developer.android.com/jetpack/androidx/releases/benchmark （1.5.0）
- https://developer.android.com/ndk/downloads （r30；Last updated 2026-09-08）
- https://github.com/android/ndk/releases/tag/r30
- https://developer.android.com/google/play/requirements/target-sdk （Last updated 2026-09-01）
- https://developer.android.com/guide/practices/page-sizes
- https://developer.android.com/about/versions/16/behavior-changes-16 （Last updated 2026-09-01）
- https://developer.android.com/about/versions/17/behavior-changes-all （Last updated 2026-09-02）
- https://developer.android.com/about/versions/17/behavior-changes-17 （Last updated 2026-09-02）
