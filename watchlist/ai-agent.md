# AI Agent Watchlist

基准日：2026-09-10  
上次核对：2026-09-14  
判断标准：AI 是否真正节省 Android 工程师时间，且能否形成

`Problem → Agent → Read Repository → Analyze → Modify Code → Run Test → Verify → Report`

只收录能进入 Android 团队研发流程的能力，不收录「某项目用了 AI」类新闻。

| ID | 项目 | 阶段 | 闭环完整度 | 节省时间？ | 建议 | 下次核对 |
|---|---|---|---|---|---|---|
| as-studio-agent | Android Studio Quail 4 Agent（AQI Fix with AI + LeakCanary Fix with Agent + 内置 23 skills + 并行 Agent） | Watch | Crash 高 / Leak 中高 / 迁移高 | 是（Crash/Leak/官方迁移） | Adopt | 每周 |
| crashlytics-mcp | Firebase Crashlytics MCP + `/crashlytics:connect` | Watch | Crash 高（Experimental） | 是（On-call 分诊） | Adopt | 每周 |
| android-cli-skills | Android CLI + android/skills 官方技能库（仍 24 个 SKILL.md） | Watch | 工具层完整 / 业务验证靠 Agent | 是（迁移/文档/设备） | Adopt | 每周 |
| apa-perfetto-agent | android-profiler skill + APA / Perfetto SQL（录制 → trace_processor 查询 → 根因） | Watch | 分析闭环完整，改代码+复测未接 | 是（读 trace），否（自动修） | Trial | 每周 |
| journeys | Android Studio / Android CLI Journeys | Watch | UI 测试执行闭环，不改业务代码 | 部分（冒烟，不替代 Espresso） | Trial | 每周 |
| maestro-mcp | Maestro MCP（含 Cloud 失败调试 + crash/ANR artifact） | Watch | 写测 → 跑测 → 自修 → YAML/Cloud | 是（E2E 起草与失败分诊） | Trial | 每周 |
| as-rabbit1-migrate | Android Studio Rabbit 1：iOS / Flutter / RN → Kotlin+Compose | Watch | 规划 → 改代码 → 编译检查 | 部分（机械移植；验收靠人） | Assess | 每周 |
| cursor-bugbot | Cursor Bugbot + Autofix + `/review` | Watch | Review → 评论 → Cloud Agent 修 | 部分（缺 Android 领域规则则噪声高） | Trial | 每周 |
| cursor-cloud-agent | Cursor Cloud / Scheduled / Repository Agent | Watch | 仓库闭环有，真机/模拟器闭环无 | 部分（JVM 单测/Lint/文档） | Assess | 每周 |
| claude-code | Claude Code + Firebase plugin + Android skills | Watch | 与 Crashlytics MCP / CLI 同构 | 是（终端 Agent） | Trial | 每周 |
| android-bench | Android Bench（官方 LLM 排行） | Watch | 评测闭环，不是工程闭环 | 间接（选型，不直接省工时） | Assess | 排行更新时 |
| github-aw | GitHub Agentic Workflows（CI 自愈） | Evaluate | Gradle 编译/单测失败可闭环 | 部分（依赖升级/编译失败） | Assess | 每月 |
| gbox-mcp | GBOX Android MCP | Evaluate | 云端/本地设备操控 | 未验证团队收益 | Assess | 每月 |
| androidbuild-mcp | AndroidBuildMCP / android-pilot-mcp | Evaluate | 社区 Build/ADB/Logcat | 未验证稳定性 | Assess | 每月 |
| gradle-mcp | Gradle Tooling API MCP（IlyaGulya / rnett） | Evaluate | 解析后依赖模型 | 部分（依赖诊断） | Assess | 每月 |
| jenkins-ai | Jenkins + AI 插件/脚本 | Discover | 无 Android 一等闭环 | 否 | Hold | 季度 |

## 2026-09-14 相对 09-11 的清单变化

- **无新增 / 无更名 / 无删除。** 本窗口没有新产品接上 Android 工程闭环。
- `crashlytics-mcp`：专用页日期 09-10 → 09-11，仍 Experimental，工具未扩环。
- `android-cli-skills`：CLI 文档日期 09-01 → 09-11；命令面未增；`android/skills` 仍 24 个 `SKILL.md`，HEAD 仍 2026-09-07 v1.0.11。
- Maestro CLI 仍 2.10.0。Android Bench 仍 2026-08-11。Studio MCP 仍无 stdio。
- Cloud 模拟器 / 生产 ANR 自动修 / Perfetto 自动复测 / Jenkins Android Agent：仍 Hold。

## 2026-09-11 相对基线的清单变化

- **更名**：`as-quail2-agent` → `as-studio-agent`。生产入口已是 Quail 4 Stable（2026-09-01），不再以 Quail 2 为 Adopt 宿主。
- **新增 Watch**：`apa-perfetto-agent`（官方把 Perfetto 分析写进 android-profiler / APA AI 页）。
- **新增 Watch**：`as-rabbit1-migrate`（Rabbit 1 Canary：跨平台工程迁到原生 Android）。
- **maestro-mcp 补记**：Cloud `describe_cloud_run` + 本地/Cloud `crash-report.txt` / `anr-report.txt`。CLI 当前 2.10.0。
- 官方 GitHub `android/skills` 仍 24 个 `SKILL.md`；最近提交 2026-09-07（plugin v1.0.11），无新技能文件。
- Crashlytics MCP 文档 2026-09-10 仍 Experimental。Studio MCP **不支持 stdio**，Crashlytics/Maestro 不能装进 Studio Agent。

## 收录规则

进入 Watchlist 必须满足至少一条：

1. 官方或可复现文档证明 Agent 能读仓库并改代码。
2. 能接到 Crash / ANR / Build / Test / Review 的真实输入，而不是聊天摘要。
3. 有 Verify 步骤（Gradle 测试、设备跑测、Profiler 复测、CI check）。

不收录：

- 模型发布、融资、演示视频。
- 「用 AI 写了一段 Kotlin」而无验证。
- 无法接到 Android 工程产物（APK、logcat、stacktrace、Gradle 失败日志、Perfetto trace）的通用聊天机器人。

## 当前优先闭环

1. **Crash**：Crashlytics / Play Vitals → AQI 或 MCP → 读源码 → 改代码 → 单测/复现 → 回写 issue note。
2. **Memory Leak**：Profiler LeakCanary → Fix with Agent → 复测 heap。
3. **重复劳动迁移**：Studio 内置 skills 或 `android skills add --all`（edge-to-edge、Navigation 3、AGP 9、XML→Compose、R8）。
4. **Performance 分诊**：录 Perfetto → `android-profiler` → `trace_processor` SQL → 根因报告。自动改代码+复测仍 Hold。
5. **UI 冒烟**：Journeys 或 Maestro MCP → 设备执行 → 保留可回归产物；Maestro Cloud 失败可用 Agent 拉 artifact。
6. **PR Review**：Bugbot + `.cursor/BUGBOT.md` Android 规则 → Autofix 仅修高置信问题。
