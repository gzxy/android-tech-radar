# Weekly Radar Watchlist

Last updated: 2026-09-10  
Type: first merged baseline  
Sources: android-official / engineering / open-source / ai-android

本表只保留进入周雷达决策面的条目。领域完整清单仍在各源 Watchlist，本文件负责去重与推荐收敛。

| ID | Technology | Category | Source | Version / Signal | Rec | First Seen | Last Checked |
|---|---|---|---|---|---|---|---|
| play-target-36 | Play Target API 36 | Official / Policy | android-official | Enforced 2026-08-31; ext 2026-11-01 | Adopt | 2026-09-10 | 2026-09-10 |
| page-16kb | 16KB Page Size | Official / Native | android-official | Play hard stop 2027-02-01 | Adopt | 2026-09-10 | 2026-09-10 |
| studio-quail4 | Android Studio Quail 4 | Official / Tooling | android-official | 2026.1.4 stable | Adopt | 2026-09-10 | 2026-09-10 |
| config-cache | Configuration Cache | Engineering | engineering | Gradle 9 preferred mode | Adopt | 2026-09-10 | 2026-09-10 |
| baseline-startup | Baseline + Startup Profile CI | Performance | engineering + official | Require mode | Adopt | 2026-09-10 | 2026-09-10 |
| android-skills | Android CLI + official skills | AI / Tooling | ai-android + oss | skills v1.0.11 | Adopt | 2026-09-10 | 2026-09-10 |
| aqi-agent | Studio AQI Crash/Leak Agent | AI | ai-android | Quail 2+ capability in Quail 4 | Adopt | 2026-09-10 | 2026-09-10 |
| ndk-r30 | NDK r30 LTS | Official / Native | android-official | 30.0.16248370 | Adopt | 2026-09-10 | 2026-09-10 |
| agp-94 | AGP 9.4.0 / AGP 10 prep | Official / Build | android-official + engineering | 9.4.0; 10 deletes legacy API | Trial | 2026-09-10 | 2026-09-10 |
| isolated-projects | Gradle Isolated Projects | Engineering | engineering + oss | 9.7 incubating | Trial | 2026-09-10 | 2026-09-10 |
| kotlin-2420 | Kotlin 2.4.20 | Official / Language | android-official | 2026-09-07 | Trial | 2026-09-10 | 2026-09-10 |
| compose-1121 | Jetpack Compose 1.12.1 | Official / UI | android-official | 2026-09-09 | Trial | 2026-09-10 | 2026-09-10 |
| benchmark-150 | Benchmark 1.5.0 | Official / Perf | android-official | requireAot=true | Trial | 2026-09-10 | 2026-09-10 |
| r8-analyzer | AGP R8 analyzer + keepRules | Engineering / Perf | engineering | AGP 9.3+ notes 2026-09-03 | Trial | 2026-09-10 | 2026-09-10 |
| metro-1 | Metro 1.0 | Architecture | engineering | compiler-plugin DI | Trial | 2026-09-10 | 2026-09-10 |
| adk-kotlin | ADK for Kotlin | AI / OSS | open-source | 1.0.1 | Trial | 2026-09-10 | 2026-09-10 |
| maestro-mcp | Maestro MCP | AI / Testing | ai-android | YAML stays in CI | Trial | 2026-09-10 | 2026-09-10 |
| kuikly | KuiklyUI | Domestic OSS | open-source | 2.27.0 + KuiklyUI-AI | Trial | 2026-09-10 | 2026-09-10 |
| android-17 | Android 17 | Official / Platform | android-official | Beta 4.1 | Assess | 2026-09-10 | 2026-09-10 |
| nav3-12 | Navigation3 1.2 RC | Official / Jetpack | android-official | 1.2.0-rc01 / stable 1.1.7 | Assess | 2026-09-10 | 2026-09-10 |
| ksp-2312 | KSP 2.3.12 | Official / Build | android-official | backing fields opt-in | Assess | 2026-09-10 | 2026-09-10 |
| agp10-plugins | AGP 10 plugin inventory | Engineering | engineering | lock-in late 2026 | Assess | 2026-09-10 | 2026-09-10 |
| kmp-split | KMP default module split | Architecture | engineering + oss | AGP 9 hard constraint | Assess | 2026-09-10 | 2026-09-10 |
| circuit-038 | Circuit 0.38 | Architecture | open-source | Screen no longer Parcelable | Assess | 2026-09-10 | 2026-09-10 |
| crashlytics-mcp | Crashlytics MCP | AI | ai-android | Experimental | Assess | 2026-09-10 | 2026-09-10 |
| github-aw | GitHub Agentic Workflows | AI / CI | ai-android | compile/dep self-heal | Assess | 2026-09-10 | 2026-09-10 |
| paparazzi-2 | Paparazzi 2.0-alpha05 | OSS / Testing | open-source | AGP 9 + KMP library | Assess | 2026-09-10 | 2026-09-10 |
| mnn | Alibaba MNN | Domestic OSS / AI | open-source | 3.6.1 on-device LLM | Assess | 2026-09-10 | 2026-09-10 |
| lynx-41 | Lynx 4.1.0 | Domestic OSS | open-source | monthly + Autolink | Trial* | 2026-09-10 | 2026-09-10 |
| isolated-prod | Isolated Projects production | Engineering | engineering | official: do not use | Hold | 2026-09-10 | 2026-09-10 |
| circuit-replace-mvvm | Circuit full MVVM replace | Architecture | engineering | no platform pressure | Hold | 2026-09-10 | 2026-09-10 |
| cloud-instrumented | Cloud Agent Instrumented/ANR | AI | ai-android | emulator not delivered | Hold | 2026-09-10 | 2026-09-10 |
| jenkins-ai | Jenkins + AI | AI / CI | ai-android | no Android protocol | Hold | 2026-09-10 | 2026-09-10 |
| hotfix-stack | Tinker/Shadow/Atlas/AndFix/Robust | Domestic OSS | open-source | inactive generation | Hold | 2026-09-10 | 2026-09-10 |
| legacy-tools | Flipper/AMD/ByteX | OSS | open-source | archived | Hold | 2026-09-10 | 2026-09-10 |
| dual-runtime | ADK + MNN dual runtime | AI | weekly merge | pick one stack | Hold | 2026-09-10 | 2026-09-10 |

\* Lynx：仅已有前端/动态化预算的团队 Trial；纯 Kotlin 团队优先 Compose / Kuikly。

## Ring counts

- Adopt: 8
- Trial: 10（含 Lynx 条件 Trial，雷达主表 Trial 以 Kuikly 代表跨端）
- Assess: 10
- Hold: 7

## Next-run rule

下一轮只对比本表的 Version / Signal / Rec。三者都不变则不要重写周报对应章节。
