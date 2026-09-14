# Weekly Radar Watchlist

Last updated: 2026-09-14  
Type: incremental vs 2026-09-11  
Sources: android-official / engineering / open-source / ai-android  
本周新日报：`engineering` 09-11+09-14、`open-source` 09-14、`ai-android` 09-11+09-14。official 无增量。

本表只保留进入周雷达决策面的条目。领域完整清单仍在各源 Watchlist，本文件负责去重与推荐收敛。

| ID | Technology | Category | Source | Version / Signal | Rec | First Seen | Last Checked |
|---|---|---|---|---|---|---|---|
| play-target-36 | Play Target API 36 | Official / Policy | android-official | Enforced 2026-08-31; ext 2026-11-01 | Adopt | 2026-09-10 | 2026-09-10 |
| page-16kb | 16KB Page Size | Official / Native | android-official + engineering | Phone/tablet 2027-02-01; Wear 2026-09-15 | Adopt | 2026-09-10 | 2026-09-14 |
| studio-quail4 | Android Studio Quail 4 | Official / Tooling | android-official | 2026.1.4 stable; 23 skills preloaded | Adopt | 2026-09-10 | 2026-09-11 |
| config-cache | Configuration Cache | Engineering | engineering | Gradle 9 preferred mode | Adopt | 2026-09-10 | 2026-09-14 |
| baseline-startup | Baseline + Startup Profile CI | Performance | engineering + official | Require mode | Adopt | 2026-09-10 | 2026-09-14 |
| android-skills | Android CLI + official skills | AI / Tooling | ai-android + oss | skills v1.0.11; 24 SKILL.md; Quail 4 preloaded | Adopt | 2026-09-10 | 2026-09-14 |
| aqi-agent | Studio AQI Crash/Leak Agent | AI | ai-android | Quail 4 production host | Adopt | 2026-09-10 | 2026-09-14 |
| ndk-r30 | NDK r30 LTS | Official / Native | android-official | 30.0.16248370 | Adopt | 2026-09-10 | 2026-09-10 |
| dagger-ksp | Dagger / Hilt KSP | Official / Build | open-source | Docs: stable since Dagger 2.60+ / KSP 2.3.9+ | Adopt | 2026-09-11 | 2026-09-14 |
| compose-lints | compose-lints 1.6.0 | Engineering | open-source | Slack production Compose lint | Adopt | 2026-09-11 | 2026-09-14 |
| r8-analyzer | R8 Analyzer + Play DEX 25% | Official / Build | engineering | Docs 2026-09-08; Play 3× ≥25%; Tinder 28%→50% | Adopt | 2026-09-10 | 2026-09-14 |
| play-memory-p90 | Play Memory / Bitmap P90 | Official / Perf | engineering | Core vital; RAM-tier P90; enforce 2027-02 | Adopt | 2026-09-14 | 2026-09-14 |
| benchmark-150 | Benchmark 1.5.0 | Official / Perf | engineering + official | Stable 2026-09-09; requireAot=true | Adopt | 2026-09-10 | 2026-09-14 |
| agp-94 | AGP 9.4.0 / New DSL | Official / Build | android-official + engineering | 9.4.0 current 9.x; newDsl.optOut; DFM 1:1 | Adopt | 2026-09-10 | 2026-09-14 |
| isolated-projects | Gradle Isolated Projects | Engineering | engineering + oss | 9.7.1 incubating; 9.8.0-RC1 bypass | Trial | 2026-09-10 | 2026-09-14 |
| kotlin-2420 | Kotlin 2.4.20 | Official / Language | android-official | 2026-09-07; Foundry main aligned | Trial | 2026-09-10 | 2026-09-14 |
| compose-1121 | Jetpack Compose 1.12.1 | Official / UI | android-official | 2026-09-09 | Trial | 2026-09-10 | 2026-09-10 |
| metro-1 | Metro 1.4.3 | Architecture | engineering | 1.4.3 Hilt interop on IR class gen | Trial | 2026-09-10 | 2026-09-14 |
| adk-kotlin | ADK for Kotlin | AI / OSS | open-source | 1.0.1; main: AppFunctionsToolset + MCP reject | Trial | 2026-09-10 | 2026-09-14 |
| maestro-mcp | Maestro MCP | AI / Testing | ai-android | YAML + Cloud describe + crash/ANR artifact | Trial | 2026-09-10 | 2026-09-14 |
| kuikly | KuiklyUI | Domestic OSS | open-source | 2.27.0 + KuiklyUI-AI | Trial | 2026-09-10 | 2026-09-14 |
| appfunctions | AppFunctions (on-device MCP) | Official / AI | open-source | Jetpack 1.0.0-alpha11; samples + Toolset | Trial | 2026-09-11 | 2026-09-14 |
| apa-perfetto | android-profiler / Perfetto | AI / Perf | ai-android | SQL diagnosis closed; auto-fix+retest open | Trial | 2026-09-14 | 2026-09-14 |
| android-17 | Android 17 | Official / Platform | android-official | Beta 4.1 | Assess | 2026-09-10 | 2026-09-10 |
| nav3-12 | Navigation3 1.2 RC | Official / Jetpack | android-official | 1.2.0-rc01 / stable 1.1.7 | Assess | 2026-09-10 | 2026-09-14 |
| ksp-2312 | KSP 2.3.12 | Official / Build | android-official | backing fields opt-in | Assess | 2026-09-10 | 2026-09-14 |
| agp10-plugins | AGP 10 plugin inventory | Engineering | engineering | lock-in late 2026 | Assess | 2026-09-10 | 2026-09-14 |
| kmp-split | KMP default module split | Architecture | engineering + oss | AGP 9 hard constraint | Assess | 2026-09-10 | 2026-09-14 |
| circuit-038 | Circuit 0.38 | Architecture | open-source | Screen no longer Parcelable | Assess | 2026-09-10 | 2026-09-14 |
| crashlytics-mcp | Crashlytics MCP | AI | ai-android | Experimental; docs 2026-09-11 | Assess | 2026-09-10 | 2026-09-14 |
| github-aw | GitHub Agentic Workflows | AI / CI | ai-android | compile/dep self-heal | Assess | 2026-09-10 | 2026-09-14 |
| paparazzi-2 | Paparazzi 2.0-alpha05 | OSS / Testing | open-source | parallel cleanRecord race; prune hidden a11y | Assess | 2026-09-10 | 2026-09-14 |
| mnn | Alibaba MNN | Domestic OSS / AI | open-source | 3.6.1; RVV KV-cache / OpenCL FlashAttention | Assess | 2026-09-10 | 2026-09-14 |
| remote-compose | Remote Compose | Architecture | engineering | 1.0.0-alpha19; official SDUI | Assess | 2026-09-14 | 2026-09-14 |
| rabbit-1 | Studio Rabbit 1 | AI / Migration | ai-android | Canary iOS/Flutter/RN → Compose | Assess | 2026-09-14 | 2026-09-14 |
| lynx-41 | Lynx 4.1.0 | Domestic OSS | open-source | pin 4.1.0; 4.0.3 empty maint tag; do not follow develop | Trial* | 2026-09-10 | 2026-09-14 |
| isolated-prod | Isolated Projects / 9.8 RC production | Engineering | engineering | official: do not use | Hold | 2026-09-10 | 2026-09-14 |
| circuit-replace-mvvm | Circuit full MVVM replace | Architecture | engineering | no platform pressure | Hold | 2026-09-10 | 2026-09-14 |
| cloud-instrumented | Cloud Agent Instrumented/ANR | AI | ai-android | emulator not delivered | Hold | 2026-09-10 | 2026-09-14 |
| jenkins-ai | Jenkins + AI | AI / CI | ai-android | no Android protocol | Hold | 2026-09-10 | 2026-09-14 |
| hotfix-stack | Tinker/Shadow/Atlas/AndFix/Robust | Domestic OSS | open-source | inactive generation | Hold | 2026-09-10 | 2026-09-14 |
| legacy-tools | Flipper/AMD/ByteX | OSS | open-source | archived | Hold | 2026-09-10 | 2026-09-14 |
| dual-runtime | ADK + MNN dual runtime | AI | weekly merge | pick one stack | Hold | 2026-09-10 | 2026-09-14 |
| appfn-adk-merged | AppFunctions + Gemini one prod milestone | AI | weekly merge | share contract; do not bind EAP | Hold | 2026-09-11 | 2026-09-14 |
| remote-compose-core | Remote Compose in core flows | Architecture | engineering | still alpha | Hold | 2026-09-14 | 2026-09-14 |
| kotlin-toolchain-replace | Kotlin Toolchain replaces Gradle | AI / Build | open-source | Agent skill only; no large-app landing | Hold | 2026-09-14 | 2026-09-14 |

\* Lynx：仅已有前端/动态化预算的团队 Trial；纯 Kotlin 团队优先 Compose / Kuikly。钉 4.1.0，等 4.2。

## Ring counts

- Adopt: 14
- Trial: 9（主表含 AppFunctions + Perfetto；Lynx 为条件 Trial，雷达主表跨端仍以 Kuikly 代表）
- Assess: 12
- Hold: 10

## Next-run rule

下一轮只对比本表的 Version / Signal / Rec。三者都不变则不要重写周报对应章节。下一快照：`snapshots/weekly/2026-09-14.md`。
