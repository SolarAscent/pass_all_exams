<p align="right">
  <a href="./README.md">EN</a> | <strong>简体中文</strong>
</p>

<p align="center">
  <img src="docs/hero.svg" alt="Pass All Exams" width="760"/>
</p>

<p align="center">
  <strong>面向 Codex、OpenClaw、OpenCode 的证据化考试复习 Skill。</strong>
</p>

<p align="center">
  把课堂笔记、考纲、往年题、老师重点和零散知识点，变成一个更省 token 的复习闭环：
  拆考点、讲一小点、马上检索、修错、安排复盘。
</p>

<p align="center">
  <a href="https://github.com/SolarAscent/pass_all_exams/releases/tag/v0.1.0"><img src="https://img.shields.io/github/v/release/SolarAscent/pass_all_exams?style=flat-square&label=release&labelColor=111827&color=2563EB" alt="Latest release"/></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-16A34A?style=flat-square&labelColor=111827" alt="MIT license"/></a>
  <img src="https://img.shields.io/badge/Codex-supported-2563EB?style=flat-square&labelColor=111827" alt="Codex supported"/>
  <img src="https://img.shields.io/badge/OpenClaw-supported-0F766E?style=flat-square&labelColor=111827" alt="OpenClaw supported"/>
  <img src="https://img.shields.io/badge/OpenCode-supported-9333EA?style=flat-square&labelColor=111827" alt="OpenCode supported"/>
  <img src="https://img.shields.io/badge/token%20mode-compact-F59E0B?style=flat-square&labelColor=111827" alt="Compact token mode"/>
</p>

<br/>

## 这个项目做什么

Pass All Exams 不是让 AI 一次性生成一大坨复习资料，而是把复习压成学生考前真正需要的循环：

```text
一门课 -> 一个高价值考点 -> 一次短讲解 -> 一道检索题 -> 一次修错或复盘卡
```

它保留了 `cram-engine` 里很有价值的部分：分阶段复习、控制认知负荷、主动回忆、错题补漏。然后在此基础上增加了资料依据标注、机器可读进度、间隔复习卡、理工/编程/语言类课程适配，以及更省 token 的默认流程。

## 为什么不一样

| 普通 AI 复习的问题 | Pass All Exams 的做法 |
|---|---|
| 生成长笔记，但不检查你会不会。 | 每讲一个点，都跟一个检索练习。 |
| 考点预测容易像老师确认过一样。 | 明确区分 `资料依据`、`合理推断`、`待确认`。 |
| 聊天历史越来越贵，越复习越费 token。 | 进度写入 `state.json`、`errors.jsonl`、`cards.jsonl`。 |
| 只适合文科定性课。 | 增加定量题、编程题、语言题和记忆密集型课程模式。 |
| 错了以后只是原话再讲一遍。 | 先诊断错误类型，再换一种表示方式重讲并重测。 |

## 安装

按你使用的智能体选择安装方式。GitHub 仓库名是 `pass_all_exams`，安装后的 skill 名是 `pass-all-exams`。

### 方式一：从 Git 安装

```bash
git clone https://github.com/SolarAscent/pass_all_exams.git
cd pass_all_exams
```

然后选择你的智能体：

| 智能体 | 命令 |
|---|---|
| Codex | `bash scripts/install.sh codex` |
| OpenClaw | `bash scripts/install.sh openclaw` |
| OpenCode，全局 | `bash scripts/install.sh opencode` |
| OpenCode，仅当前项目 | `bash scripts/install.sh opencode-project` |

### 方式二：手动克隆到指定目录

```bash
# Codex
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.codex/skills/pass-all-exams

# Codex，使用 CODEX_HOME 时
git clone https://github.com/SolarAscent/pass_all_exams.git "$CODEX_HOME/skills/pass-all-exams"

# OpenClaw
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.openclaw/skills/pass-all-exams

# OpenCode 全局
git clone https://github.com/SolarAscent/pass_all_exams.git ~/.config/opencode/skill/pass-all-exams

# OpenCode 当前项目
git clone https://github.com/SolarAscent/pass_all_exams.git .opencode/skill/pass-all-exams
```

### 方式三：下载 `.skill` 包

下载 release 附件：

```text
https://github.com/SolarAscent/pass_all_exams/releases/download/v0.1.0/pass-all-exams.skill
```

适合支持上传 skill 压缩包的客户端或网页 UI。

## 快速开始

安装后直接说：

```text
/exam 组织行为学 start
```

或者把信息一次性说清楚：

```text
帮我用 pass-all-exams 复习组织行为学。
考试题型是选择题、简答题和案例分析。
老师强调必考：霍桑实验、期望理论。我会继续粘贴课堂笔记。
```

英文课程也可以：

```text
Use pass-all-exams to help me review Organizational Behavior.
The exam has multiple choice, short answer, and case analysis.
My must-know topics are Hawthorne studies and expectancy theory.
```

## 复习流程

```text
建档
  收集课程、考试日期、题型、资料、必考点

拆解
  把资料拆成可考试的小知识点，并标注来源可信度

讲授
  一次只讲一个点：具体例子开头，最多三块，再让你自己总结

检题
  按真实题型出题：选择、案例、计算、代码 trace、简答等

补漏
  判断错因，换讲法，从新角度重测

复盘
  生成当天、次日、三天后、考前一天的检索卡
```

## 证据约束

每次讲解、押题或批改时，都应该把来源状态说清楚：

```text
资料依据:
- 直接来自你的笔记、考纲、老师原话、往年题或粘贴资料。

合理推断:
- 基于通用课程知识、常见考试方式做出的复习推断。

待确认:
- 需要你再看老师要求、教材版本或本校考试范围的内容。
```

如果你没有提供任何资料，它会按通用知识帮你复习，但不能假装知道你老师到底考什么。

## 命令

| 命令 | 作用 |
|---|---|
| `/exam <课程> start` | 创建或刷新课程复习计划。 |
| `/cram <课程> start` | 兼容 cram-style 使用习惯。 |
| `/exam <课程> resume` | 从保存进度继续。 |
| `/exam <课程> drill` | 根据薄弱点和到期复习卡出题。 |
| `/exam <课程> retry <知识点>` | 对某个薄弱点重讲、重测并更新记录。 |
| `/exam <课程> summary` | 输出考前清单。 |

## 本地状态

课程数据默认保存在本地：

```text
~/.pass-all-exams/courses/<course-slug>/
```

主要文件：

| 文件 | 作用 |
|---|---|
| `course.yaml` | 课程配置：题型、资料、必考点、偏好。 |
| `state.json` | 当前阶段和知识点状态。 |
| `errors.jsonl` | 错题和诊断历史。 |
| `cards.jsonl` | 检索复习卡和到期日期。 |
| `sessions.jsonl` | 可选会话日志。 |

常用脚本：

```bash
python3 scripts/examctl.py init --course "组织行为学"
python3 scripts/examctl.py status --course "组织行为学"
python3 scripts/examctl.py summary --course "组织行为学"
```

记录一个知识点和一次错题：

```bash
python3 scripts/examctl.py record-point \
  --course "组织行为学" \
  --point "期望理论" \
  --level must \
  --status taught \
  --source material

python3 scripts/examctl.py record-error \
  --course "组织行为学" \
  --point "期望理论" \
  --reason confusion \
  --question-type "选择题" \
  --must-know
```

## Token 模式

| 模式 | 适合场景 | 行为 |
|---|---|---|
| `compact` | 大多数考前突击 | 一个点、一个例子、一题检索、一次纠错。 |
| `standard` | 正常周复习 | 多一个例子，并关联一个已学知识点。 |
| `deep` | 难课或高风险考试 | 增加推导、边界条件和混合练习。 |

默认是 `compact`。详细阶段规则放在 `references/`，需要时才加载，避免每次都把长提示塞进上下文。

## 适合哪些课

| 课程类型 | 示例 | 特别处理 |
|---|---|---|
| 文史社科 | 法学、政治学、社会学、教育学 | 定义、比较、案例分析踩分框架 |
| 经管类 | 组织行为学、市场营销、会计理论 | 框架、陷阱、场景应用 |
| 定量课 | 高数、统计、经济学方法 | 公式条件、例题、计算错误诊断 |
| 编程课 | 数据结构、数据库、操作系统、Python/C/Java | 代码 trace、bug 修复、复杂度解释 |
| 语言和记忆密集课 | 英语、历史、医学基础 | 填空、回忆卡、对比表 |

## 打包与验证

生成可上传的 `.skill` 包：

```bash
python3 scripts/package_skill.py
```

验证 skill 结构：

```bash
python3 scripts/validate_skill.py
python3 -m py_compile scripts/examctl.py scripts/validate_skill.py scripts/package_skill.py
```

## 仓库结构

```text
pass_all_exams/
├── SKILL.md                    # 智能体读取的入口
├── agents/openai.yaml          # Codex UI 元数据
├── configs/example.yaml        # 示例课程配置
├── references/
│   ├── pipeline.md             # 详细复习流程
│   ├── prompt-patterns.md      # 可复用提示模板
│   ├── platforms.md            # Codex/OpenClaw/OpenCode 安装说明
│   └── comparison.md           # 设计对比说明
├── scripts/
│   ├── examctl.py              # 本地进度管理
│   ├── install.sh              # 跨平台安装脚本
│   ├── package_skill.py        # .skill 打包脚本
│   └── validate_skill.py       # 结构校验脚本
└── docs/hero.svg
```

## 隐私

默认所有课程数据都存在本机。这个 skill 不需要外部服务、数据库或账号。你的笔记、错题、复习卡会保存在 `~/.pass-all-exams/`，除非你主动移动或分享。

## 致谢

本项目借鉴了 [cram-engine](https://github.com/liuliu667/cram-engine) 的分阶段学习逻辑、[token-monitor](https://github.com/Javis603/token-monitor) 的 README 呈现方式，以及 [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) 的清晰安装与快速开始结构。

## License

[MIT](LICENSE)
