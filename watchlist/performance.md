# Performance Watchlist

Last updated: 2026-09-11

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Android 17 Memory Limiter | Watchlist | Adopt (telemetry) | 官方博文 2026-08-19；行为页 2026-09-02。Pixel 已开；OEM 将在未来一年铺到 4–16GB 机型。超出先 zRAM 卡顿，再无堆栈杀掉。 | Yes。图多 / 长会话 / 多媒体尤其 |
| AGP 9.4 R8Plugin + 9.3 analyzer | Evaluate | Trial | 9.3 的 `:app:analyzeReleaseR8Config` 仍是 keep 反馈环；9.4 把 R8 拆成 incubating 插件。Analyzer 可试，R8Plugin 只 Assess。 | Yes |
| Startup Profile + Baseline Profile CI | Watchlist | Adopt | 无新平台 API。差距仍在 CI 重生 + `BaselineProfileMode.Require`。 | Yes |
| 16 KB page size | Snapshot | Adopt (compliance) | **截止日期更正：2027-02-01**（上一周期写成 May 2026 已过）。target 35+ 的 64-bit 更新必须对齐。 | 有 `.so` 就必须做 |
| Compose compiler reports in CI | Watchlist | Trial | 仍是官方 skippability 信号。只在有 jank 的 release 构建开。 | Compose 重的表面 |
| Macrobenchmark on 16 KB images | Watchlist | Assess | 页大小改变 page fault / ELF 布局；4 KB 设备启动数字会骗人。 | Native 重的应用 |

## Hold / not new this cycle

- Generic LeakCanary / StrictMode 清单：卫生项，不是新技术。
- Cloud Profiles 单独使用：收敛仍慢于自带 Baseline + Startup Profile。
- Benchmark `requireAot` 默认 true：1.5 线仍在 alpha（公开页 1.5.0-alpha07）。等稳定再改 CI 默认，不单列发现。
