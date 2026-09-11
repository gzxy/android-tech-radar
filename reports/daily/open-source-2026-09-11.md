# Android Open Source Daily Report

Date: 2026-09-11
Run type: incremental vs `snapshots/open-source/2026-09-10.md`

## 1. Executive Summary

昨天基线刚立完，今天没有新的大版本号。真正值得改排期的是三件事：

1. **Google 把「App 当成端上 MCP Server」写成了官方路径。** `android/appfunctions`（189★，2026-05 建仓，基线漏收）是官方样品 + Testing Agent。文档 2026-09-08 更新：AppFunctions = MCP tool 的 Android 等价物，Android 16+，Jetpack `1.0.0-alpha10`。`android/skills` 里已经有 `device-ai/appfunctions` skill。Gemini 对接仍是 private preview / EAP——但暴露函数、写 KDoc、用 ADB 自测可以现在做。
2. **ADK Kotlin 1.0.1 之后立刻在修生产容错，但还没打 1.0.2。** main 新增：MCP server 拒绝请求时保活当前 turn；`Plugin.onRunError` 对齐 Python/Java。昨天报告的 unknown-tool 修复也落到 main。接了 MCP Toolset 的 PoC 不要停在 1.0.1 的心理预期上，盯下一包。
3. **Dagger 正式改口：KSP 已稳定。** 不是新 release（仍是 2.60.1），是开发者指南 + CI：Dagger 2.60+ / KSP 2.3.9+ 起 KSP 为稳定路径。叠加昨天的 KSP 2.3.12，kapt→KSP 不再是「等等看」。

同步信号：Slack Circuit 当天跟上官方 Compose 1.12.1 和 Benchmark 1.5.0；Paparazzi 修了 Compose `HideFromAccessibility` 截图污染；MNN 去掉工具链硬编码 STS / 遥测，并补了 Qwen3-TTS 端侧 decode。  
华为 / 百度 / 网易 / 京东再扫一轮，仍没有可迁入大型 Android 工程的新开源。

Kuikly Compose DSL 正式发版、Lynx 4.2：都还没到。不要把 develop 上的 TransferView / 回滚当成发版。

## 2. Domestic Big Tech

### Tencent

- **KuiklyUI 仍是 2.27.0。** HEAD 只是 OHOS 拷贝目录和 CDN 地址。Compose DSL + KSP 页面注册没有新的正式发版。Roadmap 上的 MCP Server 也还没从 KuiklyUI-AI（8 月 10 日后无提交）变成可调用的服务。
- **新观察：`Tencent-TDS/dsh-kuikly-expert`（13★）。** 2026-08 一次性提交，把四条 Kuikly skill 打成 DeepSeek Harness 插件。星标极低，但说明腾讯 TDS 在同时喂 Cursor/官方 Skills 和 DeepSeek 两套 Agent。只观察，不排期。
- **libpag / Hippy / MMKV：** 无版本变化。libpag 修了 PAGX 导出滤镜丢失，不影响 Android 宿主接入。

### ByteDance / Lynx Family

- **Lynx 仍是 4.1.0。** develop 上出现 Android `TransferView` 所有权/生命周期 API（宿主之间挪 LynxView），随后同一夜回滚了 DevTool CDPResponder 和 iOS 异步 UI。含义：嵌入式宿主 API 在长，但 **不要追 develop HEAD**，等 4.2（路线图 2026-10）。
- **新观察：`lynx-family/animax`（30★，1.1.0）。** Lynx 自己的 C++ Lottie / Alpha Video 引擎，本周还在修 Harmony 同步编解码和 iOS Metal 帧。低星、持续维护、解决「跨端动画不要再绑一份 JS Lottie」。对已经上 Lynx 的团队有意义；纯 Compose 团队继续用 Lottie Android / libpag。
- btrace / CodeLocator / BlockFramework：无新版本。

### Alibaba / Ant

- **MNN 3.6.1 未发版，但 main 有两类高信号提交。**  
  安全：去掉工具链硬编码 STS、关闭遥测——用官方转换/调优脚本的团队应跟 main。  
  能力：Qwen3-TTS talker / code-predictor 的 KV-cache decode，并修乱码。端侧语音开始进同一推理栈。
- ARouter / SoloPi：无新变化。昨天的 interceptor 修复仍是遗产续命，不是路由方向复活。

### Meituan / Kuaishou / Others

- Logan / KOOM / 一代热修复：无复活。
- 华为 HMS-Core 仍是 Scan / IAP / Video Editor demo。百度开源主线在 Kunlun / OCR / 云端 Agent。网易 `NetEase/skills` 是通用 agent skills，2026-03 后无推送。京东 JoyAI / OxyGent / Taro 不是 Android 工程仓库。小米 MACE 继续被 MNN 甩开。

## 3. International Big Tech

### Google

- **ADK Kotlin：版本号还是 1.0.1，行为已经往前走了。** 1.0.1 发布时间是 09-10 09:25Z。之后 main 合入：  
  - MCP server 拒请求 → 不再结束整轮；  
  - `Plugin.onRunError`（只通知，再重新抛）；  
  - unknown-tool 修复从 tag 回到 main。  
  没有 Android samples 新仓。PoC 继续用 1.0.1，把 MCP 失败路径写成必测项，1.0.2 出来再升。
- **AppFunctions 样品仓首次入库。** ChatApp（Compose + Hilt，手机 + Wear）展示发消息 / 搜联系人 / 打电话；另有特权 Testing Agent（手动 + LLM）。样品 main 停在 2026-08-19 的 26Q4 allowlist 脚本，不是本周新功能，但是官方「怎么把 App 注册成系统 Agent 工具」的唯一完整参考。
- **android/skills：** 无新 tag。确认已包含 AppFunctions 四段生命周期 skill（发现功能 → 生成实现 → 优化 KDoc → ADB 调试）。
- **Dagger：** 文档宣布 KSP 稳定（2.60+ / KSP 2.3.9+），CI 矩阵升到 KSP 2.3.11。Hilt 现网若还钉 kapt，迁移理由已经足够。
- Now in Android / KSP：无新 commit / 无 2.3.13。

### JetBrains

- Kotlin 2.4.20、CMP 1.12.0 无新 tag。HEAD 分别是 Wasm 测试和 Web 资源解码让出帧，与 Android 宿主无关。
- kotlin-agent-skills 仍停在 2026-07-21。

### Slack / Cash App / Square

- **Circuit 0.38.0 未发版，但工程已吃下官方 09-09 工具链：** Compose 1.12.1、Benchmark 1.5.0。这是「大厂样板会在 24 小时内跟上官方补丁」的证据，不是又一次 Circuit breaking。
- **compose-lints 1.6.0 补入 Watchlist。** Slack 自己的 Compose lint，最近在加强 modifier / slot 复用的控制流分析，Lint 已到 32.4.0。比再抄一套自定义 Compose Detekt 便宜。
- **Paparazzi：** 无 2.0 新 alpha。main 修了两件测试正确性：  
  1. 过滤 `HideFromAccessibility`（不只是已废弃的 `InvisibleToUser`），避免 disabled+hidden 节点污染 a11y legend；  
  2. 删除库内 synthetic WindowInsets fixture——insets 回归归消费方。  
  已在跑 a11y 截图的模块，下一包可能看到更干净的 legend，不是业务 UI 变了。
- Foundry / LeakCanary / Store：无版本变化。

### Airbnb / Uber / Meta / Others

- NullAway 内部重构分析缓存，用户 API 不变。
- Fresco OSS 构建对齐 Kotlin 2.2，不是 3.8。
- Mavericks / RIBs / Lottie / Showkase：沉寂。

## 4. New Projects

只列第一次应该认真看的，不是新仓库清单。

1. **android/appfunctions**（2026-05，189★）  
   解决：让系统 Agent / Gemini 以类型安全的方式调用 App 内能力，而不是让模型「看屏幕点按钮」，也不是自己搭 MCP 进程。  
   现在看的原因：文档刚在 2026-09-08 把「Android MCP」写死；alpha10 已切到 `@AppFunctionServiceEntryPoint`；官方 Skill 齐了。Gemini 仍是 EAP，但注册与自测窗口就是现在。  
   迁移：能。`compileSdk 36+`，KSP compiler，注解进现有 Service 模块。先暴露 2–3 个只读/低风险写操作。  
   PoC：值得。不要和 ADK 进程内 Agent 做成同一个里程碑。

2. **slackhq/compose-lints**（1.6.0，513★）  
   解决：Compose 复用、稳定性、slot 误用这类「能编过但运行态掉帧 / 状态错」的问题。  
   现在看的原因：基线漏了；Slack 自己还在加 CFA。  
   迁移：能。Lint 依赖，不进 APK。  
   PoC：不必。直接接到现有 Lint / CI。

3. **Tencent-TDS/dsh-kuikly-expert / lynx-family/animax**  
   只作为生态信号入库。前者是 DeepSeek 侧的 Kuikly skill；后者是 Lynx 动画引擎。都不建议独立业务 PoC。

不入库：`alibaba/MobiZen-GUI`（桌面 VLM 控真机，3 月后停更，不是可嵌入 SDK）；`bytedance/DanceUI`（iOS）。

## 5. Major Project Changes

| Company | Project | Change | Technical Meaning | Recommendation |
|---|---|---|---|---|
| Google | AppFunctions samples | 首次入库；文档定义「端上 MCP」 | App 向系统 Agent 暴露工具，和进程内 ADK 是两条线 | 有助理/系统集成 KPI 的 App **立刻做只读函数 PoC**；等 EAP 再对 Gemini 联调 |
| Google | ADK Kotlin | 1.0.1 后 MCP reject 保活 + `onRunError` | 生产 Agent 的失败路径开始补齐，但未发 1.0.2 | PoC 继续；把 MCP 失败写成测试。**等 1.0.2 再升生产依赖** |
| Google | Dagger | 文档宣布 KSP 稳定（2.60+ / 2.3.9+） | kapt 退役窗口被官方盖章 | **Adopt KSP**：新模块禁止 kapt；旧模块按 Hilt/Dagger 分批 |
| Google | android/skills | 确认含 AppFunctions skill | Agent 可以按官方四步生成/测试 AppFunction | 做 AppFunctions 时装这个 skill，不要让模型自由写 manifest |
| Alibaba | MNN | 去 STS/遥测 + Qwen3-TTS decode | 工具链安全债 + 端侧语音进同一引擎 | 已用 MNN：**跟 main 换工具脚本**。TTS 另开对比 PoC，不要和 ADK 双运行时 |
| Cash App | Paparazzi | a11y hidden 过滤；去掉 synthetic insets | 截图测试更接近真实无障碍树；insets 回归下放 | 已上 2.0-alpha 的模块预期 legend 变干净；**不要在库里造 WindowInsets** |
| Slack | Circuit | Compose 1.12.1 / Benchmark 1.5.0 | 大厂样板 24h 内跟上官方补丁 | 已用 Circuit 的工程对齐这两包；**不是又一次 0.38 breaking** |
| Slack | compose-lints | 基线补入 1.6.0 | 生产级 Compose 静态检查 | 直接接 CI |
| ByteDance | Lynx | TransferView API（未发版）+ develop 回滚 | 嵌入式宿主 API 在长，主干不稳 | **钉 4.1.0**；4.2 前不要跟 develop |
| Tencent TDS | dsh-kuikly-expert | 新仓（13★） | Kuikly 开始服务 DeepSeek Harness | 观察。评估 Kuikly 时和 KuiklyUI-AI 一起看 |
| ByteDance | AnimaX | 新仓（30★） | Lynx 自研 Lottie/Alpha 引擎 | 已上 Lynx 再看；纯 Android 继续 Lottie/libpag |

## 6. Watchlist Diff

### Added

- `android/appfunctions`（P0）
- `slackhq/compose-lints`（P1）
- `Tencent-TDS/dsh-kuikly-expert`（P2）
- `lynx-family/animax`（P2）

### Updated

P0/P1 元数据已按 2026-09-11 GitHub API 回写（star / HEAD / 日期）。有技术含义的更新只有：ADK main 超前 1.0.1、MNN 安全/TTS、Paparazzi a11y、Dagger KSP 文档、Circuit 工具链、Lynx TransferView。其余是计数和普通 commit。

### Deprecated / Inactive

无新增 archived。华为 / 百度 / 网易 / 京东继续空窗，不强制填表。

## 7. Industry Trend

昨天已经点名的趋势，今天只在证据变厚时升级，不重复当「新发现」。

### 趋势 A 证据加强：SDK + Skill + **端上 MCP（AppFunctions）**

Google 现在同时给三条官方轨道：

- **进程内 Agent：** `google/adk-kotlin`（自己跑模型、自己调 `@Tool` / MCP Toolset）
- **系统级 Tool：** AppFunctions（App 被 Gemini / 系统 Agent 调，官方称 MCP 移动等价物）
- **怎么写这两套：** `android/skills`（AGP 9 / Nav3 / R8 / AppFunctions）

叠加 JetBrains CMP Hot Reload MCP、腾讯 KuiklyUI-AI + DeepSeek Harness skill、字节 Lynx AI-ready roadmap。

> 这可能代表 Android 工程领域正在形成行业趋势。

2026 下半年评估「我们要不要做 App 内 AI」，先问清楚是 **App 里跑 Agent**，还是 **让系统 Agent 跑进 App**。两套 API、两套权限、两个 PoC。

### 趋势 B 继续：官方补丁被大厂样板 24h 吸收

昨天：Now in Android / Circuit / Foundry 已在 AGP 9.3。  
今天：Circuit 当天跟上 Compose 1.12.1 和 Benchmark 1.5.0；Dagger 宣布 KSP 稳定。

> 这可能代表 Android 工程领域正在形成行业趋势。

大仓如果还把「等一个季度再升补丁」当策略，会和样板工程的可复制性拉开差距——尤其是 Benchmark `requireAot` 和 KSP 2.3.x。

### 明确还不是趋势

- Kuikly Compose DSL 正式发版、Lynx 4.2：未到点。
- 热修复 / 插件化：继续沉寂。
- 国内 GUI Agent 开源（MobiZen-GUI）：研究仓，没有第二家 Android 工程落地。

## 8. Recommended Projects

只推荐现在值得投入人天的。每个都回答四个问题。

### 1) android/appfunctions — 立刻 PoC（和 ADK 拆开）

- **解决什么真实问题？** 用户对系统助理说「查一下我的订单 / 创建一个提醒」，助理需要调用**你 App 里已经存在的业务**，而不是再做一个聊天 WebView，也不是把整棵 UI 交给截图 Agent。
- **为什么现在值得关注？** 平台 API + Jetpack alpha10 + 官方 Skill + 样品仓齐了；Gemini 还没 GA，所以现在做的是「函数注册和契约」，不是「等联调再设计 API」。
- **能否迁移到大型商业 Android 项目？** 能。独立 `:appfunctions` 模块，`compileSdk 36`，KSP，先只读。权限模型是系统 `EXECUTE_APP_FUNCTIONS`，不是普通互调。
- **是否值得 PoC？** 值得。一周目标：2 个 `@AppFunction`（搜索 + 创建草稿）+ `adb shell cmd app_function` 自测 + 官方 skill 走一遍 KDoc。不要承诺「下个版本就能被 Gemini 调到」。

### 2) google/adk-kotlin — 继续昨天的 PoC，不要为今天的 main 重写

- **解决什么真实问题？** App 进程里要有可测试、可持久化、可端云混合的 Agent。
- **为什么现在值得关注？** 1.0.1 之后的 MCP / Plugin 失败路径说明 Google 在按生产标准补，1.0.2 会很快。
- **能否迁移？** 能。KSP `@Tool` 进现有模块。
- **是否值得 PoC？** 值得，但 **今天不要为 unreleased main 改 API**。把 MCP 拒绝和未知 tool 写成测试夹具，等 1.0.2。

### 3) android/skills（含 AppFunctions skill）+ Dagger KSP — 立刻接入，不做业务 PoC

- **解决什么真实问题？** Agent 升 AGP / 写 AppFunction / 迁 Hilt-KSP 时会编出不能跑的工程。
- **为什么现在值得关注？** AppFunctions skill 已在仓里；Dagger 今天把 KSP 标成稳定。
- **能否迁移？** 能。不进 APK。
- **是否值得 PoC？** 不必。装 skill；开一个 Hilt 模块的 kapt→KSP 迁移 PR。

### 4) slackhq/compose-lints — 直接进 CI

- **解决什么真实问题？** Compose 稳定性 / slot / modifier 误用，单元测试抓不到。
- **为什么现在值得关注？** Slack 生产在用，1.6.0 且还在加分析。
- **能否迁移？** 能。Lint 配置。
- **是否值得 PoC？** 不必。接上，看一周噪音再调 baseline。

### 5) 昨天仍成立、今天没有被否定的推荐

- **Circuit：** 新模块 PoC 仍值得；0.38 Parcelable breaking 没有撤回。
- **KuiklyUI / Lynx：** 有跨端 KPI 再 PoC。今天没有新发版来改变「嵌入、不要整包替换」。
- **Paparazzi：** 继续组件库模块 PoC。今天的 a11y 修复降低误报，不是 2.0 稳定的信号。
- **MNN：** 已有端侧模型再对比。新出现的 TTS 路径可以加一项延迟测试，仍不要和 LiteRT/ADK 双栈。

### 明确不推荐现在投入

- 追 Lynx develop、为 TransferView 改宿主。
- 新选 ARouter / Tinker / Shadow / Atlas / ByteX。
- MobiZen-GUI、dsh-kuikly-expert、animax 独立业务排期。
- 把 AppFunctions 和 ADK 揉成一个「大 AI 项目」。

## 9. Sources

- GitHub API（2026-09-11）：watchlist 仓库 metadata / latest release / HEAD commit
- [android/appfunctions](https://github.com/android/appfunctions)
- [Overview of AppFunctions](https://developer.android.com/ai/appfunctions)（Last updated 2026-09-08）
- [Add the AppFunctions API](https://developer.android.com/ai/appfunctions/add-appfunctions)
- [Jetpack appfunctions 1.0.0-alpha10](https://developer.android.com/jetpack/androidx/releases/appfunctions)
- [android/skills device-ai/appfunctions](https://github.com/android/skills/tree/main/device-ai/appfunctions)
- [google/adk-kotlin](https://github.com/google/adk-kotlin)（`245a74a2b3` MCP reject；`77aea89604` onRunError；`93c4beb889` unknown tool）
- [google/dagger `099c3c8f40`](https://github.com/google/dagger/commit/099c3c8f40) KSP stable docs
- [cashapp/paparazzi #2430](https://github.com/cashapp/paparazzi/pull/2430) HideFromAccessibility
- [cashapp/paparazzi #2431](https://github.com/cashapp/paparazzi/pull/2431) remove synthetic WindowInsets
- [slackhq/circuit](https://github.com/slackhq/circuit) Compose 1.12.1 / Benchmark 1.5.0
- [slackhq/compose-lints 1.6.0](https://github.com/slackhq/compose-lints/releases/tag/1.6.0)
- [alibaba/MNN](https://github.com/alibaba/MNN) STS/telemetry + Qwen3-TTS
- [lynx-family/lynx TransferView](https://github.com/lynx-family/lynx/commit/2765273c2e)
- [Tencent-TDS/dsh-kuikly-expert](https://github.com/Tencent-TDS/dsh-kuikly-expert)
- [lynx-family/animax](https://github.com/lynx-family/animax)
- [Lynx Roadmap 2026](https://lynxjs.org/next/blog/lynx-open-source-roadmap-2026)
