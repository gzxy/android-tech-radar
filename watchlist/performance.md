# Performance Watchlist

Last updated: 2026-09-10

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Startup Profile + Baseline Profile CI | Watchlist | Adopt | R8 rewriting + Startup Profiles still the cheapest first-launch win (~15% extra on DEX layout). Stale profiles are the real regression. | Yes. Gate with `BaselineProfileMode.Require` |
| R8 Configuration Analyzer task | Evaluate | Trial | AGP 9.3 standalone `:app:analyzeReleaseR8Config` (notes 2026-09-03). Keep-rule loop without packaging. | Yes |
| 16 KB page size | Snapshot | Adopt (compliance) | Play blocked non-compliant targetSdk 35+ updates. May 2026 deadline already passed. | Yes if any `.so` ships |
| Compose compiler reports in CI | Watchlist | Trial | Still the only official skippability signal. Only enable on release builds when jank exists. | Yes for Compose-heavy surfaces |
| Macrobenchmark on 16 KB images | Watchlist | Assess | Page-size change shifts page faults and ELF layout; startup numbers from 4 KB devices can lie. | Yes for native-heavy apps |

## Hold / not new this cycle

- Generic LeakCanary / StrictMode checklists: hygiene, not a new technique.
- Cloud Profiles alone: still slower to converge than shipping Baseline + Startup Profiles.
