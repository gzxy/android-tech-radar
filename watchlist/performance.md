# Performance Watchlist

Last updated: 2026-09-14

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Play Memory Core Vitals（P90 门槛） | Watchlist | **Adopt（看板 + 分档回归）** | 2026-08-26 Play 质量要求。Memory 成为 core vital。2027-02 起按 RAM 档 + 进程态卡 P90。上一周期只写了 Memory Limiter 遥测，没写数字门槛。 | Yes。图多 / 长会话 / 多媒体尤其 |
| Android 17 Memory Limiter | Watchlist | Adopt (telemetry) | 限额仍不可查询。Play 看板是本周期新杠杆，Limiter 本身无 API 变化。 | Yes |
| R8 Analyzer + Play DEX 25% | Watchlist | **Adopt** | 从「full R8 执行项」变成 Play 上传门槛。Tinder 官方数字：慢冷启动 -47%、包体 -29%、ANR 0.35%→0.28%。 | Yes |
| Benchmark 1.5.0 | Watchlist | **Adopt（CI）** | **2026-09-09 稳定。** 上一周期误写成仍 alpha。`requireAot` / `requireMainThread` 默认 true。 | Yes。有 Microbenchmark 的仓立刻升 |
| Startup Profile + Baseline Profile CI | Watchlist | Adopt | 无新平台 API。差距仍在 CI 重生 + `BaselineProfileMode.Require`。 | Yes |
| 16 KB page size | Snapshot | Adopt (compliance) | 手机/平板截止仍 **2027-02-01**。**Wear 截止 2026-09-15**（本周）。 | 有 `.so` 就必须做；有 Wear 本周必须过 |
| Compose compiler reports in CI | Watchlist | Trial | 仍是官方 skippability 信号。只在有 jank 的 release 构建开。 | Compose 重的表面 |
| Macrobenchmark on 16 KB images | Watchlist | Assess | 页大小改变 page fault / ELF 布局；4 KB 设备启动数字会骗人。 | Native 重的应用 |

## Hold / not new this cycle

- Generic LeakCanary / StrictMode 清单：卫生项，不是新技术。
- Cloud Profiles 单独使用：收敛仍慢于自带 Baseline + Startup Profile。
- Memory Limiter 全盘改造：等 P90 看板证明击中再开专项（推荐未变）。
