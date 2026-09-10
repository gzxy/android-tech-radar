# Engineering Productivity Watchlist

Last updated: 2026-09-10

| Tech | Status | Rec | Why now | Large commercial app? |
| --- | --- | --- | --- | --- |
| Gradle Isolated Projects (9.7) | Evaluate | Trial (local/IDE only) | 2026-08-06 incubating. Parallel configuration. Now in Android + AndroidX already compatible. | Yes. Biggest remaining config-phase lever after Configuration Cache |
| AGP 10.0 lock-in | Watchlist | Assess now | Late 2026. Deletes legacy Variant API and opt-out flags. Roadmap updated 2026-07-22. | Yes. Blocking risk if custom plugins still use `applicationVariants` |
| AGP 9.3 + built-in Kotlin | Watchlist | Adopt | AGP 9.3 (July 2026) + KGP bundled. `kotlin-android` plugin is incompatible with new DSL. | Yes. Prerequisite for Isolated Projects and AGP 10 |
| AGP 9.3 R8 optimization DSL | Watchlist | Trial | `optimization {}`, `src/*/keepRules/*.keep`, `:app:analyzeReleaseR8Config` without full package. Notes updated 2026-09-03. | Yes. Shortens keep-rule iteration |
| Configuration Cache as preferred mode | Watchlist | Adopt | Gradle 9 made CC preferred; Isolated Projects requires it. | Yes. Non-negotiable for 40+ module apps |

## Hold / not new this cycle

- Version Catalogs / Convention Plugins: table stakes, not a discovery.
- KSP vs KAPT: known. Metro is the interesting alternative, tracked under architecture.
- Monorepo tooling beyond Isolated Projects: no new official Android path this window.
