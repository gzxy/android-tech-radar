# AI + Android Daily Report

日期：2026-09-10  
范围：首次建档。不写 AI 新闻，只回答：这些能力能不能进 Android 团队流程，以及能不能省工程师时间。

## Executive Summary

**能真正省时间的，已经不是「会写 Kotlin 的聊天框」，而是接到工程产物的闭环。**

今天可落地的完整闭环只有三条：

1. **Crash**：Play/Crashlytics → Android Studio AQI 或 Crashlytics MCP → 读仓库 → 改代码 → 人审 → 回写 issue。
2. **重复迁移劳动**：官方 `android/skills`（edge-to-edge、Navigation 3、AGP 9、XML→Compose、R8）+ Android CLI。
3. **UI 冒烟起草**：Maestro MCP（确定性 YAML 进 CI）或 Journeys（自然语言，每次都要模型）。

**ANR、通用性能、架构分析、Jenkins、Cloud 模拟器** 仍停在「分析或实验」，不能当流程。

**是否真正节省 Android 工程师时间？**

- Crash 分诊与常见 NPE/生命周期修：是。从「打开控制台 + 对 stacktrace + 搜代码」压到「批准 diff」。
- LeakCanary 已定位的泄漏：是。Agent 写解除引用，人复测 heap。
- 官方 skills 覆盖的迁移：是。这些是模型单独做会写错、人做又机械的工作。
- 未接 MCP/CLI 的通用 Agent：否。只会增加 review 负担。

## New AI Capabilities

今日为基线，全部记为新增入库（详见 `diffs/ai-agent/2026-09-10.md`）。

| 能力 | 输入 | Agent 动作 | 验证 |
|---|---|---|---|
| AQI Fix with AI | Crashlytics / Vitals stacktrace | 读源码、出计划、改代码 | 官方称 apply 后 verify；需人复现 |
| LeakCanary Fix with Agent | Profiler 泄漏轨迹 | 解释 retain 链、写补丁 | 需再跑 Profiler，不是自动 |
| Crashlytics MCP | issue id / 用户数 / event | 拉数、改代码、写 note、关 issue | 测试靠 Gradle/CLI，MCP 本身不跑测 |
| Android CLI + skills | 迁移/文档/设备任务 | 按 SKILL.md 改项目，调 CLI | `studio analyze-file` / Gradle / 设备截图 |
| Journeys | 自然语言步骤 | 看屏 tap/type/swipe | 设备执行 + reasoning 面板 |
| Maestro MCP | 「测这个流程」 | 写 YAML、跑、自修 | 模拟器/真机；YAML 可进 CI |
| Bugbot Autofix | PR diff | 评论 → Cloud Agent 修 | CI check；Android 规则需自写 |
| GitHub Agentic Workflows | CI 失败日志 | 判断瞬时/永久、开修复 PR | `./gradlew` 再跑 |

## Android Use Cases

### Crash — 进入流程

闭环已在官方产品里写死：

```text
生产 Crash
 ↓
AQI 或 /crashlytics:connect
 ↓
读本地仓库 + 完整 stacktrace
 ↓
根因与修复计划
 ↓
改 Kotlin/Java
 ↓
人批准 + 单测/复现
 ↓
Crashlytics note / close
```

省的是 On-call 前 30–90 分钟的「定位文件 + 解释崩溃」。**不省**「多线程竞态、厂商 ROM、无符号表 R8」这类仍要人盯的问题。R8 场景应先挂 `r8-analyzer` skill 和 mapping。

### ANR — 未闭环

AQI 能列出 ANR，Insights 能摘要。主线程等待、锁、binder、过度布局没有等价于 Crash 的「Fix with AI + 复现」按钮。Agent 可以改代码，但 **Verify 需要 systrace / Perfetto / 复现路径**，今天没有产品把这一段接上。

**建议：Hold 自动修复；Assess 用 Agent 写 ANR 复盘文档 + 标可疑帧。**

### Performance — 仅 Leak 一段可试

LeakCanary 进 Profiler 后，泄漏从「装 debug 包 + 在手机上等分析」变成桌面分析 + 跳声明 + Agent 补丁。这是真重复劳动。

启动、帧时间、内存抖动、电量：`android-profiler` skill 只接地，不构成「改代码 → 再采同一指标」。

### Testing — 可 Trial，不要替换现有金字塔

- **JVM 单测 / Robolectric**：Cloud Agent、Claude Code、Codex + `./gradlew test` 已能闭环。这是最便宜的验证。
- **Journeys**：给核心 Happy Path 写自然语言冒烟。抗 UI 微调，但每次消耗模型、手势能力不全、configuration cache 有坑。适合「还没写 UI 测」的模块，不适合替代回归套件。
- **Maestro MCP**：Agent 起草后留下 YAML。**这才是能进 CI 的测试资产。** 优先 Trial。

### Build — 编译失败可做，构建系统升级靠 skill

- Gradle 编译错误：Agent + 压缩后的 `file:line`（AndroidBuildMCP 或原始 Gradle）能修大部分 Kotlin 编译/依赖冲突。
- AGP 9：用官方 `agp-9-upgrade` skill，不要让模型自由发挥。
- Android CLI **不负责编译**，只负责环境、部署、设备、Studio 桥。

### Code Review — 可 Trial，必须写 Android 规则

Bugbot 对任何仓库都能跑，但默认不懂 Compose 重组、Lifecycle、Main thread I/O、`remember` 误用。没有 `.cursor/BUGBOT.md` 的 Android 规则，Review 会变成通用风格喷子，**不省时间**。

Autofix 只应开给「测试已覆盖的高置信缺陷」，不要对 UI 行为自动修。

### Release / Documentation / Repository Analysis

- Release：无可靠的「AI 自动签 Play 并回滚」闭环。最多让 Agent 写 changelog、检查 `targetSdk` / permission。
- Documentation：`android docs search|fetch` 把官方知识库接到终端，比网页搜索快。写模块 README 能省时间，但要挂在 PR 里审。
- Repository Analysis：`android describe` + `studio find-usages` 对依赖/符号有用；「架构评分」无 Verify，不当流程。

### AI + Jenkins / CI/CD

- **Jenkins**：Hold。没有官方 Android Agent 协议。
- **GitHub Actions + Agentic Workflows**：Assess。适合 Dependabot/编译红灯自愈，必须限制权限（默认只读 + safe output）。
- **Cursor Scheduled Agent**：适合本仓库这类日报，不适合替代 Android CI。

## Agent / MCP

团队最小工具面（按优先级）：

1. **Android Studio Quail 2 Agent** — Crash/Leak 主路径，工程师仍住在 IDE。
2. **Firebase MCP** — On-call 与非 Studio Agent（Cursor / Claude Code）共用同一套 Crash 数据。
3. **Android CLI + `android skills add --all`** — 给 Cursor / Claude / Codex / Gemini 同一套官方技能。
4. **Maestro MCP 或 Journeys** — 只选一条做 UI 冒烟，避免两套不可比资产。
5. **（可选）Gradle Tooling API MCP** — 多 module 依赖诊断。

不要堆社区 MCP。每个 MCP 都是权限面和幻觉源。

Cloud / Scheduled / Repository Agent：可以修「有 JVM 测试的 Kotlin」，不能假装能复现 ANR。

## Developer Productivity

| 重复劳动 | 今天能否交给 Agent | 人还要做什么 |
|---|---|---|
| Crash 分诊与常见修复 | 能 | 批准 diff、确认符号表、回归 |
| ANR | 不能自动修 | 人抓 trace，Agent 最多辅助阅读 |
| Leak | 能起草补丁 | 再跑 Profiler |
| XML→Compose / edge-to-edge / Nav3 / AGP9 | 能（官方 skill） | 视觉验收、导航回归 |
| 写第一版 E2E | 能（Maestro） | 稳定 selector、抽公共 flow |
| PR 里 Android 生命周期/线程问题 | 能（自写规则后） | 架构取舍仍归人 |
| Gradle 编译红 / 依赖冲突 | 能 | 锁版本策略 |
| 发版、商店审核、签名 | 不能 | 全部人控 |
| 架构评审 | 不能当门禁 | 可当讨论稿 |

Android Bench 说明模型差距很大（约 37%–92% 任务解决率）。**选错模型会负节省。** 团队应用 Bench 选默认模型，而不是用营销名。

## Watchlist Diff

无历史快照。今日新建 `watchlist/ai-agent.md`，14 个条目入库。

新增 Watch：`as-quail2-agent`、`crashlytics-mcp`、`android-cli-skills`、`journeys`、`maestro-mcp`、`cursor-bugbot`、`cursor-cloud-agent`、`claude-code`、`android-bench`。

新增 Evaluate：`github-aw`、`gbox-mcp`、`androidbuild-mcp`、`gradle-mcp`。

新增 Discover/Hold：`jenkins-ai`。

完整能力列表见 `diffs/ai-agent/2026-09-10.md`。下一跑次只报相对本快照的增量。

## PoC Candidates

按「一周内能在真实 app module 看到工时变化」排序。

### P0 — Crash 闭环（Adopt 前的验收）

1. 选 3 个已有 mapping 的 Crashlytics 高用户数 issue。
2. 路径 A：Studio AQI → Fix with AI。路径 B：Cursor/Claude + `/crashlytics:connect`。
3. 成功标准：2/3 给出可编译 diff；至少 1 个能被现有单测或手工复现验证；Agent 在 issue 留下 note。
4. 失败则不要全员推广，只留给 NPE/空指针/明显生命周期错误。

### P1 — 官方 skills 迁一条机械变更

选 `edge-to-edge` 或 `r8-analyzer`（不要一上来做全量 XML→Compose）。

成功标准：Agent 按 skill 改完，`./gradlew :app:assembleDebug` 过，视觉抽检 3 个屏幕。

### P2 — Maestro 冒烟一条主路径

登录或首页搜索。成功标准：留下可在 CI 跑的 YAML，失败时 Agent 能自修一次 selector。

### 不做的 PoC

- Cloud Agent 里启动 Android 模拟器。
- ANR 自动修复。
- Jenkins 插件「AI 构建分析」。
- 无测试的架构重构。

## Recommendation

| 对象 | 级别 | 理由 |
|---|---|---|
| Android Studio Quail 2 AQI Fix with AI + LeakCanary Fix with Agent | **Adopt** | 唯一官方、就地、人在回路的 Crash/Leak 闭环 |
| Android CLI + `android/skills --all`（Cursor/Claude/Codex 各装一份） | **Adopt** | 把「模型会写错的 Android 流程」变成可更新技能，而不是 prompt |
| Firebase Crashlytics MCP（On-call 值班机） | **Adopt** | 数据进 Agent；Experimental，限制在排障，不写进 SLA |
| Maestro MCP 主路径冒烟 | **Trial** | 唯一能留下确定性 CI 资产的 UI Agent |
| Journeys 核心 Happy Path | **Trial** | 与 Maestro 二选一作补充；AGP 9 与手势限制要先评估 |
| Bugbot + Android `BUGBOT.md` + 有限 Autofix | **Trial** | 无 Android 规则则 Hold |
| GitHub Agentic Workflows 修编译/依赖红灯 | **Assess** | 权限与误修风险高于收益，先单个仓库 |
| Cursor Cloud Agent 做 Instrumented/ANR | **Hold** | 模拟器未交付 |
| Jenkins + AI | **Hold** | 无闭环 |
| 仅「用了 AI」的项目/演示 | **Hold** | 不回答省时间问题 |

**给 Android 团队的一句执行建议：**  
先把 Crash 和官方 skills 接进现有 Studio/On-call，再谈 Cloud Agent 和自动发版。前者已经能减重复劳动；后者还在断环。

## Sources

- https://developer.android.com/blog/posts/android-studio-quail-2-is-stable-multi-task-with-the-android-studio-ai-agent
- https://android-developers.googleblog.com/2026/05/whats-new-android-developer-tools.html
- https://developer.android.com/studio/gemini/analyze-crashes-with-aqi
- https://developer.android.com/studio/debug/app-quality-insights
- https://developer.android.com/studio/gemini/journeys
- https://developer.android.com/tools/agents/android-cli
- https://developer.android.com/tools/agents/android-cli/journeys
- https://developer.android.com/tools/agents/android-skills
- https://developer.android.com/studio/gemini/skills
- https://github.com/android/skills
- https://developer.android.com/bench
- https://developer.android.com/blog/posts/evolving-how-ll-ms-are-measured-for-android-the-next-era-of-android-bench
- https://firebase.google.com/docs/crashlytics/ai-assistance-mcp
- https://firebase.google.com/docs/ai-assistance/mcp-server
- https://firebase.blog/posts/2025/11/crashlytics-mcp-with-gemini-cli/
- https://maestro.dev/mcp
- https://cursor.com/docs/bugbot
- https://github.blog/changelog/2026-06-11-agentic-workflows-no-longer-need-a-personal-access-token/
- https://android-developers.googleblog.com/2026/04/build-android-apps-3x-faster-using-any-agent.html
