# Engineering Productivity Watchlist

Last updated: 2026-09-14

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Play DEX 25% + R8 Configuration Analyzer | Watchlist | **Adopt** | Play 2026-08-26 公告；HC 给出 25% shrink / optimize / obfuscate。Analyzer 文档 **2026-09-08** 更新。Tinder：分数 28%→50%，慢冷启动 -47%。上一周期把 analyzer 写成 Trial，过时。 | Yes。DEX > 10 MB 的商业 App 是发布闸门 |
| AGP 9.4.0 + `newDsl.optOut` | Watchlist | Adopt | 仍为当前 9.x 稳定线。无 9.4.x / 9.5 / 10.0。 | Yes |
| AGP 10.0 lock-in | Watchlist | Assess now | Late 2026。Roadmap 仍是 2026-07-22。 | Yes。自定义插件仍用 `applicationVariants` 会发布阻断 |
| DFM 1:1 flavor parity | Evaluate | Assess | AGP 9.4 默认 warning；10.0 默认失败。无新能力。 | 仅有 Dynamic Feature 的仓 |
| AgpTestSuite / R8Plugin | Discover | Assess | 仍 incubating。Analyzer 已 Adopt，不要和 R8Plugin 现网切混为一谈。 | 观望即可 |
| Gradle Isolated Projects | Evaluate | Trial (local/IDE only) | 稳定线仍 **9.7.1**。**9.8.0-RC1（约 2026-09-13）** 出现，未改 incubating。KSP 2.3.11 已支持 `org.gradle.isolated-projects`。 | Yes。不要打生产包 |
| Configuration Cache as preferred mode | Watchlist | Adopt | Isolated Projects 前置。 | Yes。40+ 模块仓非谈判 |

## Hold / not new this cycle

- Version Catalogs / Convention Plugins: 基建，不是发现。
- Declarative Gradle：仍 experimental，不进雷达。
- KSP vs KAPT: 已知。KSP 2.3.11 Isolated Projects 兼容记在 Isolated Projects 附件。
- Metro 全量替换 Hilt：1.4.3 是补丁，不是 2.0。
