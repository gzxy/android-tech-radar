# Architecture Watchlist

Last updated: 2026-09-14

Status legend: Discover → Evaluate → Watchlist → Snapshot

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Remote Compose (AndroidX SDUI) | Watchlist | Assess | 仍为 `1.0.0-alpha19`（2026-09-09）。无 RC/稳定线。不重写。 | 核心流程 Hold。活动页 / 卡片 / 远程表面值得小范围 Trial |
| Metro 1.4 compile-time DI | Watchlist | Trial | **1.4.3（2026-09-08）**。IR class generation 下补了 Hilt interop；推荐仍单 feature Trial。 | Yes，若 Dagger/Anvil/KSP 编译税仍高 |
| Jetpack Navigation 3 | Watchlist | Adopt (new screens) | 仍为 1.1.7 stable / **1.2.0-rc01（2026-09-09）**。无 1.2 stable。 | Yes for Compose-first；可与 Nav2 并存 |
| KMP default module split | Watchlist | Assess | 无新官方结构变更。 | Yes if sharing logic/UI |
| Circuit + MetroX codegen | Evaluate | Assess | 无平台压力，不升级推荐。 | Greenfield Compose/KMP；MVVM 锁定则 Hold |
| Vertical slice / public-impl | Watchlist | Adopt | 100+ 模块仓仍靠它压增量编译。 | Yes |

## Hold / not new this cycle

- Classic MVVM + Hilt + Navigation 2: 成熟，无阶跃变化。
- 自研 JSON 组件目录式 SDUI：被 Remote Compose 官方路径覆盖，不再单独跟踪。
- Plugin architecture / Dynamic Feature：无新平台解锁。
- 本周期 Architecture 无新条目进雷达。Play 质量门槛落在 Engineering / Performance。
