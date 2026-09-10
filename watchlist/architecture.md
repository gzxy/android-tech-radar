# Architecture Watchlist

Last updated: 2026-09-10

Status legend: Discover → Evaluate → Watchlist → Snapshot

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Metro 1.0 compile-time DI | Watchlist | Trial | 2026-04-27 stable. Compiler plugin, no KSP/KAPT. Slack-origin, multiplatform-first. | Yes, if Dagger/Anvil/KSP cost dominates compile time |
| Jetpack Navigation 3 | Watchlist | Adopt (new screens) | Stable 2025-11-19. Compose-owned back stack. JetBrains KotlinConf app already on it. | Yes for Compose-first apps; migrate incrementally |
| KMP default module split | Watchlist | Assess | JetBrains May 2026. AGP 9.0 forbids Android application plugin in a KMP module. | Yes if sharing logic/UI; mandatory if already on KMP+AGP 9 |
| Circuit + MetroX codegen | Evaluate | Assess | Metro ships opt-in Circuit codegen. Compose-runtime presenters, not ViewModel-centric. | Yes for greenfield Compose/KMP; Hold if MVVM is locked |
| Vertical slice / public-impl | Watchlist | Adopt | Still the only modularization shape that keeps incremental compile cheap at 100+ modules. | Yes |

## Hold / not new this cycle

- Classic MVVM + Hilt + Navigation 2: mature, no step-function change.
- Server Driven UI: no high-signal 90-day shift worth promoting.
- Plugin architecture / Dynamic Feature: no new platform unlock.
