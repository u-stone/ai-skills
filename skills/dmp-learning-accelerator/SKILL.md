---
name: dmp-learning-accelerator
version: 1.0.0
description: >
  Deep Mastery Protocol (DMP) — 编程领域学习型项目的快速启动方法论。
  适用于任何需要系统性掌握某一编程领域（图形学、网络、编译器、ML等）的学习项目。
  将 PBL、费曼学习法、敏捷开发与长期记忆工程融合为一套可执行的 AI 协作协议。
triggers:
  - "启动学习项目"
  - "new learning project"
  - "开始学习"
  - "bootstrap DMP"
  - "dmp init"
  - "学习型项目"
---

# Deep Mastery Protocol (DMP) — Learning Accelerator

> **核心目标**：将学习过程工程化，将隐性知识显性化，实现极速认知迭代。

---

## 🧠 四大认知支柱

| 支柱 | 原则 | 执行方式 |
|------|------|----------|
| **Bloom's Taxonomy** | 不止于应用，追求分析、评价、创造 | KnowledgeBase 写至分析层级 |
| **Pareto 80/20** | 聚焦 20% 的核心高价值知识 | Roadmap 用 `[CORE]` 标记 |
| **Spaced Repetition** | 对抗遗忘曲线 | Roadmap 内建 `[Review: DayXX]` |
| **Ultralearning** | 瓶颈时针对性爆破 | 触发 `drill(topic)` 提交 |

---

## 📁 项目标准目录结构 (Bootstrap Template)

```
<project-root>/
├── README.md              # 总地图：概览、快速入口
├── Roadmap.md             # SSOT：课题计划，含 [CORE] 标记与复习点
├── SyncState.md           # 仪表盘：当前进度指针 + Handover Note
│
├── Protocol/
│   ├── DEEP_MASTERY_PROTOCOL.md   # 本协议副本（持久化）
│   └── AGENT_FLIGHT_CHECKLIST.md  # 门控执行清单
│
├── Engineering/
│   ├── Standards.md       # 编码规范、命名约定
│   ├── Setup.md           # 环境搭建说明
│   ├── Retrospective.md   # 错误复盘记录
│   └── Journal.md         # 学习日志
│
├── Reference/
│   ├── Glossary.md        # 术语表（每课增量更新）
│   ├── QuickRef.md        # 高频代码片段速查
│   └── MentalModels.md    # 直觉理解（如："SDF 是距离的等高线"）
│
├── KnowledgeBase/         # 深度费曼笔记（每课一篇）
│   └── Day_01_<Topic>.md
│
├── src/                   # 实践代码（每课独立子目录）
│   ├── common/            # 可复用工具库
│   └── 01_<topic>/        # 脚手架生成
│
├── Gallery/               # 视觉成果快照
├── Verification/          # 自动化测试与验证脚本
└── tools/
    └── scaffold_lab.sh    # 课程脚手架生成器
```

---

## 🚀 Step 0: Bootstrap（首次启动专用）

当用户说"启动新学习项目"时，**必须**执行：

```bash
# 1. 创建目录结构
mkdir -p Reference Engineering Protocol KnowledgeBase Gallery src/common Verification tools

# 2. 询问用户：学习领域、目标天数、主要技术栈
# 3. 生成以下核心文件（见各模板节）：
#    - README.md
#    - Roadmap.md（含 [CORE] 标记的课题大纲）
#    - SyncState.md（初始状态）
#    - Protocol/DEEP_MASTERY_PROTOCOL.md（本协议）
#    - Engineering/Standards.md（领域规范）
#    - tools/scaffold_lab.sh（自动脚手架）
# 4. git init && git add . && git commit -m "chore: bootstrap DMP learning project"
```

### Bootstrap 必询问用户的三个问题

1. **学习领域**：例如 "OpenGL 图形学"、"Rust 系统编程"、"分布式系统"
2. **计划周期**：例如 "30天"、"60天"、"按章节不限时"
3. **每课产出物**：例如 "可运行Demo"、"代码+笔记"、"只要笔记"

---

## ✈️ 门控执行清单（每课必走四关）

> **核心原则**：未完成当前 Gate Output，禁止进入下一阶段。

### 🔒 Gate 1 — 启动与环境锁

- [ ] 读取 `SyncState.md`（当前进度）和 `Roadmap.md`（今日课题）
- [ ] 执行 `./tools/scaffold_lab.sh <day> <topic>` 生成脚手架
- [ ] 输出 `[PLAN]: 我将实现 X，预计产出 Y，涉及核心知识 Z`

**🚩 Gate Output 1**：脚手架已创建，PLAN 已声明

### 🔨 Gate 2 — 构建与验证

- [ ] 编写代码（**零占位符**原则）
- [ ] 关键参数必须通过 UI 暴露（ImGui / CLI flags / 配置文件）
- [ ] 构建达到 **0 Errors, 0 Warnings**（`-Werror` 或等效）
- [ ] 启动程序，目视/运行时验证无异常输出
- [ ] 截图/录屏存入 `Gallery/Day_XX_<Topic>.png`
- [ ] `git commit -m "feat(lab/XX): core logic verified"`

**🚩 Gate Output 2**：截图路径 + 逻辑提交 SHA

### 🧠 Gate 3 — 提炼与沉淀

- [ ] 创建 `KnowledgeBase/Day_XX_<Topic>.md`（见笔记模板）
- [ ] 增量更新 `Reference/Glossary.md`（新术语）
- [ ] 增量更新 `Reference/QuickRef.md`（高频片段）
- [ ] 增量更新 `Reference/MentalModels.md`（新直觉）
- [ ] `git commit -m "docs(kb/XX): distillation complete"`

**🚩 Gate Output 3**：KB 核心摘要 + 资产增量列表

### ⚖️ Gate 4 — 审计与交接

- [ ] 提交 MIR 报告（见模板）
- [ ] 清理临时文件
- [ ] 更新 `SyncState.md`（Handover Note 必须极其清晰）
- [ ] `git commit -m "sync: Day XX complete"`

**🚩 Gate Output 4**：MIR 报告输出

---

## 📝 KnowledgeBase 笔记模板

每课费曼笔记必须包含以下章节（达到 Bloom 分析层级）：

```markdown
# Day XX: <Topic>

## 核心问题
> 用一句话说明：这一课解决了什么问题？

## 原理推导
<!-- 数学公式（LaTeX）/ 算法逻辑 / 数据流图 -->

## 核心代码讲解
<!-- GLSL / Rust / Python 核心片段 + 逐行注释 -->

## 预期结果描述
<!-- 运行后应该看到/得到什么？用感官语言描述 -->

## 踩坑记录
<!-- 遇到的问题 + 根本原因 + 修复方案 -->

## 与历史知识的连接
<!-- Related Days: Day 03 (VAO), Day 08 (Phong) -->

## Self-Test Q&A
<!-- Q: 为什么要用 GL_LEQUAL？A: ... -->

## 资产来源
<!-- 纹理/模型来源记录（避免版权问题） -->
```

---

## 🛡️ MIR 报告模板（Mastery Integrity Report）

```markdown
### 🛡️ Mastery Integrity Report (MIR) — Day XX: <Topic>

- **[Status]**: Pass ✅ / Fail ❌
- **[Code]**: Build [0 Errors / 0 Warnings] | Runtime [Clean / Logs attached]
- **[Logic]**: 
  - UI 参数: [列出所有可调参数]
  - 核心算法: [一句话说明实现方式]
- **[Docs]**: 
  - KB: `KnowledgeBase/Day_XX_Topic.md` ✅
  - Glossary 新增: N 条
  - QuickRef 新增: N 条
  - MentalModels 新增: N 条
- **[Gallery]**: `Gallery/Day_XX_Topic.png` ✅
- **[Git]**: feat + docs + sync 三次原子提交 ✅
- **[Next]**: 下一课题简述
```

---

## 📦 Roadmap 课题条目格式

```markdown
## 第N阶段：<阶段名> (Day X - Day Y)
*目标：一句话描述阶段目标。*

- **[CORE] Day X: <核心课题>**
    - **课题**：具体要实现的东西
    - **核心**：涉及的关键概念/API
    - **[Review: Day Z]**：需要复习的历史内容（间隔重复）

- **Day X+1: <普通课题>**
    - **课题**：...
```

---

## 📮 Git 提交规范

| 类型 | 触发时机 | 示例 |
|------|----------|------|
| `feat(lab/XX)` | 代码跑通验证 | `feat(lab/17): logic verified` |
| `docs(kb/XX)` | 笔记文档完成 | `docs(kb/17): complete deep dive` |
| `docs(assets)` | Reference 资产同步 | `docs(assets): update glossary day 17` |
| `docs(gallery)` | 截图/GIF 添加 | `docs(gallery): add Day 17 snapshot` |
| `drill(topic)` | 针对性练习代码 | `drill(matrix): practice lookAt impl` |
| `refactor(core)` | 工具提取至 common | `refactor(core): extract Camera helper` |
| `docs(retro)` | 错误复盘记录 | `docs(retro): debug shadow map matrix order` |
| `sync` | 每课完成全局同步 | `sync: Day 17 complete` |

---

## 🔧 scaffold_lab.sh 模板

以下是通用脚手架脚本模板（根据技术栈替换 `# TECH-SPECIFIC` 部分）：

```bash
#!/usr/bin/env bash
# DMP Lab Scaffolder — 通用模板
# Usage: ./tools/scaffold_lab.sh <day_number> <topic_name>
set -e

DAY="$1"
TOPIC="$2"
DIR="src/${DAY}_${TOPIC}"

[[ -z "$DAY" || -z "$TOPIC" ]] && echo "Usage: $0 <day> <topic>" && exit 1
[[ -d "$DIR" ]] && echo "Directory $DIR already exists!" && exit 1

mkdir -p "$DIR"

# TECH-SPECIFIC: 生成 main 文件（根据领域替换）
cat > "$DIR/main.<ext>" << 'EOF'
// Day ${DAY}: ${TOPIC}
// [PLAN]: TODO — 填写本课实现目标
EOF

# 生成 KnowledgeBase 模板
cat > "KnowledgeBase/Day_${DAY}_${TOPIC}.md" << EOF
# Day ${DAY}: ${TOPIC}

## 核心问题
> TODO

## 原理推导

## 核心代码讲解

## 预期结果描述

## 踩坑记录

## 与历史知识的连接

## Self-Test Q&A

## 资产来源
EOF

echo "✅ Scaffolded: $DIR"
echo "📝 KB template: KnowledgeBase/Day_${DAY}_${TOPIC}.md"
```

---

## 📋 SyncState.md 初始模板

```markdown
# 🛑 CRITICAL PROTOCOLS
1. Zero-Placeholder Policy
2. Read-Back Verification
3. Handover Awareness: 每次会话结束前必须更新 Handover Note
4. Flight Checklist: 严格遵循 Protocol/AGENT_FLIGHT_CHECKLIST.md

**Role:** 你是 <领域> 专家导师，指导学习者系统性掌握该领域。

**Project Context:**
- **当前进度:** Day 00: Bootstrap
- **计划总量:** XX 天 / XX 章节

**Current Focus (Dashboard):**
- [ ] Day 01: <首课题>

---
**📝 Handover Note:**
- **当前状态**: 项目刚初始化，尚未开始任何课题。
- **下一步**: 执行 `./tools/scaffold_lab.sh 01 <topic>` 开始第一课。
```

---

## ⚠️ 强制约束（Safety Protocol）

1. **Zero-Placeholder Policy**：禁止使用 `(...)` `TODO` `...` 等占位符提交代码或文档。
2. **Zero Warning Policy**：所有编译警告视为错误，必须当场修复。
3. **Progression Integrity**：进阶内容禁止覆盖基础版本，必须新建独立目录。
4. **Handover Awareness**：每次会话结束必须更新 `SyncState.md`，为下一个 Agent 留清晰的交接信息。
5. **Read-Back Verification**：修改核心文档后主动读回验证完整性。
6. **Math Rigor**：公式必须用 LaTeX 记录，禁止用自然语言替代。

---

## 🎯 成功定义标准

一个 DMP 学习项目成功的标准：

| 维度 | 标准 |
|------|------|
| **代码能跑** | `src/` 项目验证成功，`Verification/` 测试通过 |
| **原理能讲** | `KnowledgeBase/` 达到 Bloom 分析/评价层级，能通过 Self-Test |
| **资产能留** | `Reference/` 体系完整，5 分钟内找回任意心智模型 |
| **记忆能回** | Spaced Repetition 轨道执行，历史课题定期复习 |
| **工具能复用** | `src/common/` 形成可移植的工具库 |
