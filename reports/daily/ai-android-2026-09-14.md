# AI + Android Daily Report

日期：2026-09-14  
对照：2026-09-11 快照。不写 AI 新闻。只回答相对上次核对：**有没有新的能力能进 Android 团队流程，以及能不能省工程师时间。**

## Executive Summary

本窗口（09-11 → 09-14，周一 cron）**没有新产品把生产 ANR、Perfetto 复测、Cloud 模拟器或 Jenkins 接成闭环。** 官方技能库、Crashlytics MCP 工具面、Maestro CLI、Android Bench 排行均未前进。

**AI 是否真正节省 Android 工程师时间？**

- 答案与 09-11 相同，入口未换。
- Crash / Leak / 官方 skill 覆盖的迁移：**是**。省的是定位文件与机械改配置，不省竞态、无符号表、视觉验收。
- 读一张启动/卡顿 Perfetto：**是**（SQL 可复现）。**不是**「修好再对比指标」。
- 未接 Crashlytics / Gradle / 设备 / `.perfetto-trace` 的通用 Agent：**否**。只增加 review 负担。

团队本周不要换 Adopt 宿主，不要并行铺新工具。把还没做完的 Crash PoC 和 Perfetto 分诊 PoC 做完，比追新 Agent 品牌更省时间。

## New AI Capabilities

相对 `snapshots/ai-agent/2026-09-11.md`：**无新增能力。**

详见 `diffs/ai-agent/2026-09-14.md`。下列日期变化只更新快照事实，不进流程：

| 核对项 | 09-11 快照 | 今天 | 是否新闭环 |
|---|---|---|---|
| Crashlytics MCP 专用页 | 2026-09-10，Experimental | 2026-09-11，仍 Experimental，工具未扩 | 否 |
| Android CLI 文档 | 2026-09-01 | 2026-09-11；命令面未增，仍无 `android build` | 否 |
| `android/skills` | 24 个 SKILL.md，commit 2026-09-07 | 仍 24，无新 commit | 否 |
| Maestro CLI | 2.10.0 | 2.10.0 | 否 |
| Android Bench | 2026-08-11；Opus 5 91.8 | 未刷新 | 否 |
| Studio MCP stdio | 不支持 | 不支持 | 否 |
| Cloud 模拟器 / nested KVM | 无官方能力 | 论坛 09-10 仍报 `KVM_CREATE_VCPU` BUG | 否 |

## Android Use Cases

### Crash — 维持 Adopt，无增量

继续 Quail 4 AQI Fix with AI，以及非 Studio Agent 上的 Crashlytics MCP。MCP 仍 Experimental，无 ANR 工具。  
**不要**要求在 Studio 里装 Firebase MCP（无 stdio）。

### ANR — 仍未闭环

生产 ANR 没有「Fix with AI + 复现」按钮。Maestro 的 `anr-report.txt` 只覆盖**该次 UI 跑测**。Hold 自动修。

### Performance — 维持 Trial 分诊，后半环仍断

`android-profiler` → Perfetto SQL 的分析闭环未变。自动改代码 + 再采同一指标仍 Hold。  
本周没有新产品把 APA 接到「修复可复现」。

### Testing / Build / Review / Release / Documentation

无新闭环。Journeys 文档仍 08-31；Maestro 仍 2.10.0；编译失败仍靠 Gradle + Agent，不靠新的 `android build`；Bugbot 仍无官方 Android 规则；发版 / Play 签署仍人控。

### 跨平台迁移

Rabbit 1 仍 Canary、仍停在编译检查。没有源工程的团队继续忽略。

## Agent / MCP

工具面相对 09-11 **零修正**：

1. **Android Studio Quail 4 Agent** — 生产默认。Crash/Leak + 预装 skills。
2. **Firebase MCP** — 只给 Cursor / Claude Code / Codex / Gemini。Studio 不硬接。
3. **Android CLI + `android skills add --all`** — 给非 Studio Agent；技能数仍 24。
4. **`android-profiler` skill** — 性能分诊；只分析。
5. **Maestro MCP 或 Journeys** — 仍只选一条 UI 资产。

Cloud / Scheduled Agent：JVM 单测可以；模拟器官方未交付。Self-hosted machines 可自带 KVM 硬件，那是基础设施，不是官方 Android 设备闭环。

## Developer Productivity

| 重复劳动 | 相对 09-11 | 人还要做什么 |
|---|---|---|
| Crash 分诊与常见修复 | 不变 | 批准 diff、符号表、回归 |
| 官方 skill 迁移 | 不变（Studio 已预装） | 视觉/导航验收 |
| 读 Perfetto / 写第一版 SQL | 不变，能交给 Agent | 复录对比、定优化 |
| 生产 ANR | 不能自动修 | 人抓 trace |
| Maestro Cloud 失败看盘 | 不变 | 确认 selector 策略 |
| 发版 / Jenkins / Cloud 模拟器 | 不能 | 全部人控 |

**本周没有新的重复劳动被自动化。** 省时间仍然只发生在已经 Adopt / Trial 的三条线上。

## Watchlist Diff

### Added

无。

### Updated

- 全表 `Last checked` → 2026-09-14。
- `crashlytics-mcp`：文档日期 09-11，状态仍 Experimental。
- `android-cli-skills`：CLI 文档日期 09-11；技能数仍 24。

### Removed / Deprecated

无。

### No Significant Change

Studio Agent、APA/Perfetto、Journeys、Maestro、Rabbit 1、Bugbot、Cloud Agent、Claude Code、Android Bench、GitHub AW、社区 MCP、Jenkins。

## PoC Candidates

不新开 PoC。09-11 列出的验收标准仍然有效，且本周没有任何产品变化让它们过期。

### 仍应做（若尚未做完）

- **P0 Crash**：3 个有 mapping 的高用户数 issue；AQI 与 Crashlytics MCP 各走一条。成功：2/3 可编译，1 个能复现或单测盖住。
- **P1b Perfetto 分诊**：一张已知卡顿/启动 trace + `android-profiler`。成功：可复现 SQL + 工程师认可根因方向。不要验收「自动加速 x%」。

### 仍不做

- 生产 ANR 自动修复。
- Cloud Agent 启模拟器。
- Jenkins AI 构建分析。
- 无复测协议的「Agent 优化启动」。

## Recommendation

| 对象 | 级别 | 相对 09-11 |
|---|---|---|
| Android Studio **Quail 4** AQI + Leak Agent + 预装 skills | **Adopt** | 不变 |
| Android CLI + `android/skills --all`（非 Studio Agent） | **Adopt** | 不变 |
| Firebase Crashlytics MCP（值班机，非 Studio） | **Adopt** | 不变；仍 Experimental |
| android-profiler / Perfetto 分诊 | **Trial** | 不变；只试分析 |
| Maestro MCP（含 Cloud 失败调试） | **Trial** | 不变 |
| Journeys 核心 Happy Path | **Trial** | 不变；与 Maestro 二选一 |
| Bugbot + Android `BUGBOT.md` | **Trial** | 不变 |
| Rabbit 1 跨平台迁移 | **Assess** | 不变；无源工程则忽略 |
| GitHub Agentic Workflows | **Assess** | 不变 |
| Perfetto 自动修复并复测 / 生产 ANR 自动修 | **Hold** | 后半环仍断 |
| Cursor Cloud 模拟器 / Jenkins + AI | **Hold** | 不变 |

**给 Android 团队的一句执行建议：**  
不要因为这是周一周报就换工具。默认 IDE 继续 Quail 4；把「Crash 闭环验收」和「一张 Perfetto 的 SQL 分诊」做完再谈下一层自动化。

## Sources

- https://developer.android.com/ai-in-android
- https://developer.android.com/studio/releases
- https://developer.android.com/studio/preview/features （Last updated 2026-09-09）
- https://developer.android.com/studio/gemini/agent-mode （Last updated 2026-07-14）
- https://developer.android.com/studio/gemini/skills （Last updated 2026-09-11）
- https://developer.android.com/studio/gemini/add-mcp-server （Last updated 2026-08-31）
- https://developer.android.com/studio/gemini/analyze-crashes-with-aqi
- https://developer.android.com/studio/gemini/journeys （Last updated 2026-08-31）
- https://developer.android.com/tools/agents
- https://developer.android.com/tools/agents/android-cli （Last updated 2026-09-11）
- https://developer.android.com/tools/agents/android-skills （Last updated 2026-09-02）
- https://developer.android.com/android-performance-analyzer/analyze/ai （Last updated 2026-09-04）
- https://developer.android.com/bench （Latest results as of August 11th）
- https://github.com/android/skills （24 × SKILL.md；HEAD 2026-09-07 v1.0.11）
- https://firebase.google.com/docs/crashlytics/ai-assistance-mcp （Last updated 2026-09-11）
- https://firebase.google.com/docs/ai-assistance/mcp-server （Last updated 2026-09-10）
- https://docs.maestro.dev/get-started/maestro-mcp
- https://github.com/mobile-dev-inc/maestro/releases （CLI 2.10.0，2026-08-31）
- https://forum.cursor.com/t/cloud-agent-kernel-issue-amx-state-corruption-unusable-nested-vmx/171293 （2026-09-10）
- https://cursor.com/docs/cloud-agent
- https://plugins.jenkins.io/ai-agent
