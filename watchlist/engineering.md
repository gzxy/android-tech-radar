# Engineering Productivity Watchlist

Last updated: 2026-09-11

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| AGP 9.4.0 + `newDsl.optOut` | Watchlist | Adopt | 2026-09 稳定；notes 2026-09-03。当前 9.x 最新线。模块级 opt-out 是大型仓迁 AGP 10 的阀门。Gradle 最低 9.6.0。 | Yes。上一周期写的「升 9.3」应改为升 9.4 |
| AGP 10.0 lock-in | Watchlist | Assess now | Late 2026。删除 legacy Variant API 与 opt-out。Roadmap 仍是 2026-07-22。 | Yes。自定义插件仍用 `applicationVariants` 会发布阻断 |
| DFM 1:1 flavor parity | Evaluate | Assess | AGP 9.4 默认 warning；`android.enforceDynamicFeatureVariantMatching=true` 可升 error；10.0 默认失败。 | 仅有 Dynamic Feature 的仓 |
| AgpTestSuite / R8Plugin | Discover | Assess | AGP 9.4 incubating。测试套件一等 DSL；R8 以独立插件形态出现。文档不足以 Trial。 | 观望即可 |
| Gradle Isolated Projects (9.7.1) | Evaluate | Trial (local/IDE only) | 9.7.1 补丁（官方建议避开 9.7.0）。仍 incubating，**不要打生产包**。成熟度未变。 | Yes。CC 之后最大的配置阶段杠杆 |
| Configuration Cache as preferred mode | Watchlist | Adopt | Isolated Projects 前置。 | Yes。40+ 模块仓非谈判 |

## Hold / not new this cycle

- Version Catalogs / Convention Plugins: 基建，不是发现。
- Declarative Gradle：仍 experimental，EAP3 之后无 2026 稳定信号，不进雷达。
- KSP vs KAPT: 已知。Metro 才是编译税的有趣替代。
- Monorepo 工具超出 Isolated Projects：本窗口无新官方路径。
