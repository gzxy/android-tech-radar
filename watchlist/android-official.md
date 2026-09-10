# Android Official Watchlist

Last updated: 2026-09-10  
Check type: Initial baseline (no previous snapshot)

| Name | Category | Official URL | Repository | Current Version | Priority | First Discovered | Last Checked | Last Known Change |
|---|---|---|---|---|---|---|---|---|
| Android 16 (API 36) | Platform | https://developer.android.com/about/versions/16 | AOSP | 16 / API 36 stable | P0 | 2026-09-10 | 2026-09-10 | Play 要求自 2026-08-31 起新应用/更新必须 target API 36 |
| Android 17 (API 37) | Platform | https://developer.android.com/about/versions/17 | AOSP | 17 Beta 4.1 / API 37 | P0 | 2026-09-10 | 2026-09-10 | 全量行为变化页 2026-09-02 更新：内存限额、后台音频硬化、本地网络权限 |
| Android Studio Quail 4 | Tooling | https://developer.android.com/studio/releases | https://android.googlesource.com/platform/tools/adt/idea | Quail 4 \| 2026.1.4 stable | P0 | 2026-09-10 | 2026-09-10 | 2026-09-01 进入 stable，Quail 系列最终稳定版 |
| Android Studio Rabbit 1 | Tooling | https://developer.android.com/studio/preview/features | https://android.googlesource.com/platform/tools/adt/idea | Rabbit 1 \| 2026.2.1 Canary 4 | P2 | 2026-09-10 | 2026-09-10 | 2026-09-03 Canary；preview 页 2026-09-09 更新 |
| Android Gradle Plugin | Build | https://developer.android.com/build/releases/agp-9-4-0-release-notes | https://android.googlesource.com/platform/tools/base | 9.4.0 | P0 | 2026-09-10 | 2026-09-10 | 2026-09-01 发布；AGP 10 将强制 New Variant API |
| Gradle | Build | https://docs.gradle.org/current/release-notes.html | https://github.com/gradle/gradle | 9.7.1 | P1 | 2026-09-10 | 2026-09-10 | 2026-08-19/20 发布；Isolated Projects 进入 incubating |
| Kotlin | Language | https://kotlinlang.org/docs/releases.html | https://github.com/JetBrains/kotlin | 2.4.20 | P0 | 2026-09-10 | 2026-09-10 | 2026-09-07 tooling release；下一代 2.5.0 计划 2026-12 |
| Kotlin Coroutines | Language | https://github.com/Kotlin/kotlinx.coroutines/releases | https://github.com/Kotlin/kotlinx.coroutines | 1.11.0 | P1 | 2026-09-10 | 2026-09-10 | 2026-05-08；Android 侧无本周新 release |
| KSP | Build | https://github.com/google/ksp/releases | https://github.com/google/ksp | 2.3.12 | P0 | 2026-09-10 | 2026-09-10 | 2026-09-09：backing fields opt-in；最低 AGP 8.12.0 |
| Jetpack Compose | UI | https://developer.android.com/jetpack/androidx/releases/compose-ui | https://android.googlesource.com/platform/frameworks/support | 1.12.1 | P0 | 2026-09-10 | 2026-09-10 | 2026-09-09 发布 1.12.1；1.13.0-alpha03 同步更新 |
| Compose Material3 | UI | https://developer.android.com/jetpack/androidx/releases/compose | AndroidX | 1.4.0 stable / 1.5.0-alpha27 | P1 | 2026-09-10 | 2026-09-10 | 2026-08-26 稳定 1.4.0 |
| Navigation3 | Jetpack | https://developer.android.com/jetpack/androidx/releases/navigation3 | AndroidX | 1.1.7 stable / 1.2.0-rc01 | P1 | 2026-09-10 | 2026-09-10 | 2026-09-09 发布 1.2.0-rc01 |
| R8 | Build / Perf | https://developer.android.com/topic/performance/app-optimization/enable-app-optimization | https://r8.googlesource.com/r8 | Bundled with AGP 9.4；R8Plugin incubating | P1 | 2026-09-10 | 2026-09-10 | AGP 9.4 引入 incubating R8Plugin；9.0+ 默认 optimized resource shrinking |
| Baseline Profile | Performance | https://developer.android.com/topic/performance/baselineprofiles/overview | AndroidX | AGP 9.1+ 能力；profileinstaller 1.4.1 | P1 | 2026-09-10 | 2026-09-10 | 文档 2026-09-01 更新；推荐 Macrobenchmark 1.4.1+，现可跟 1.5.0 |
| Benchmark (Macro/Micro) | Performance | https://developer.android.com/jetpack/androidx/releases/benchmark | AndroidX | 1.5.0 | P1 | 2026-09-10 | 2026-09-10 | 2026-09-09 稳定 1.5.0；默认 requireAot=true |
| NDK | Native | https://developer.android.com/ndk/downloads | https://github.com/android/ndk | r30 LTS `30.0.16248370` | P0 | 2026-09-10 | 2026-09-10 | 2026-09-08 发布 LTS；AGP 9.4 默认仍为 NDK 28.2 |
| 16 KB Page Size | Compatibility / Play | https://developer.android.com/guide/practices/page-sizes | AOSP / Play | Play 强制：2027-02-01 | P0 | 2026-09-10 | 2026-09-10 | target API 35+ 的 64-bit 更新必须 16KB 对齐，否则 2027-02-01 起无法上架更新 |
| Google Play Target SDK | Play Policy | https://developer.android.com/google/play/requirements/target-sdk | Play Console Help | Target API 36（延期至 2026-11-01） | P0 | 2026-09-10 | 2026-09-10 | 文档 2026-09-01 更新；2026-08-31 主截止已过 |
| App Bundle | Distribution | https://developer.android.com/guide/app-bundle | Play | AAB 为 Play 上架格式 | P2 | 2026-09-10 | 2026-09-10 | 本周无新政策；Studio Rabbit 增加 Play 测试轨上传 |
| App Startup | Performance | https://developer.android.com/jetpack/androidx/releases/startup | AndroidX | 1.2.0 | P2 | 2026-09-10 | 2026-09-10 | 自 2024-09-18 无新稳定版 |
| AndroidX Navigation | Jetpack | https://developer.android.com/latest-updates | AndroidX | 2.10.0 | P2 | 2026-09-10 | 2026-09-10 | 2026-08-26 稳定 2.10.0 |
| Room3 | Jetpack | https://developer.android.com/latest-updates | AndroidX | 3.0.2 | P2 | 2026-09-10 | 2026-09-10 | 2026-08-26 稳定 3.0.2 |
| Lifecycle | Jetpack | https://developer.android.com/latest-updates | AndroidX | 2.12.0 | P2 | 2026-09-10 | 2026-09-10 | 2026-08-26 |
| CameraX | Jetpack | https://developer.android.com/latest-updates | AndroidX | 1.6.2 | P2 | 2026-09-10 | 2026-09-10 | 2026-08-26 |

## First Discovery Notes

- 本仓库此前无 Watchlist / Snapshot。2026-09-10 为官方生态监控首次基线。
- 加入 Android 17：已进入 Beta 4.1，且行为变化页在本周仍在更新，工程上必须开始兼容测试。
- 加入 Navigation3：官方已提供稳定线 1.1.7，并进入 1.2.0-rc01，属于 Compose 导航迁移窗口。
- 加入 R8Plugin：AGP 9.4 起 R8 以独立 incubating 插件形态出现，是构建系统拆分信号。
