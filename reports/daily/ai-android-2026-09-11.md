# AI + Android Daily Report

日期：2026-09-11  
对照：2026-09-10 基线快照。不写 AI 新闻。只回答相对昨日：**有没有新的能力能进 Android 团队流程，以及能不能省工程师时间。**

## Executive Summary

昨夜到今早，**没有新产品把生产 ANR、Cloud 模拟器或 Jenkins 接成闭环。** 相对昨日快照，真正值得改流程的是三件事：

1. **Adopt 宿主换成 Quail 4。** 官方 skills 已预装，Crash/Leak/机械迁移不必再先装 CLI skill。
2. **Performance 分诊可以 Trial。** `android-profiler` 能对 Perfetto trace 跑真实 SQL，不再只是「提示模型去看 Profiler」。自动改代码+复测仍 Hold。
3. **有 iOS / Flutter / RN 源工程的团队**，可 Assess Rabbit 1 迁移助手（规划→转码→编译）。没有源工程的团队忽略。

**AI 是否真正节省 Android 工程师时间？**

- Crash / Leak / 官方 skill 覆盖的迁移：是（结论与昨日相同，入口改为 Quail 4）。
- 读一张启动/卡顿 Perfetto：是。省的是「打开 UI 盲翻 track」，不是「修好再对比指标」。
- 跨平台机械移植：Canary 下部分是；编译过 ≠ 能上架。
- 未接 trace / Crashlytics / Gradle / 设备的通用 Agent：否。

## New AI Capabilities

只列相对 `snapshots/ai-agent/2026-09-10.md` 的增量。详见 `diffs/ai-agent/2026-09-11.md`。

| 能力 | 输入 | Agent 动作 | 验证 | 相对昨日 |
|---|---|---|---|---|
| Quail 4 预装 23 skills | 迁移/配置类自然语言 | 按元数据自动调官方 skill 改工程 | Gradle / 视觉验收（与昨日 skill 相同） | 宿主换代，少配置 |
| android-profiler → Perfetto SQL | `.perfetto-trace` / APA 录制 | 路由工作流、写 SQL、跑 `trace_processor` | 查询可复现；**无自动复测** | 昨日低估为「只接地」 |
| Rabbit 1 跨平台迁移 | iOS / Flutter / RN 工程 | 规划、转 Kotlin/Compose | 编译检查 | 新条目，Canary |
| Maestro Cloud 失败调试 | Cloud `run_id` | 拉录像/log/hierarchy，解释并改 YAML | 再跑 Cloud/本地 flow | 昨日漏记（7 月已有） |
| Maestro 跑测 Crash/ANR 产物 | 该次 flow 的 tombstone / ANR | 读 `crash-report.txt` / `anr-report.txt` | 仅覆盖该次跑测 | 昨日漏记 |

## Android Use Cases

### Crash — 流程不变，入口对齐 Quail 4

继续 Adopt AQI Fix with AI 与 Crashlytics MCP。MCP 文档 2026-09-10 仍 Experimental。  
**Studio Agent 接不了 Crashlytics MCP**（无 stdio）。Studio 走 AQI；Cursor / Claude Code / Codex 走 MCP。不要要求全员在 Studio 里装 Firebase MCP。

### ANR — 仍未闭环；多了一条「测试会话」旁路

生产 ANR：AQI 能列，无「Fix with AI + 复现」按钮。Hold 自动修。

新增旁路：Maestro 跑测若触发 ANR，artifact 里有 `anr-report.txt`，Agent 可据此改 flow 或可疑主线程代码。这不是 On-call ANR 流程。

### Performance — 从 Hold 分析，上调到 Trial 分诊

昨日判断仍然对后半段：没有产品做「改代码 → 再采同一指标」。

前半段应上调。官方路径已经是：

```text
问题（启动 / jank / 内存）
 ↓
APA 或 Studio System Trace 录制
 ↓
android-profiler skill
 ↓
Perfetto SQL + trace_processor
 ↓
根因报告
 ↓
人（或 Agent 起草）改代码
 ↓
人再录一张 trace 对比
```

**省的是读 trace 的前 30–90 分钟。** 不省调参和回归。PoC 只验收「同一张 trace 上 Agent 给出可复现 SQL + 说得通的根因」，不要验收自动加速百分之几。

### Testing — Maestro 补上「CI 红了之后」

写 YAML 进 CI 的建议不变，仍与 Journeys 二选一。

增量：Cloud 跑失败后，把 `run_id` 丢给已接 Maestro MCP 的 Agent，让它拉 artifact 修 selector 或断言。这比打开 Cloud 控制台省一次上下文切换。

### Build / Code Review / Release / Documentation

无新闭环。编译失败、Bugbot、changelog、`android docs` 维持昨日结论。

### 跨平台迁移 — 仅部分团队

Rabbit 1：源工程 → 规划 → Compose 代码 → 编译。  
没有 iOS/Flutter/RN 仓库的 Android 团队：**不 Adopt、不排期。**  
有的：用一个中等模块做 Assess，成功标准是 `assembleDebug` 过 + 3 个主屏幕能点，而不是「迁移完成」。

## Agent / MCP

团队工具面相对昨日的修正：

1. **Android Studio Quail 4 Agent** — 生产默认。Crash/Leak + 预装 skills。
2. **Firebase MCP** — 仍只给非 Studio Agent（Cursor / Claude Code）。Studio 不要硬接。
3. **Android CLI + `android skills add --all`** — 给 Cursor / Claude / Codex / Gemini；Studio 已预装则不必重复。
4. **`android-profiler` skill** — 性能分诊必装（若不用 Studio 预装）。
5. **Maestro MCP 或 Journeys** — 仍只选一条 UI 资产；选 Maestro 的团队应升到 CLI 2.7+ 才能用 Cloud 失败调试。

Studio MCP（GitHub / Figma 等 HTTP 服务器）能减少「去网页开 PR / 对设计稿」，**补不了** Crash 与真机 UI。不要把它算进 Android 质量闭环。

Cloud / Scheduled Agent：结论不变。JVM 单测可以；模拟器官方未交付。

## Developer Productivity

| 重复劳动 | 相对昨日 | 人还要做什么 |
|---|---|---|
| Crash 分诊与常见修复 | 不变，入口 Quail 4 | 批准 diff、符号表、回归 |
| 官方 skill 迁移的环境准备 | **变少**（Studio 预装） | 视觉/导航验收 |
| 读 Perfetto / 写第一版 SQL | **能交给 Agent** | 复录对比、定优化 |
| 生产 ANR | 不能自动修 | 人抓 trace |
| Maestro Cloud 失败看盘 | **能交给 Agent** | 确认 selector 策略 |
| iOS/RN/Flutter 机械搬到 Compose | Canary 可试 | 行为验收、平台 API |
| 发版 / Jenkins / Cloud 模拟器 | 不变，不能 | 全部人控 |

## Watchlist Diff

### Added

- `apa-perfetto-agent`（Watch / Trial）
- `as-rabbit1-migrate`（Watch / Assess）

### Updated

- `as-quail2-agent` → `as-studio-agent`：Adopt 宿主改为 Quail 4；补记预装 skills 与 Studio MCP 无 stdio。
- `maestro-mcp`：补记 Cloud 失败调试与跑测 Crash/ANR artifact；CLI 2.10.0。
- `android-cli-skills`：技能数仍 24；`android-profiler` 升为 Perfetto 编排器。
- `crashlytics-mcp`：文档日期 2026-09-10，状态仍 Experimental。

### Removed / Deprecated

无。

### No Significant Change

Journeys、Bugbot、Cloud Agent、Claude Code、Android Bench、GitHub AW、社区 MCP、Jenkins。

## PoC Candidates

昨日 P0 Crash / P1 skill 迁移 / P2 Maestro 主路径仍然有效。今日只加两条，且不要并行铺开。

### P1b — Perfetto 分诊（本周可做）

1. 选 1 个已知的启动或滑动卡顿，录一张 system trace。
2. Cursor 或 Studio Agent + `android-profiler`：「为什么启动慢 / 这一段掉帧」。
3. 成功标准：Agent 跑出可复现的 `trace_processor` SQL，并指出具体线程/slice；工程师认可根因方向。
4. 失败（幻觉 schema、不跑 SQL、只给空泛建议）则退回 Hold，继续人看 APA。

### P3 — 仅当存在源工程：Rabbit 1 迁移一个模块

成功标准：`assembleDebug` 过，主路径 3 屏可点。失败则等 Stable，不要进主线。

### 仍不做

- 生产 ANR 自动修复。
- Cloud Agent 启模拟器。
- Jenkins AI 构建分析。
- 「Agent 自动把启动优化 x%」而无复测协议。

## Recommendation

| 对象 | 级别 | 相对昨日 |
|---|---|---|
| Android Studio **Quail 4** AQI + Leak Agent + 预装 skills | **Adopt** | 宿主从 Quail 2 换到 Quail 4 |
| Android CLI + `android/skills --all`（非 Studio Agent） | **Adopt** | 不变 |
| Firebase Crashlytics MCP（值班机，非 Studio） | **Adopt** | 不变；仍 Experimental |
| android-profiler / Perfetto 分诊 | **Trial** | 新；只试分析 |
| Maestro MCP（含 Cloud 失败调试） | **Trial** | 补强，不升级为 Adopt |
| Journeys 核心 Happy Path | **Trial** | 不变；与 Maestro 二选一 |
| Bugbot + Android `BUGBOT.md` | **Trial** | 不变 |
| Rabbit 1 跨平台迁移 | **Assess** | 新；无源工程则忽略 |
| GitHub Agentic Workflows | **Assess** | 不变 |
| Perfetto 自动修复并复测 / 生产 ANR 自动修 | **Hold** | 后半环仍断 |
| Cursor Cloud 模拟器 / Jenkins + AI | **Hold** | 不变 |

**给 Android 团队的一句执行建议：**  
把默认 IDE 升到 Quail 4，把「读 Perfetto」做成本周一个有 SQL 验收的 Trial。其他维持昨日：先 Crash 和官方 skills，再谈自动发版和 Cloud 模拟器。

## Sources

- https://developer.android.com/ai-in-android
- https://android-developers.googleblog.com/2026/09/leverage-gemma-4-android-studio-quail.html
- https://developer.android.com/studio/preview/features
- https://developer.android.com/studio/gemini/skills
- https://developer.android.com/studio/gemini/add-mcp-server
- https://developer.android.com/tools/agents/android-cli
- https://developer.android.com/tools/agents/android-skills
- https://developer.android.com/android-performance-analyzer/analyze/ai
- https://developer.android.com/blog/posts/introducing-android-performance-analyzer-the-next-evolution-in-profiling-for-android
- https://github.com/android/skills
- https://github.com/android/skills/blob/main/profilers/android-profiler/SKILL.md
- https://firebase.google.com/docs/crashlytics/ai-assistance-mcp
- https://firebase.google.com/docs/ai-assistance/mcp-server
- https://developer.android.com/studio/gemini/journeys
- https://developer.android.com/bench
- https://docs.maestro.dev/get-started/maestro-mcp
- https://maestro.dev/blog/maestro-cli-2-7-0
- https://github.com/mobile-dev-inc/maestro/blob/main/CHANGELOG.md
