# Architecture Watchlist

Last updated: 2026-09-11

Status legend: Discover → Evaluate → Watchlist → Snapshot

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Remote Compose (AndroidX SDUI) | Discover → Watchlist | Assess | Official `androidx.compose.remote` 1.0.0-alpha19 (2026-09-09). 90 天内从 alpha12 推到 alpha19，公开 API 在加速。上一周期误判为「无高信号」。 | 核心流程 Hold。活动页 / 卡片 / 远程表面值得小范围 Trial |
| Metro 1.4 compile-time DI | Watchlist | Trial | 1.4.2（2026-08-13）。相对 1.0：实验性 suspend providers、Circuit `@SubCircuitInject`。推荐不变。 | Yes，若 Dagger/Anvil/KSP 编译税仍高 |
| Jetpack Navigation 3 | Watchlist | Adopt (new screens) | 稳定线 1.1.7；**1.2.0-rc01 于 2026-09-09 发布**。Deep link serializer / BackStackMatcher。 | Yes for Compose-first；可与 Nav2 并存 |
| KMP default module split | Watchlist | Assess | 无新官方结构变更。AGP 9.4 增加 `KotlinHierarchyBuilder.withAndroid()`。 | Yes if sharing logic/UI |
| Circuit + MetroX codegen | Evaluate | Assess | Metro 1.4 增加 sub-circuit。无平台压力，不升级推荐。 | Greenfield Compose/KMP；MVVM 锁定则 Hold |
| Vertical slice / public-impl | Watchlist | Adopt | 100+ 模块仓仍靠它压增量编译。 | Yes |

## Hold / not new this cycle

- Classic MVVM + Hilt + Navigation 2: 成熟，无阶跃变化。
- 自研 JSON 组件目录式 SDUI：被 Remote Compose 官方路径覆盖，不再单独跟踪。
- Plugin architecture / Dynamic Feature：无新平台解锁。DFM 只在 AGP 9.4 出现 1:1 flavor 校验（记在 engineering）。
