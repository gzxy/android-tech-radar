# Android Open Source Daily Report

Date: 2026-09-14
Run type: incremental vs `snapshots/open-source/2026-09-11.md`（中间隔了周末）

## 1. Executive Summary

09-11 之后三天，真正改排期的不是新仓库，而是 Google 把上周拆开的两条 Agent 线接上了：

1. **ADK Kotlin 在未发 1.0.2 的情况下，把 AppFunctions 收成了官方 Toolset。** `AppFunctionsToolset`（`6f349ef5af`）让进程内 `LlmAgent` 直接发现并调用本 App 的 `@AppFunction`。默认只看自己的包；设备没有 AppFunctions 时贡献 0 个 tool，不崩。依赖是 `androidx.appfunctions` **1.0.0-alpha11** 的 `compileOnly`——消费方必须自己声明。官方样品仓同一天把 Testing Agent 切到 `AppFunctionState` / observe / search。09-11 说「ADK 和 AppFunctions 不要做成同一个里程碑」仍然对**系统 Gemini EAP** 成立，但对**自己 App 里的 Agent** 已经过时：函数写一次，先用 Toolset 自测。
2. **阿里 ARouter 在 develop 合并了未发布的 KSP2 编译器。** PR #1088（分支名 `codex/ksp2-support`）新增独立工程 `arouter-compiler-ksp`，KSP 2.3.12，消费矩阵含 AGP 8.12 / 9.0 / **9.3.2**。运行时契约不变，artifact 是本地 `0.1.0-SNAPSHOT`。这不是「路由技术复活」，是 2020 年的 kapt 遗产被 AGP 9 / KSP 2 逼着续命。不要把 snapshot 打进生产。
3. **CMP 1.13.0-alpha01 漏记补上；大厂样板继续吃官方补丁。** 1.13.0-alpha01 在 09-10 打 tag，09-11 写成「无新 tag」。Android **minSDK 升到 24**。Slack Foundry main 在 09-13 把 Kotlin 2.4.10 → **2.4.20**。Paparazzi 修了 `--parallel` 下 `cleanRecord` 删掉刚录 golden 的竞态。

没有出现：ADK 1.0.2、Kuikly Compose DSL 正式版、Lynx 4.2、KSP 2.3.13。Lynx 多了一个空 notes 的 **4.0.3** 维护 tag，不要当成 4.2。  
华为 / 百度 / 网易 / 京东再扫一轮，仍没有可迁入大型 Android 工程的新开源。

## 2. Domestic Big Tech

### Tencent

- **KuiklyUI 仍是 2.27.0。** HEAD 是 H5 父拖拽/子点击冲突。`chore: update 2.1 publish version` 只是发布脚本，不是 2.28，也不是 Compose DSL 正式发版。KuiklyUI-AI 继续停在 08-10。
- **dsh-kuikly-expert** 无新提交。同组织多了一个 `dsh-create-app`（1★、同文案），不入库。
- libpag / Hippy / MMKV：无版本变化。

### ByteDance / Lynx Family

- **Lynx 功能线仍是 4.1.0。** 09-11 打了 **4.0.3**，release body 为空——4.0 维护线，不是路线图里的 4.2（仍指向 2026-10）。develop 上继续回滚：Android Markdown 集成、iOS 异步 UI / 圆角。**继续钉 4.1.0，不要追 develop。**
- **lynxtron v0.0.22**（09-11）：桌面 CEF 打包、开发态 AutoLink 打进 native、Linux TestBench replay。对已经押 Lynx 桌面的团队有意义；纯 Android 宿主忽略。
- **lynx-stack** 09-11 切了一组包（`create-rspeedy@0.17.2`、`create-lynx-library@0.6.1` 等），并在 GenUI bench 里复用 UI Judge agent。这是 Lynx「AI-ready」路线图的工具链侧声响，不是 Android 工程 SDK。
- btrace / CodeLocator / BlockFramework：无新版本。

### Alibaba / Ant

- **ARouter：release 仍是 2020 的 1.5.1，develop 不再只是 interceptor 补丁。** 独立 KSP2 编译器已合入：路由 / Provider / Autowired / Interceptor / 可选文档；增量删除和祖先变更有测试；和旧 APT 可按模块混用（**同一模块只能选一种后端**）。Kotlin 字段只保证 `@JvmField` 和可写 `lateinit`。官方写明「unpublished development artifact」。已用 ARouter 且在迁 AGP 9 / 去 kapt 的大仓：列入观察，等 Maven 坐标，不要 `mavenLocal` 进主干。
- **MNN 3.6.1 未发版。** main 是 RVV KV-cache / attention 和 OpenCL FlashAttention。对 Android 宿主 API 无新约束。已用 MNN 的团队当性能提交跟，不要当新推理栈。
- SoloPi：无变化。

### Meituan / Kuaishou / Others

- Logan / KOOM / 一代热修复：无复活。
- 华为 HMS-Core 仍是 Scan / IAP / Video Editor demo。百度本轮搜索无 Android/Kotlin 工程仓。网易 `NetEase/skills` 仍停在 2026-03。京东 `jd-opensource` 无 Android/Kotlin 新信号。小米 MACE 继续被 MNN 甩开。

## 3. International Big Tech

### Google

- **ADK Kotlin：版本号还是 1.0.1（09-10 09:25Z），main 已经能把 App 当自己的 MCP。** 09-11 当天连续合入：转换层 → Toolset → 把 App 级 guidance 注入 instructions → 真机 E2E → workflow 可恢复修复。关键约束：
  - `@ExperimentalAppFunctionsFeature`，未打 tag；
  - 必须自己加 `androidx.appfunctions:1.0.0-alpha11`；
  - 返回 `PendingIntent`、当前被 App 关掉的函数，不会交给模型；
  - 看别人的包需要 `EXECUTE_APP_FUNCTIONS` + 可见性，默认只看自己。
  09-11 已报的 MCP reject 保活 / `onRunError` 仍未进 1.0.2。**生产依赖继续钉 1.0.1；PoC 可以按 main 的 Toolset API 写，但不要把 unreleased 坐标写进 version catalog。**
- **appfunctions 样品仓不再是「8 月停更的参考」。** PR #52 把 Testing Agent 对齐 alpha11：`AppFunctionState` 替代 `AppFunctionMetadata#isEnabled`，search/observe API 跟上平台。alpha11 本身是 08-26 的 Jetpack，不是本周新库；本周新的是「样品 + ADK 同时按 alpha11 写」。
- android/skills：无新 tag。AppFunctions skill 仍按四段生命周期。
- Dagger / KSP / Now in Android：无新版本。KSP 仍停在 2.3.12，2.3.13 分支未发。

### JetBrains

- **Compose Multiplatform 1.13.0-alpha01**（09-10，本轮补记）。对 Android 有含义的只有：**minSDK 24**。其余亮点是 Desktop AppCDS/AOT、Web viewport 出实验、Hot Reload 1.3.0-alpha01。Skottie 拆出核心二进制——用 Lottie/Skottie 的 KMP 模块要显式加依赖。稳定版继续 1.12.0。
- Kotlin 2.4.20 无新 tag。HEAD 是 Analysis API / Wasm。
- **kotlin-agent-skills 不再停在 07-21。** 可见提交补了 Kotlin Toolchain（原 Amper）一族 skill：`kotlin-tooling-kotlin-toolchain`、Gradle→Toolchain 整仓迁移、plugin authoring。CLI 自称 Alpha，配置是 `project.yaml` / `module.yaml`。**大型商业 Android 不要做「弃 Gradle」PoC。** 只说明 JetBrains 在把「Agent 怎么改构建」从 AGP 9 迁仓扩到下一代 CLI。

### Slack / Cash App / Square

- **Foundry 0.36.0 未发版，main 对齐 Kotlin 2.4.20。** 和 09-11 Circuit 当天吃 Compose 1.12.1 是同一模式：样板仓库按天跟官方补丁。
- **Paparazzi 仍是 2.0.0-alpha05。** 两件测试正确性：
  1. `#2377`：多模块 `--parallel cleanRecordPaparazzi*` 会在录完后被 `delete*Snapshots` 清掉 golden——大仓 CI 若偶发空 `snapshots/images/`，先怀疑这个，不要当业务 UI 回退；
  2. `#2383`：`NO_HIDE_DESCENDANTS` 整棵子树不再进 a11y legend（普通 `NO` 仍遍历子孙）。接在 09-11 的 `HideFromAccessibility` 过滤后面。
- Circuit / compose-lints / LeakCanary / Store：无版本变化。
- **OkHttp / Retrofit 的 GitHub 规范名现为 `lysine-dev/*`（Commonhaus）。** `square/okhttp` 会重定向。Maven 坐标未变，不是新实现，也不降低优先级。

### Airbnb / Uber / Meta / Others

- Fresco main 给流式 AVIF 做了按字节节流，并更新了内部 `.llms` 领域文档。不是 3.8，不必为 Android 接入改版本。
- Mavericks / RIBs / Lottie / Showkase / Litho：沉寂。

## 4. New Projects

本轮没有「第一次应该认真看」的新仓库。

上周已入库、本周才变厚的，不要再当新发现：`android/appfunctions`、`google/adk-kotlin`、`slackhq/compose-lints`。

明确不入库：`dsh-create-app`、把 Kotlin Toolchain 当成可替换 Gradle 的新项目、把 Commonhaus 重定向当成新的网络栈。

## 5. Major Project Changes

| Company | Project | Change | Technical Meaning | Recommendation |
|---|---|---|---|---|
| Google | ADK Kotlin | main 增加 `AppFunctionsToolset`（未发 1.0.2） | 进程内 Agent 官方消费本 App 的 AppFunctions；和系统 Gemini 共用同一套函数 | **改 PoC 结构**：函数写一次，Toolset 自测。生产继续钉 1.0.1 |
| Google | AppFunctions samples | Testing Agent 对齐 alpha11 | `AppFunctionState` / observe / search 成为实现规范 | 样品和 ADK 都按 **alpha11** 写，不要停在 alpha10 文档 |
| Alibaba | ARouter | develop 合并 KSP2 编译器（未发布） | 遗产路由开始给出 kapt 退出路径，矩阵已含 AGP 9.3.2 | **观察**。等正式坐标。禁止 snapshot 进主干 |
| JetBrains | CMP | 1.13.0-alpha01（补记） | Android minSDK 24；Skottie 拆包 | 稳定版留 1.12.0。min 21/23 的 KMP 模块不要跟 alpha |
| Slack | Foundry | main Kotlin 2.4.20 | 样板继续按天吃语言补丁 | 已用 Foundry / 对齐 Foundry 基线的仓跟上 2.4.20 |
| Cash App | Paparazzi | parallel `cleanRecord` 竞态；隐藏子树剪枝 | 大仓 CI 空 golden 可能是任务顺序，不是 UI 回归 | 已上 2.0-alpha 且开 `--parallel` 的模块：**先吃这两笔 main，再查 flaky** |
| ByteDance | Lynx | 4.0.3 空 tag；develop 继续回滚 | 4.0 维护，不是 4.2 | **钉 4.1.0** |
| ByteDance | lynxtron | v0.0.22 | 桌面打包/AutoLink | 只有桌面 KPI 才看 |
| JetBrains | kotlin-agent-skills | Kotlin Toolchain skills | Agent 开始会写 YAML 构建，替代 Gradle 的叙事出现 | 不排期。AGP 9 skill 继续用 |

## 6. Watchlist Diff

### Added

无。

### Updated

P0/P1 元数据已按 2026-09-14 GitHub API 回写。有技术含义的更新：

- `google/adk-kotlin`：HEAD 超前 1.0.1（AppFunctionsToolset）
- `android/appfunctions`：alpha11 样品
- `alibaba/ARouter`：KSP2 develop
- `JetBrains/compose-multiplatform`：Version → 1.13.0-alpha01
- `Kotlin/kotlin-agent-skills`：Last Commit → 2026-09-11
- `slackhq/foundry`：HEAD Kotlin 2.4.20
- `cashapp/paparazzi`：HEAD 竞态 / a11y
- `lynx-family/lynxtron`：v0.0.22
- `lynx-family/lynx-stack`：rspeedy 0.17.2
- `lynx-family/lynx`：记下 4.0.3 维护 tag
- `square/okhttp` / `square/retrofit`：注明 Commonhaus 重定向

### Deprecated / Inactive

无新增 archived。华为 / 百度 / 网易 / 京东继续空窗，不强制填表。

## 7. Industry Trend

只在证据变厚时升级，不把上周的结论再宣布一遍。

### 趋势 A 证据加强：同一套 AppFunctions，既是端上 MCP，也是进程内 ADK Tool

Google 现在把三件事写进同一周的代码里：

- App 向系统注册函数（Jetpack AppFunctions alpha11 + `android/appfunctions`）
- 系统 / Gemini 将来调这些函数（仍是 EAP）
- **App 自己的 ADK Agent 现在也能调这些函数**（`AppFunctionsToolset`，未发版）

叠加 09-11 已点名的 `android/skills`、CMP Hot Reload MCP、KuiklyUI-AI、Lynx AI-ready。

> 这可能代表 Android 工程领域正在形成行业趋势。

2026 下半年「App 内 AI」的设计问题从「做两套工具」变成「**函数契约写一次，消费方有两个**」。权限模型仍然不同：自己调自己不需要 `EXECUTE_APP_FUNCTIONS`；跨包 / 系统助理需要。PoC 先覆盖前者。

### 趋势 B 继续：kapt → KSP 从「新库默认」扩到「遗产库补课」

09-11：Dagger 文档宣布 KSP 稳定（2.60+ / KSP 2.3.9+）。  
09-12：ARouter 用独立 KSP2 工程覆盖 AGP 9.3.2，尽管 1.5.1 六年没发版。

Google + Alibaba 同时出现「编译期路由/DI 退出 kapt」。

> 这可能代表 Android 工程领域正在形成行业趋势。

大仓如果还把 kapt 当「等业务空窗再迁」，窗口已经不是 Dagger 一家的事。ARouter 用户不要抢 snapshot，但迁移设计可以现在做：那些字段是 `@JvmField` / `lateinit`，哪些模块先切。

### 趋势 C 继续：官方补丁被样板工程按天吸收

Foundry 在 2.4.20 发布后数日把构建基线推上去。Circuit 已在 09-10 吃 Compose 1.12.1。

> 这可能代表 Android 工程领域正在形成行业趋势。

### 明确还不是趋势

- Kuikly Compose DSL 正式发版、Lynx 4.2：未到点。
- Kotlin Toolchain 替换 Gradle：只有 Agent Skill，没有第二家 Android 大仓落地。
- 热修复 / 插件化：继续沉寂。
- 国内 GUI Agent 开源：仍无工程落地。

## 8. Recommended Projects

只推荐现在值得投入人天的。每个都回答四个问题。

### 1) AppFunctions + ADK `AppFunctionsToolset` — 立刻改 PoC 结构（仍不要等 1.0.2 上生产）

- **解决什么真实问题？** 用户对助理说「查订单 / 建草稿」时，模型应调用**已经存在的业务 API**，而不是再做一套聊天 WebView，也不该让 `@Tool` 和 `@AppFunction` 各写一遍同一件事。
- **为什么现在值得关注？** ADK main 把「自己的 Agent 调自己的函数」写成一等 API；样品和 Jetpack 已在 alpha11。系统 Gemini 仍是 EAP，所以现在做的是契约和自测，不是联调承诺。
- **能否迁移到大型商业 Android 项目？** 能。独立 `:appfunctions` 模块，`compileSdk 36`，KSP，先只读。ADK 侧 `compileOnly` 不够，必须自己声明 `androidx.appfunctions:1.0.0-alpha11`。Android 16 或带 extension 的 14；不支持的设备 Toolset 为空。
- **是否值得 PoC？** 值得。一周目标：2 个 `@AppFunction` + `AppFunctionsToolset(context)` 挂到 `LlmAgent` + `adb shell cmd app_function` 对照。**不要**把 `google/adk-kotlin` main 写进生产 catalog；等 1.0.2。

### 2) android/skills（AppFunctions skill）+ Dagger KSP — 立刻接入，不做业务 PoC

- **解决什么真实问题？** Agent 升 AGP / 写 AppFunction / 迁 Hilt-KSP 时会编出不能跑的工程。
- **为什么现在值得关注？** 样品 API 已到 alpha11；Dagger KSP 稳定结论未被撤回。
- **能否迁移？** 能。不进 APK。
- **是否值得 PoC？** 不必。装 skill；继续 Hilt 模块 kapt→KSP。

### 3) slackhq/compose-lints — 直接进 CI（结论不变）

- **解决什么真实问题？** Compose 稳定性 / slot / modifier 误用，单元测试抓不到。
- **为什么现在值得关注？** 无新版本，但 1.6.0 仍是最低成本的生产级检查。
- **能否迁移？** 能。Lint 配置。
- **是否值得 PoC？** 不必。接上。

### 4) Paparazzi — 已在跑 2.0-alpha 的模块跟 main，而不是新开 PoC

- **解决什么真实问题？** 无设备截图；本周修的是「并行录制被自己删掉」和 a11y 树过脏。
- **为什么现在值得关注？** 大仓 `--parallel` 会把 flaky 误判成 UI 回退。
- **能否迁移？** 能。仍是 alpha，不要规模替换 Espresso。
- **是否值得 PoC？** 没在用的模块：继续小组件库 PoC。已经在用：先合这两笔，再谈 2.0 稳定。

### 5) 昨天仍成立、今天没有被否定的推荐

- **Circuit：** 新模块 PoC 仍值得；0.38 Parcelable breaking 没有撤回。
- **KuiklyUI / Lynx：** 有跨端 KPI 再 PoC。今天没有新功能发版改变「嵌入、不要整包替换」。
- **MNN：** 已有端侧模型再对比。RVV/FlashAttention 不是换栈理由。
- **ARouter KSP：** **不推荐现在投入。** 等正式 artifact。可以先盘字段形态和模块边界。

### 明确不推荐现在投入

- 追 Lynx develop / 为 4.0.3 或 TransferView 改宿主。
- 把 ADK main 或 ARouter `0.1.0-SNAPSHOT` 写进生产依赖。
- 新选 Tinker / Shadow / Atlas / ByteX / 把 Gradle 迁到 Kotlin Toolchain。
- 为 OkHttp Commonhaus 重定向做任何迁移。
- 把系统 Gemini 联调写进本迭代目标。

## 9. Sources

- GitHub API（2026-09-14）：watchlist 仓库 metadata / latest release / HEAD commit
- [google/adk-kotlin `AppFunctionsToolset`](https://github.com/google/adk-kotlin/blob/main/core/src/androidMain/kotlin/com/google/adk/kt/tools/appfunctions/AppFunctionsToolset.kt)（`6f349ef5af` / `cc2928fb3a` / `7620e9fa7d` / `00de2d5e69`）
- [android/appfunctions PR #52](https://github.com/android/appfunctions/pull/52)
- [Jetpack appfunctions 1.0.0-alpha11](https://developer.android.com/jetpack/androidx/releases/appfunctions)（2026-08-26）
- [Overview of AppFunctions](https://developer.android.com/ai/appfunctions)
- [alibaba/ARouter PR #1088](https://github.com/alibaba/ARouter/pull/1088) KSP2
- [JetBrains/compose-multiplatform v1.13.0-alpha01](https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.13.0-alpha01)
- [Kotlin/kotlin-agent-skills kotlin-tooling-kotlin-toolchain](https://github.com/Kotlin/kotlin-agent-skills/tree/main/skills/kotlin-tooling-kotlin-toolchain)
- [slackhq/foundry #1855](https://github.com/slackhq/foundry/pull/1855) Kotlin 2.4.20
- [cashapp/paparazzi #2377](https://github.com/cashapp/paparazzi/pull/2377) cleanRecord race
- [cashapp/paparazzi #2383](https://github.com/cashapp/paparazzi/pull/2383) prune hidden a11y subtrees
- [lynx-family/lynx 4.0.3](https://github.com/lynx-family/lynx/releases/tag/4.0.3)
- [lynx-family/lynxtron v0.0.22](https://github.com/lynx-family/lynxtron/releases/tag/v0.0.22)
- [lysine-dev/okhttp](https://github.com/lysine-dev/okhttp)（`square/okhttp` 重定向，Commonhaus）
