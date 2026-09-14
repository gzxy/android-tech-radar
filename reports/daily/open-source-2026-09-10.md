# Android Open Source Daily Report

Date: 2026-09-10
Run type: first baseline (watchlist + snapshot established)

## 1. Executive Summary

今天最重要的不是又多了一批 GitHub 仓库，而是三件事叠在同一周：

1. **Google ADK for Kotlin 进入 1.0。** `google/adk-kotlin` 在 2026-09-07 发 1.0.0，今天（2026-09-10）已补 1.0.1。这是第一份面向 Android / JVM / KMP 的官方 Agent SDK：同一套 `LlmAgent` 可以接 LiteRT-LM 端侧、ML Kit Gemini Nano、Firebase AI，并用 KSP `@Tool` 生成类型安全工具，也支持 MCP Toolset。星标只有 199，但对商业 App 的迁移价值远高于星标。
2. **国内跨端框架按月交付。** 字节 Lynx `4.1.0`（2026-09-07）已按 2026 Roadmap 切到月更；腾讯 KuiklyUI `2.27.0`（2026-09-03）几乎周更，并在 Compose DSL 上加了 KSP 页面注册。两边的 2026 Roadmap 都把 **AI / MCP / Skills / 对 LLM 友好的 API** 写成主航道。
3. **AGP 9.3 已经不是新闻，而是样板工程默认值。** Google Now in Android 升到 Gradle 9.7.1 + AGP 9.3.2 并打开 project isolation；Slack Circuit 的 changelog 已出现 `Update agp to v9.3.2`；Slack Foundry 构建基线是 AGP 9.3.1 / Gradle 9.6.1 / Kotlin 2.4.10。大厂如果还停在 AGP 8 + 手写 `kotlin-android`，差距已经是工程结构问题，不是版本号问题。

同步信号：`android/skills` v1.0.11（7277★）和 `Kotlin/kotlin-agent-skills` 把 AGP 9 / Navigation 3 / R8 / KMP 迁移做成 Agent Skill；Compose Multiplatform 1.12.0 给 Hot Reload 加了 MCP Server。  
**这可能代表 Android 工程领域正在形成行业趋势：框架不再只提供 SDK，而是同时提供 Agent Skill / MCP，让 AI 能稳定改工程。**

国内一代热修复/插件化（AndFix / Atlas / Robust / Matrix / QMUI）继续沉寂。例外是阿里 ARouter 在 2026-09-05 修了 interceptor 重初始化——值得看一眼是否有人在为新 minSDK 续命，但不构成新技术方向。

## 2. Domestic Big Tech

### Tencent

- **KuiklyUI 2.27.0**：KMP 一套代码打 Android / iOS / Harmony / Web / 小程序 / macOS。本版关键变化是 Compose 侧 `KuiklyModulePages` + KSP，页面注册从手写名单变成编译期生成。Roadmap 2026 把 MCP Server、Rules、Skills、Figma→代码、存量 React/Vue/Flutter 转码写成「AI 驱动开发」主线。
- **KuiklyUI-AI**（126★，2026-04 新建）：官方 Skills/Rules，覆盖 Kuikly DSL、Compose DSL、原生 View 扩展、资源打包。星标低，但是腾讯 TDS 自己在补「AI 怎么正确写 Kuikly」的缺口。
- **MMKV 2.4.2**：跨 Android / iOS / OHOS / KMP 的 mmap KV。本版修了过期时间常量（原先一年在多端被算成 30 年）、空 byte array / UTF-8 一致性、Harmony / Flutter SPM。仍是商业 App 默认候选存储。
- **libpag 4.5.94、Hippy 3.3.7 LTS**：libpag 几乎日更；Hippy 昨天还在修 Android RecyclerView「复用 View 仍 attached」崩溃。说明腾讯跨端/动画引擎没有停，但叙事已经让位给 Kuikly。
- **Tinker / Shadow**：只有修补，没有新架构。新项目不要再以它们为默认动态化方案。

### ByteDance / Lynx Family

- **Lynx 4.1.0**：2026-07 的 4.0 之后按月发 4.0.1 / 4.0.2 / 4.1.0。Roadmap 承诺 2026-09 就是 4.1，节奏兑现。3.8 引入 Autolink：npm 包装 `lynx.lib.json`，Android 侧用 `org.lynxsdk.library-settings` / `org.lynxsdk.library-build` 自动注册 Native Module，不再改每个宿主的 `build.gradle.kts`。
- **生态仓库都活着**：primjs 4.1.1、lynx-devtool、lynx-stack（Rspack/Rspeedy）、lynxtron v0.0.21（Lynx+Electron，30★）。低星仓库里 lynxtron 值得记——这是 Roadmap 点名的桌面方向，不是玩具。
- **btrace 3.1.0**：Perfetto 级方法/原因追踪，本版加 Harmony。对「为什么慢」而不是「慢了多少」有用。
- **CodeLocator 2.0.5**：2025-08 已跟 K2 和新 IDE，之后无新版本。
- **BlockFramework**（150★）：字节内部大页多团队解耦 + 异步 inflate/bind。开源后几乎没动，先观察不要上生产。
- **ByteX / AlphaPlayer**：已 archived。Transform API 时代的字节码平台不要再评估。

### Alibaba / Ant

- **MNN 3.6.1**：阿里端侧推理，定位已明确写成 on-device LLM / Edge AI，昨天还在修 OpenCL tuning。和 Google ADK + LiteRT-LM 是同一赛道的国内选项。
- **ARouter**：官方 release 仍停在 2020 的 1.5.1，但 2026-09-05 合并了 interceptor 状态隔离和 demo minSDK 拆分。这是「遗产路由库被新系统逼着修」而不是「路由技术复活」。
- **SoloPi v1.0.2**（蚂蚁）：无线自动化测试，8 月还在修 overlay 权限。对没有完善 UI 自动化的团队仍有 PoC 价值。
- **vlayout / Tangram / Atlas / AndFix**：archived 或死亡。不要用于新架构。

### Meituan / Kuaishou / Others

- **Logan 1.2.12、KOOM（2026-01 commit）**：两边都为 **16KB page size** 打过补丁。这是 Android 15+ 设备的硬门槛，不是特性。
- **Walle / Robust / Shield**：渠道包和热修复一代，已不活跃。
- 华为 / 百度 / 小米 / 京东 / 网易 / B 站 / 携程：本次没有扫到「持续维护 + 可迁入大型 Android 工程」的新开源。小米 MACE 已被 MNN / LiteRT 时代甩开；ijkplayer / CRN 只作历史参考。

## 3. International Big Tech

### Google

- **ADK Kotlin 1.0.0 / 1.0.1**：KMP 核心 + Android 扩展。1.0 对齐 ADK Core 的多 Agent 编排；Android 上可纯端侧（LiteRT-LM 支持 tool calling；ML Kit Gemini Nano 仍是 beta、尚不支持 tool calling）、可走 Firebase AI，也可用 Room / AppSearch 做 session/memory。今天的 1.0.1 修了 `load_memory` 的 JSON 返回，并把「模型调用了未注册 tool」从直接结束 invocation 改成返回可用 tool 列表——这是上线后立刻会踩的坑。
- **android/skills v1.0.11**：官方 Agent Skills，7277★。覆盖 AGP 9、Navigation 3、edge-to-edge、XML→Compose、R8 分析。Android CLI 可 `android skills add --skill agp-9-upgrade`。
- **Now in Android**：Gradle 9.7.1 + AGP 9.3.2，开启 project isolation，并把 configuration-cache 问题策略设为 fail。这是 Google 自己的「现代 Android 工程该长什么样」。
- **KSP 2.3.12**（2026-09-09）：ADK、Kuikly、Dagger/Hilt 链路都绑在 KSP 上，版本需要跟着 Kotlin 2.4.x 走。

### JetBrains

- **Kotlin 2.4.20**（2026-09-07）：以 Analysis API / K2 IDE 修复为主，不是语言大版本。对 Android 的实质影响是：AGP 9 内置 Kotlin 之后，KGP 版本不再由业务随意钉死。
- **Compose Multiplatform 1.12.0**：桌面 Hot Reload 增加 **MCP Server**，Agent 可以实时操作正在跑的 Compose 应用。`NativeCanvas` / `NativePaint` 升到 ERROR。1.13.0-alpha01 changelog 已进仓库。
- **kotlin-agent-skills**：专门处理 KMP + AGP 9——`com.android.application` 不能再和 `kotlin.multiplatform` 同模块，必须拆 `androidApp` + `shared`（`com.android.kotlin.multiplatform.library`）。

### Slack / Cash App / Square

- **Circuit 0.38.0**：Compose 架构（Presenter + UDF + Screen）。**Breaking：`Screen`/`PopResult` 不再是 Parcelable。** 升级必须选 kotlinx-serialization saver、或改实现 `ParcelableScreen`、或 `CircuitSaver.NoOp`。不支持的值从静默丢弃改为失败。工程已用 AGP 9.3.2、compileSdk 37、Compose Runtime 1.11。
- **Foundry 0.36.0**：Slack 内部 Gradle + IntelliJ 工具链开源版。星标 478，但是它暴露了大厂 Android 仓库的真实版本地板。
- **Paparazzi 2.0.0-alpha05**：无设备截图测试。支持 `com.android.kotlin.multiplatform.library`、Gradle 9、JUnit 5 hooks；最近补了 Layoutlib 的 Agent guidance。2.0 仍是 alpha，PoC 可以，规模替换要等稳定版。
- **LeakCanary 3.0-alpha-9**：3.0 仍在 alpha，但已经在记 Agent 通信流量——内存工具也在接 Agent 工作流。
- **Store 5.1.0-beta01**（2026-09-08）：网络/磁盘/内存三级 Store，已迁到 Mobile Native Foundation。

### Airbnb / Uber / Meta / Others

- Mavericks 3.1.0、RIBs 0.16.6、NullAway 0.14.1、Fresco 3.7.0：都在维护，但不是本周主线。
- NullAway 0.14.x 的 `JSpecifyExperimental` 值得 Java/Kotlin 混编大仓关注。
- Flipper、AffectedModuleDetector 已 archived。调试看官方 Studio / Lynx DevTool / LeakCanary；增量 CI 不要再绑 Dropbox 那个插件。

## 4. New Projects

这里只列「第一次应该认真看」的项目，不是新仓库清单。

1. **google/adk-kotlin**（2026-05 建仓，昨天 1.0）  
   解决：在 Android 进程里用 Kotlin 写可测试、可持久化、可端云混合的 Agent，而不是把 Python ADK 包一层 JNI。  
   现在看的原因：1.0 GA + 官方博客（2026-09-09）+ 当天 1.0.1 补丁，窗口期就是这几周。

2. **android/skills**（2026-03 建仓，7277★）  
   解决：Agent 改 Android 工程时缺乏官方规程，乱升 AGP、乱迁 Navigation。  
   现在看的原因：Google 已经把它写进 AGP Upgrade Assistant 文档。

3. **Tencent-TDS/KuiklyUI-AI**（2026-04，126★）  
   解决：Kuikly / Kuikly Compose 的 AI 编码质量。  
   现在看的原因：和 Kuikly 2026 Roadmap、Google skills、JetBrains skills 是同一类基础设施。

4. **lynx-family/lynxtron**（30★）  
   解决：Lynx 上桌面（Electron）。  
   现在看的原因：只作为生态信号，不建议 App 团队 PoC。

## 5. Major Project Changes

| Company | Project | Change | Technical Meaning | Recommendation |
|---|---|---|---|---|
| Google | ADK Kotlin | 1.0.0 GA（09-07）+ 1.0.1（09-10） | Android 终于有官方、KMP、可端侧的 Agent 运行时；未知 tool 不再直接掐死会话 | 立刻做端侧/混合 Agent PoC，不要再自研编排层 |
| Google | android/skills | v1.0.11 | AGP 9 / Nav3 / R8 升级从「文档」变成可触发 Skill | 所有 AGP 8→9 迁移用官方 Skill，不要让 Agent 自由发挥 |
| Google | Now in Android | Gradle 9.7.1 + AGP 9.3.2 + project isolation | Google 样板已把 isolation / CC=fail 当默认 | 大仓对照自己的 convention plugin，排 isolation 阻塞点 |
| Tencent | KuiklyUI | 2.27.0 + KSP 页面注册 | Compose DSL 从 demo 走向编译期工程化 | 已有 KMP 跨端诉求的团队做嵌入式 View PoC |
| Tencent TDS | KuiklyUI-AI | Skills/Rules 持续补 Compose | 框架开始为 Agent 提供第一方编码约束 | 若评估 Kuikly，把 AI repo 和 SDK 一起接入 IDE |
| ByteDance | Lynx | 4.1.0 月更；Autolink Gradle plugin | 宿主接入 native 扩展的成本接近 RN autolink | 已有动态化/跨端预算的团队跟 4.1，不要停在 3.6 文档 |
| JetBrains | Kotlin | 2.4.20 | 编译器/IDE 修复，服务 AGP 9 内置 Kotlin | 跟 AGP 9.3 一起升，不要单独钉死旧 KGP |
| JetBrains | CMP | 1.12.0 增加 Hot Reload MCP | Agent 能操作运行中的 Compose UI | 桌面/KMP 工具链团队评估；纯 Android App 可观察 |
| Slack | Circuit | 0.38.0 去掉 Screen Parcelable | Compose 导航状态持久化改成可插拔 CircuitSaver，KMP 友好 | 已用 Circuit 必须排期升级；新项目按 serialization saver 起步 |
| Slack | Foundry | 0.36.0 版本地板 | 生产 Android 仓库的 AGP/Gradle/Kotlin 真实水位 | 不要抄整套，抄版本矩阵和 convention 分层 |
| Cash App | Paparazzi | 2.0.0-alpha05 + Agent guidance | 截图测试对齐 AGP 9 / KMP library；测试工具开始服务 Agent | 新模块 PoC；全量替换等 2.0 稳定 |
| MNF | Store | 5.1.0-beta01 | 仓库层 API 仍在演进 | 新数据层可以看；稳定版再替换现有 Repository |
| Alibaba | MNN | 3.6.1 + 持续 OpenCL 修复 | 国内端侧 LLM 推理仍在高强度维护 | 端侧模型推理 PoC；和 ADK/LiteRT 做对比，不要两套都上 |
| Alibaba | ARouter | interceptor 重初始化修复 | 遗产路由库被新 SDK/进程模型逼着修 | 已接入则合入修复；新项目不要新选 ARouter |
| Kuaishou / Meituan | KOOM / Logan | 16KB page size | Android 15+ 兼容是维护义务 | 自研 native so 按同样清单过一遍 |
| ByteDance | btrace | 3.1.0 Harmony | 性能工具开始覆盖鸿蒙 | Android 性能问题优先于鸿蒙；有双端再接入 |

## 6. Watchlist Diff

### Added

国内 P0–P1：KuiklyUI、KuiklyUI-AI、Lynx 及 primjs/devtool/stack、MMKV、libpag、Hippy、WCDB、MNN、ARouter、btrace、CodeLocator、SoloPi、KOOM。  
海外 P0–P1：ADK Kotlin、android/skills、Kotlin、CMP、kotlin-agent-skills、KSP、Now in Android、gradle-recipes、Dagger、Circuit、Foundry、Paparazzi、LeakCanary、OkHttp、NullAway、Store。  
另收入一批 P2/P3 遗产项目，只为下一轮判断 Inactive，不在报告里展开。

### Updated

无。本次为基线。

### Deprecated / Inactive

Archived：alibaba/vlayout、alibaba/Tangram-Android、bytedance/ByteX、bytedance/AlphaPlayer、facebook/flipper、dropbox/AffectedModuleDetector。  
实质停更：Tencent/matrix、Tencent/QMUI_Android、alibaba/AndFix、alibaba/atlas、Meituan Walle/Robust/Shield、ctripcorp/CRN、bilibili/ijkplayer、XiaoMi/mace。

## 7. Industry Trend

同时出现、且来自不同大厂的同构信号，才升级为趋势。

### 趋势 A：Android 工程正在变成「SDK + Agent Skill + MCP」

Google（ADK Kotlin、android/skills、AGP Upgrade Assistant 文档） + JetBrains（kotlin-agent-skills、CMP Hot Reload MCP） + Tencent（Kuikly Roadmap MCP/Skills、KuiklyUI-AI） + ByteDance（Lynx 2026「AI-ready / Agent Skills」） + Cash App（Paparazzi Layoutlib agent guidance） + Square（LeakCanary agent traffic）。

> 这可能代表 Android 工程领域正在形成行业趋势。

含义：2026 下半年评估一个框架，要同时看三件事——API 稳不稳、有没有第一方 Skill、能不能被 Agent 安全地改。只看 GitHub Stars 会漏掉 ADK / KuiklyUI-AI / Foundry。

### 趋势 B：Compose Architecture + KMP 库插件成为默认结构

Google Now in Android + JetBrains CMP + Slack Circuit + Tencent Kuikly Compose DSL + Cash App Paparazzi（KMP Android library plugin）。

AGP 9 强制：App 模块用内置 Kotlin，KMP 模块用 `com.android.kotlin.multiplatform.library`，禁止 `kotlin-multiplatform` 和 `com.android.application` 同模块。这不是风格之争，是构建系统硬约束。

> 这可能代表 Android 工程领域正在形成行业趋势。

### 趋势 C：跨端叙事从「RN 替代」变成「原生嵌入 + 鸿蒙/16KB 必选」

Lynx Autolink、Kuikly 以 View 粒度嵌进 RecyclerView、Hippy 继续修列表复用、MMKV/btrace/Logan/KOOM 全员补 Harmony 或 16KB。动态化和性能工具如果还不支持 16KB，会在新设备上直接崩。

### 明确不是趋势

热修复、插件化、自研渠道包工具没有第二家在加码。国内大厂把精力从 Tinker/Shadow/Atlas 挪到了跨端框架和端侧 AI。

## 8. Recommended Projects

只推荐现在值得投入人天的。每个都回答四个问题。

### 1) google/adk-kotlin — 立刻 PoC

- **解决什么真实问题？** 商业 Android 应用要把 Agent 做进进程：工具调用、session、端侧隐私、云端复杂推理，而不是在 App 里嵌一个 WebView Chat。
- **为什么现在值得关注？** 1.0 刚 GA，1.0.1 已经在修生产容错。再等一个季度，内部自研编排会和官方 API 重复。
- **能否迁移到大型商业 Android 项目？** 能。KSP 进现有 Gradle 模块即可；先不要上 ML Kit beta 的 tool calling。用 LiteRT-LM 或 Firebase AI 二选一做混合。
- **是否值得 PoC？** 值得。两周目标：一个带 `@Tool` 的端侧 Agent + Room session + 一个业务只读工具（搜订单/查库存）。不要一上来做多 Agent。

### 2) android/skills + Kotlin/kotlin-agent-skills — 立刻接入 IDE，不做业务 PoC

- **解决什么真实问题？** Agent 升 AGP 9、拆 KMP 模块、迁 Navigation 3 时会编出不可编译的工程。
- **为什么现在值得关注？** Google / JetBrains 已经把 Skill 写进官方升级文档；Now in Android 已在 9.3.2。
- **能否迁移？** 能。这是给 Agent 用的说明书，不进 APK。
- **是否值得 PoC？** 不必 PoC，直接装。让 Agent 跑一遍 AGP 8→9 的只读评估即可。

### 3) slackhq/circuit — 新模块 / 新 App 值得 PoC；老架构谨慎

- **解决什么真实问题？** Compose 页面状态、导航回退、进程死亡恢复、Presenter 测试，一直缺一个比「单 Activity + 手写 ViewModel」更完整、又比 RIBs 更轻的架子。
- **为什么现在值得关注？** 0.38 去掉 Parcelable 超类型，KMP 导航状态终于不再绑 Android。Slack 自己已经在 AGP 9.3 上跑。
- **能否迁移到大型商业 Android 项目？** 能渐进：单业务模块接入，不必替换整个导航。0.38 是 breaking，老 Circuit 用户必须排升级，不能无脑跟版本。
- **是否值得 PoC？** 值得。做一个带返回栈 + serialization saver 的中等复杂流程（登录后多步表单）。已经在用 Mavericks/RIBs 且稳定的大仓，不必为了跟风而换。

### 4) Tencent-TDS/KuiklyUI — 有跨端 KPI 再 PoC

- **解决什么真实问题？** 同一套 Kotlin 业务 UI 要上 Android / iOS / 鸿蒙，并且要动态下发，团队主语言已经是 Kotlin。
- **为什么现在值得关注？** 周更、Compose DSL + KSP、官方 AI Skills、View 级嵌入 RecyclerView 已经有 sample。
- **能否迁移到大型商业 Android 项目？** 可以嵌入，不适合一夜替换整个 App。包体 AOT Android ~300KB 量级友好，但动态化和鸿蒙工具链要单独评估。
- **是否值得 PoC？** 若公司已经在评估鸿蒙 + Android 双端，值得做一个瀑布流卡片嵌入。纯 Android 团队优先 Compose，不要为了框架而框架。

### 5) lynx-family/lynx — 有前端人力的动态化团队 PoC

- **解决什么真实问题？** 用 React/CSS 心智在宿主 App 里渲染原生 UI，要启动和滚动性能，而不是再养一套 RN 定制。
- **为什么现在值得关注？** 4.1 月更兑现；Autolink 降低原生扩展成本；TikTok 自己在用。
- **能否迁移？** 能作为 LynxView 嵌入，不是整包重写。要接受 C++ 引擎、独立工具链、869+ 未关 issue 的现实。
- **是否值得 PoC？** 已有 Web/RN 团队且不满 RN 性能时值得。纯 Kotlin 团队优先 Kuikly 或 Compose。

### 6) cashapp/paparazzi — 测试基建 PoC，不要全量

- **解决什么真实问题？** Compose/XML 截图测试不依赖设备农场。
- **为什么现在值得关注？** 2.0 alpha 开始吃 AGP 9 和 KMP Android library；官方在补 Agent 文档。
- **能否迁移？** 能进 library 模块。2.0 仍是 alpha，主 App 模块先不要押宝。
- **是否值得 PoC？** 值得在一个 Compose 组件库模块跑 20 张截图，验证 CI 和 isolation。

### 7) alibaba/MNN — 端侧模型团队对比 PoC

- **解决什么真实问题？** 端侧 LLM / CV 推理要小、快、阿里内部验证过。
- **为什么现在值得关注？** 持续高强度修 OpenCL，定位已转向 on-device LLM。
- **能否迁移？** 能，但是和 Google LiteRT-LM / ADK 选一条主线，不要双运行时。
- **是否值得 PoC？** 已有端侧模型文件时值得做延迟/内存对比。没有模型资产则先看 ADK。

### 明确不推荐现在投入

- 新选 ARouter / Tinker / Shadow / Atlas / ByteX。
- Flipper、AffectedModuleDetector。
- BlockFramework、lynxtron：继续观察，不进业务排期。

## 9. Sources

- GitHub API（2026-09-10）：各仓库 metadata / latest release / HEAD commit
- [Lynx Roadmap 2026](https://lynxjs.org/next/blog/lynx-open-source-roadmap-2026)
- [Lynx Autolink](https://lynxjs.org/3.8/guide/autolink.html)
- [Kuikly Roadmap 2026](https://kuikly.tds.qq.com/Blog/roadmap2026.html)
- [KuiklyUI 2.27.0](https://github.com/Tencent-TDS/KuiklyUI/releases/tag/2.27.0)
- [ADK for Kotlin 1.0 announcement](https://developers.googleblog.com/en/announcing-adk-for-kotlin-10-building-production-ready-ai-agents-in-kotlin-android-and-beyond/)
- [google/adk-kotlin](https://github.com/google/adk-kotlin)
- [android/skills](https://github.com/android/skills)
- [Kotlin/kotlin-agent-skills AGP 9 migration](https://github.com/Kotlin/kotlin-agent-skills/blob/main/skills/kotlin-tooling-agp9-migration/SKILL.md)
- [AGP 9.0.1 release notes](https://developer.android.com/build/releases/agp-9-0-0-release-notes)
- [Update Kotlin projects for AGP 9](https://blog.jetbrains.com/kotlin/2026/01/update-your-projects-for-agp9/)
- [Android CLI and skills](https://android-developers.googleblog.com/2026/04/build-android-apps-3x-faster-using-any-agent.html)
- [Circuit 0.38.0 / changelog](https://slackhq.github.io/circuit/changelog/)
- [Compose Multiplatform 1.12.0](https://github.com/JetBrains/compose-multiplatform/releases/tag/v1.12.0)
- [Paparazzi 2.0.0-alpha05](https://github.com/cashapp/paparazzi/releases/tag/2.0.0-alpha05)
- [Now in Android #2139 project isolation](https://github.com/android/nowinandroid/pull/2139)
- [MMKV v2.4.2](https://github.com/Tencent/MMKV/releases/tag/v2.4.2)
- [btrace v3.1.0](https://github.com/bytedance/btrace/releases/tag/v3.1.0)
